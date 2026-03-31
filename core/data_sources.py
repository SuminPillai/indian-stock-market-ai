# core/data_sources.py
"""Data source fetchers for Indian stock market data.

Tiered approach:
  Tier 1: yfinance (primary, most reliable)
  Tier 2: NSE/BSE session-based (for exclusive data)
  Tier 3: Cached/offline fallback
"""

import time
from abc import ABC, abstractmethod
from typing import Any

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

from core.cache import FileCache, make_cache_key


class BaseFetcher(ABC):
    """Abstract base for all data source fetchers."""

    def __init__(self):
        self.cache = FileCache()

    @abstractmethod
    def name(self) -> str:
        """Data source name for cache keys and logging."""
        ...


class YFinanceFetcher(BaseFetcher):
    """Tier 1: yfinance for prices, fundamentals, corporate actions."""

    def name(self) -> str:
        return "yfinance"

    def _normalize_symbol(self, symbol: str) -> str:
        """Append .NS suffix for NSE tickers if not already suffixed."""
        if symbol.endswith(".NS") or symbol.endswith(".BO"):
            return symbol
        return f"{symbol}.NS"

    def get_price_history(
        self, symbol: str, period: str = "1mo", interval: str = "1d"
    ) -> pd.DataFrame:
        """Fetch historical OHLCV data."""
        cache_key = make_cache_key(self.name(), "price_history", symbol=symbol, period=period)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return pd.DataFrame(cached)

        ticker = yf.Ticker(self._normalize_symbol(symbol))
        df = ticker.history(period=period, interval=interval)
        if not df.empty:
            self.cache.set(cache_key, df.reset_index().to_dict(orient="list"), ttl_seconds=900)
        return df

    def get_info(self, symbol: str) -> dict[str, Any]:
        """Fetch stock info (PE, market cap, sector, etc.)."""
        cache_key = make_cache_key(self.name(), "info", symbol=symbol)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        ticker = yf.Ticker(self._normalize_symbol(symbol))
        info = ticker.info
        if info:
            self.cache.set(cache_key, info, ttl_seconds=86400)
        return info

    def get_options_chain(self, symbol: str, expiry: str | None = None) -> dict[str, pd.DataFrame]:
        """Fetch options chain via yfinance (basic data, no OI change)."""
        ticker = yf.Ticker(self._normalize_symbol(symbol))
        expirations = ticker.options
        if not expirations:
            return {"calls": pd.DataFrame(), "puts": pd.DataFrame()}
        target = expiry if expiry in expirations else expirations[0]
        chain = ticker.option_chain(target)
        return {"calls": chain.calls, "puts": chain.puts, "expiry": target}

    def get_financials(self, symbol: str) -> dict[str, pd.DataFrame]:
        """Fetch quarterly financials for fundamental analysis."""
        ticker = yf.Ticker(self._normalize_symbol(symbol))
        return {
            "income_stmt": ticker.quarterly_income_stmt,
            "balance_sheet": ticker.quarterly_balance_sheet,
            "cashflow": ticker.quarterly_cashflow,
        }


class NSESessionFetcher(BaseFetcher):
    """Tier 2: NSE website session-based access for exclusive data."""

    def name(self) -> str:
        return "nse"

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.nseindia.com"
        self._rate_limit = 3  # max requests per second
        self._last_request_time = 0.0
        self._session: requests.Session | None = None
        self._user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        ]
        self._ua_index = 0

    def _get_headers(self) -> dict[str, str]:
        """Get headers with rotating User-Agent."""
        ua = self._user_agents[self._ua_index % len(self._user_agents)]
        self._ua_index += 1
        return {
            "User-Agent": ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def _ensure_session(self) -> requests.Session:
        """Create or refresh session with NSE cookies."""
        if self._session is None:
            self._session = requests.Session()
            self._session.headers.update(self._get_headers())
            self._session.get(self.base_url, timeout=10)
        return self._session

    def _rate_limited_get(self, url: str, params: dict | None = None) -> dict | None:
        """Make a rate-limited GET request with exponential backoff (max 3 retries)."""
        elapsed = time.time() - self._last_request_time
        min_interval = 1.0 / self._rate_limit
        if elapsed < min_interval:
            time.sleep(min_interval - elapsed)

        max_retries = 3
        for attempt in range(max_retries):
            session = self._ensure_session()
            self._last_request_time = time.time()

            try:
                resp = session.get(url, params=params, timeout=15)
                if resp.status_code == 200:
                    return resp.json()
                elif resp.status_code in (403, 429):
                    self._session = None
                    backoff = 2 ** attempt * 2  # 2s, 4s, 8s
                    time.sleep(backoff)
                    continue
                return None
            except (requests.RequestException, ValueError):
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return None
        return None

    def get_fii_dii_data(self) -> dict | None:
        """Fetch FII/DII trading activity data."""
        cache_key = make_cache_key(self.name(), "fii_dii")
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        data = self._rate_limited_get(f"{self.base_url}/api/fiidiiTradeReact")
        if data:
            self.cache.set(cache_key, data, ttl_seconds=900)
        return data

    def get_options_chain(self, symbol: str = "NIFTY") -> dict | None:
        """Fetch live options chain from NSE."""
        cache_key = make_cache_key(self.name(), "option_chain", symbol=symbol)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        data = self._rate_limited_get(
            f"{self.base_url}/api/option-chain-indices" if symbol in ("NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY")
            else f"{self.base_url}/api/option-chain-equities",
            params={"symbol": symbol},
        )
        if data:
            self.cache.set(cache_key, data, ttl_seconds=900)
        return data

    def get_bulk_deals(self) -> dict | None:
        """Fetch bulk deal data from NSE."""
        cache_key = make_cache_key(self.name(), "bulk_deals")
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        data = self._rate_limited_get(f"{self.base_url}/api/snapshot-capital-market-largedeal")
        if data:
            self.cache.set(cache_key, data, ttl_seconds=3600)
        return data

    def get_market_status(self) -> dict | None:
        """Fetch current market status."""
        return self._rate_limited_get(f"{self.base_url}/api/marketStatus")


class BSEFetcher(BaseFetcher):
    """Tier 2: BSE for corporate filings, SME data, shareholding patterns."""

    def name(self) -> str:
        return "bse"

    def __init__(self):
        super().__init__()
        self.base_url = "https://api.bseindia.com/BseIndiaAPI/api"
        self._rate_limit = 5

    def get_shareholding_pattern(self, scrip_code: str) -> dict | None:
        """Fetch quarterly shareholding pattern from BSE."""
        cache_key = make_cache_key(self.name(), "shareholding", scrip_code=scrip_code)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            url = f"{self.base_url}/ShareholdingPattern/w"
            resp = requests.get(url, params={"scripcode": scrip_code}, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                self.cache.set(cache_key, data, ttl_seconds=86400)
                return data
        except (requests.RequestException, ValueError):
            pass
        return None


class AMFIFetcher(BaseFetcher):
    """Fetcher for AMFI mutual fund data."""

    def name(self) -> str:
        return "amfi"

    def __init__(self):
        super().__init__()
        self.nav_url = "https://www.amfiindia.com/spages/NAVAll.txt"

    def get_all_navs(self) -> pd.DataFrame:
        """Fetch all MF NAVs from AMFI."""
        cache_key = make_cache_key(self.name(), "all_navs")
        cached = self.cache.get(cache_key)
        if cached is not None:
            return pd.DataFrame(cached)

        try:
            resp = requests.get(self.nav_url, timeout=30)
            if resp.status_code == 200:
                lines = resp.text.strip().split("\n")
                records = []
                current_category = ""
                for line in lines:
                    if ";" not in line:
                        current_category = line.strip()
                        continue
                    parts = line.split(";")
                    if len(parts) >= 5:
                        records.append({
                            "category": current_category,
                            "scheme_code": parts[0].strip(),
                            "scheme_name": parts[1].strip() if len(parts) > 1 else "",
                            "nav": parts[4].strip() if len(parts) > 4 else "",
                            "date": parts[5].strip() if len(parts) > 5 else "",
                        })
                df = pd.DataFrame(records)
                self.cache.set(cache_key, df.to_dict(orient="list"), ttl_seconds=86400)
                return df
        except (requests.RequestException, ValueError):
            pass
        return pd.DataFrame()


class RBIFetcher(BaseFetcher):
    """Fetcher for RBI data (exchange rates, policy rates)."""

    def name(self) -> str:
        return "rbi"

    def get_usd_inr_rate(self) -> float | None:
        """Fetch latest USD/INR reference rate."""
        cache_key = make_cache_key(self.name(), "usd_inr")
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        # Fallback: use yfinance for USD/INR
        try:
            ticker = yf.Ticker("USDINR=X")
            hist = ticker.history(period="1d")
            if not hist.empty:
                rate = float(hist["Close"].iloc[-1])
                self.cache.set(cache_key, rate, ttl_seconds=3600)
                return rate
        except Exception:
            pass
        return None


class SEBIFetcher(BaseFetcher):
    """Fetcher for SEBI corporate filings, SAST disclosures, takeover announcements."""

    def name(self) -> str:
        return "sebi"

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.sebi.gov.in"
        self.nse_announcements_url = "https://www.nseindia.com/api/corporate-announcements"

    def get_sast_disclosures(self, symbol: str | None = None) -> list[dict]:
        """Fetch SAST (insider trading) disclosures from NSE corporate announcements."""
        cache_key = make_cache_key(self.name(), "sast", symbol=symbol or "all")
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            params = {"index": "equities"}
            if symbol:
                params["symbol"] = symbol
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            }
            session = requests.Session()
            session.get("https://www.nseindia.com", timeout=10)
            resp = session.get(self.nse_announcements_url, params=params, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                # Filter for SAST/insider trading announcements
                sast = [
                    d for d in data
                    if any(kw in d.get("desc", "").lower() for kw in ["sast", "insider", "acquisition", "shareholding"])
                ]
                self.cache.set(cache_key, sast, ttl_seconds=86400)
                return sast
        except (requests.RequestException, ValueError):
            pass
        return []
