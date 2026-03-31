# NSE Stock Analysis Claude Skills — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 10 Claude Code skills for Indian stock market analysis, backed by a shared Python core and YAML config.

**Architecture:** Modular skills with shared core — `core/` provides data fetching, formatting, and export; each skill in `skills/<name>/` has a `.md` (Claude Code skill definition) and `.py` (analysis logic). Config in `config/*.yaml` for frequently-changing Indian market data.

**Tech Stack:** Python 3.10+, yfinance, pandas, numpy, requests, beautifulsoup4, rich, tabulate, platformdirs, PyYAML, pytest

**Spec:** `docs/superpowers/specs/2026-03-26-nse-stock-analysis-skills-design.md`

---

## Phase 1: Project Scaffolding & Configuration

### Task 1: Repository scaffolding

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `setup.py`
- Create: `core/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/test_core/__init__.py`
- Create: `tests/test_skills/__init__.py`
- Create: `tests/fixtures/` (directory)
- Create: `skills/` (directory with 10 subdirectories)

- [ ] **Step 1: Create .gitignore**

```
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.pytest_cache/
.venv/
venv/
env/
.env
*.csv
*.json
!config/*.yaml
!tests/fixtures/*.json
.nse-skills-cache/
credentials.yaml
```

- [ ] **Step 2: Create requirements.txt**

```
yfinance>=0.2.31
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
beautifulsoup4>=4.12.0
rich>=13.0.0
tabulate>=0.9.0
platformdirs>=4.0.0
PyYAML>=6.0
pytest>=7.4.0
```

- [ ] **Step 3: Create setup.py**

```python
from setuptools import setup, find_packages

setup(
    name="nse-stock-analysis-skills",
    version="0.1.0",
    description="Claude Code skills for Indian stock market analysis",
    author="Sumin Pillai",
    author_email="suminpillai@gmail.com",
    url="https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    install_requires=[
        "yfinance>=0.2.31",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "rich>=13.0.0",
        "tabulate>=0.9.0",
        "platformdirs>=4.0.0",
        "PyYAML>=6.0",
    ],
)
```

- [ ] **Step 4: Create directory structure and __init__.py files**

```bash
mkdir -p core tests/test_core tests/test_skills tests/fixtures config
mkdir -p skills/nse_screener skills/fii_dii_tracker skills/nse_options_chain
mkdir -p skills/sebi_deal_scanner skills/promoter_analyzer skills/fo_strategy
mkdir -p skills/mf_flow_analyzer skills/sector_rotation skills/tax_calculator
mkdir -p skills/smallcap_discovery
touch core/__init__.py tests/__init__.py tests/test_core/__init__.py tests/test_skills/__init__.py
```

- [ ] **Step 5: Commit**

```bash
git add .gitignore requirements.txt setup.py core/__init__.py tests/ config/ skills/
git commit -m "feat: scaffold project structure with dependencies and config dirs"
```

---

### Task 2: YAML configuration files

**Files:**
- Create: `config/holidays.yaml`
- Create: `config/lot_sizes.yaml`
- Create: `config/tax_rules.yaml`
- Create: `config/stt_rates.yaml`
- Create: `config/sebi_categories.yaml`
- Create: `config/credentials.example.yaml`

- [ ] **Step 1: Create config/holidays.yaml**

```yaml
last_updated: "2026-03-26"
effective_from: "2025-04-01"
description: "NSE/BSE trading holidays for FY 2025-26"

holidays:
  - date: "2025-04-10"
    name: "Shri Mahavir Jayanti"
  - date: "2025-04-14"
    name: "Dr. Baba Saheb Ambedkar Jayanti"
  - date: "2025-04-18"
    name: "Good Friday"
  - date: "2025-05-01"
    name: "Maharashtra Day"
  - date: "2025-08-15"
    name: "Independence Day"
  - date: "2025-08-27"
    name: "Ganesh Chaturthi"
  - date: "2025-10-02"
    name: "Mahatma Gandhi Jayanti"
  - date: "2025-10-20"
    name: "Diwali (Laxmi Pujan)"
  - date: "2025-10-21"
    name: "Diwali Balipratipada"
  - date: "2025-11-05"
    name: "Guru Nanak Jayanti"
  - date: "2025-12-25"
    name: "Christmas"
  - date: "2026-01-26"
    name: "Republic Day"
  - date: "2026-03-10"
    name: "Maha Shivaratri"
  - date: "2026-03-17"
    name: "Holi"
  - date: "2026-03-25"
    name: "Id-Ul-Fitr (Ramadan)"
  - date: "2026-03-30"
    name: "Shri Ram Navami"
```

- [ ] **Step 2: Create config/lot_sizes.yaml**

```yaml
last_updated: "2026-03-26"
effective_from: "2026-01-01"
description: "F&O lot sizes — update quarterly from NSE circulars"

index_lots:
  NIFTY: 75
  BANKNIFTY: 30
  FINNIFTY: 65
  MIDCPNIFTY: 120

stock_lots:
  RELIANCE: 250
  TCS: 150
  HDFCBANK: 550
  INFY: 300
  ICICIBANK: 700
  SBIN: 750
  BHARTIARTL: 950
  ITC: 1600
  KOTAKBANK: 400
  LT: 150
  AXISBANK: 600
  HINDUNILVR: 300
  BAJFINANCE: 125
  MARUTI: 100
  TATAMOTORS: 575
  SUNPHARMA: 350
  TATASTEEL: 500
  WIPRO: 1500
  ASIANPAINT: 200
  HCLTECH: 350
```

- [ ] **Step 3: Create config/tax_rules.yaml**

```yaml
last_updated: "2026-03-26"
effective_from: "2024-07-23"
description: "Capital gains tax rules — post Union Budget 2024"

equity_listed:
  stcg_rate: 0.20
  stcg_holding_period_months: 12
  ltcg_rate: 0.125
  ltcg_exemption_per_fy: 125000
  grandfathering_date: "2018-01-31"

dividend:
  tds_threshold: 5000
  tds_rate: 0.10

surcharge_thresholds:
  - income_above: 5000000
    rate: 0.10
  - income_above: 10000000
    rate: 0.15
  - income_above: 20000000
    rate: 0.25
  - income_above: 50000000
    rate: 0.37

cess_rate: 0.04
```

- [ ] **Step 4: Create config/stt_rates.yaml**

```yaml
last_updated: "2026-03-26"
effective_from: "2024-10-01"
description: "Securities Transaction Tax rates — post Budget 2024"

equity_delivery:
  buy: 0.001
  sell: 0.001

equity_intraday:
  sell: 0.00025

futures:
  sell: 0.0125

options:
  sell: 0.01
  exercise: 0.00125
```

- [ ] **Step 5: Create config/sebi_categories.yaml**

```yaml
last_updated: "2026-03-26"
effective_from: "2017-10-06"
description: "SEBI mutual fund categorization norms and MWPL thresholds"

market_cap_classification:
  large_cap:
    rank_start: 1
    rank_end: 100
    description: "Top 100 companies by market capitalization"
  mid_cap:
    rank_start: 101
    rank_end: 250
    description: "101st to 250th by market capitalization"
  small_cap:
    rank_start: 251
    description: "251st and below by market capitalization"

fo_ban:
  mwpl_threshold: 0.95
  ban_description: "F&O ban triggered when OI exceeds 95% of MWPL"
```

- [ ] **Step 6: Create config/credentials.example.yaml**

```yaml
# Copy to ~/.nse-skills/credentials.yaml
# All keys are optional — skills work without them but with reduced data

bse_api_key: ""
amfi_api_key: ""
```

- [ ] **Step 7: Commit**

```bash
git add config/
git commit -m "feat: add YAML config files for holidays, lot sizes, tax, STT, SEBI categories"
```

---

## Phase 2: Shared Core Library

### Task 3: Constants and config loader (`core/constants.py`)

**Files:**
- Create: `core/constants.py`
- Create: `tests/test_core/test_constants.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_core/test_constants.py
import pytest
from datetime import date


def test_load_holidays():
    from core.constants import load_holidays
    holidays = load_holidays()
    assert isinstance(holidays, list)
    assert all(isinstance(h, date) for h in holidays)
    assert date(2025, 8, 15) in holidays  # Independence Day


def test_load_lot_sizes():
    from core.constants import load_lot_sizes
    lots = load_lot_sizes()
    assert lots["NIFTY"] == 75
    assert lots["BANKNIFTY"] == 30
    assert lots["RELIANCE"] == 250


def test_load_tax_rules():
    from core.constants import load_tax_rules
    rules = load_tax_rules()
    assert rules["equity_listed"]["stcg_rate"] == 0.20
    assert rules["equity_listed"]["ltcg_rate"] == 0.125
    assert rules["equity_listed"]["ltcg_exemption_per_fy"] == 125000


def test_load_stt_rates():
    from core.constants import load_stt_rates
    rates = load_stt_rates()
    assert rates["options"]["exercise"] == 0.00125


def test_is_trading_day():
    from core.constants import is_trading_day
    # Independence Day is a holiday
    assert is_trading_day(date(2025, 8, 15)) is False
    # Saturday
    assert is_trading_day(date(2025, 8, 16)) is False
    # Regular Monday (not a holiday)
    assert is_trading_day(date(2025, 8, 18)) is True


def test_get_current_fy():
    from core.constants import get_current_fy
    # March 2026 is still FY 2025-26
    assert get_current_fy(date(2026, 3, 26)) == "FY2025-26"
    # April 2026 starts FY 2026-27
    assert get_current_fy(date(2026, 4, 1)) == "FY2026-27"


# Static constants
def test_grandfathering_date():
    from core.constants import GRANDFATHERING_DATE
    assert GRANDFATHERING_DATE == date(2018, 1, 31)


def test_nifty_sectors():
    from core.constants import NIFTY_SECTORS
    assert "IT" in NIFTY_SECTORS
    assert "Bank" in NIFTY_SECTORS
    assert "Pharma" in NIFTY_SECTORS
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core/test_constants.py -v`
Expected: FAIL — module not found

- [ ] **Step 3: Implement core/constants.py**

```python
# core/constants.py
"""Indian market constants and YAML config loader."""

import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

GRANDFATHERING_DATE = date(2018, 1, 31)

NIFTY_SECTORS = [
    "IT", "Bank", "Pharma", "Auto", "FMCG", "Metal", "Realty",
    "Energy", "Infra", "PSU Bank", "Private Bank", "Media",
    "Financial Services", "Consumer Durables",
]

NIFTY_SECTORAL_INDICES = {
    "IT": "NIFTY IT",
    "Bank": "NIFTY BANK",
    "Pharma": "NIFTY PHARMA",
    "Auto": "NIFTY AUTO",
    "FMCG": "NIFTY FMCG",
    "Metal": "NIFTY METAL",
    "Realty": "NIFTY REALTY",
    "Energy": "NIFTY ENERGY",
    "Infra": "NIFTY INFRA",
    "PSU Bank": "NIFTY PSU BANK",
    "Private Bank": "NIFTY PRIVATE BANK",
    "Media": "NIFTY MEDIA",
    "Financial Services": "NIFTY FINANCIAL SERVICES",
    "Consumer Durables": "NIFTY CONSUMER DURABLES",
}

_CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_yaml(filename: str) -> dict[str, Any]:
    """Load a YAML config file from the config/ directory."""
    filepath = _CONFIG_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def load_holidays() -> list[date]:
    """Load trading holidays as a list of date objects."""
    data = _load_yaml("holidays.yaml")
    return [
        datetime.strptime(h["date"], "%Y-%m-%d").date()
        for h in data.get("holidays", [])
    ]


def load_lot_sizes() -> dict[str, int]:
    """Load F&O lot sizes. Returns dict mapping symbol -> lot size."""
    data = _load_yaml("lot_sizes.yaml")
    lots = {}
    lots.update(data.get("index_lots", {}))
    lots.update(data.get("stock_lots", {}))
    return lots


def load_tax_rules() -> dict[str, Any]:
    """Load tax rules from config."""
    return _load_yaml("tax_rules.yaml")


def load_stt_rates() -> dict[str, Any]:
    """Load STT rates from config."""
    return _load_yaml("stt_rates.yaml")


def load_sebi_categories() -> dict[str, Any]:
    """Load SEBI MF categorization norms."""
    return _load_yaml("sebi_categories.yaml")


def is_trading_day(d: date) -> bool:
    """Check if a date is a trading day (not weekend, not holiday)."""
    if d.weekday() >= 5:  # Saturday=5, Sunday=6
        return False
    holidays = load_holidays()
    return d not in holidays


def get_current_fy(d: date | None = None) -> str:
    """Get financial year string (e.g., 'FY2025-26') for a given date.
    FY runs April 1 to March 31. If no date given, uses today in IST.
    """
    if d is None:
        d = datetime.now(IST).date()
    if d.month >= 4:
        return f"FY{d.year}-{str(d.year + 1)[2:]}"
    else:
        return f"FY{d.year - 1}-{str(d.year)[2:]}"


def today_ist() -> date:
    """Get today's date in IST."""
    return datetime.now(IST).date()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core/test_constants.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add core/constants.py tests/test_core/test_constants.py
git commit -m "feat: add constants module with YAML config loader and IST helpers"
```

---

### Task 4: Cache module (`core/cache.py`)

**Files:**
- Create: `core/cache.py`
- Create: `tests/test_core/test_cache.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_core/test_cache.py
import pytest
import json
import time
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def tmp_cache(tmp_path):
    with patch.dict("os.environ", {"NSE_SKILLS_CACHE_DIR": str(tmp_path)}):
        from core.cache import FileCache
        return FileCache()


def test_cache_set_and_get(tmp_cache):
    tmp_cache.set("test_key", {"price": 100.5}, ttl_seconds=60)
    result = tmp_cache.get("test_key")
    assert result == {"price": 100.5}


def test_cache_miss(tmp_cache):
    result = tmp_cache.get("nonexistent")
    assert result is None


def test_cache_expiry(tmp_cache):
    tmp_cache.set("expire_key", {"data": 1}, ttl_seconds=1)
    time.sleep(1.1)
    result = tmp_cache.get("expire_key")
    assert result is None


def test_cache_clear(tmp_cache):
    tmp_cache.set("key1", "val1", ttl_seconds=60)
    tmp_cache.set("key2", "val2", ttl_seconds=60)
    tmp_cache.clear()
    assert tmp_cache.get("key1") is None
    assert tmp_cache.get("key2") is None


def test_cache_key_hashing(tmp_cache):
    """Identical params should produce same cache key."""
    from core.cache import make_cache_key
    k1 = make_cache_key("nse", "options_chain", symbol="NIFTY", expiry="nearest")
    k2 = make_cache_key("nse", "options_chain", symbol="NIFTY", expiry="nearest")
    assert k1 == k2


def test_cache_different_params(tmp_cache):
    from core.cache import make_cache_key
    k1 = make_cache_key("nse", "options_chain", symbol="NIFTY")
    k2 = make_cache_key("nse", "options_chain", symbol="BANKNIFTY")
    assert k1 != k2
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core/test_cache.py -v`
Expected: FAIL

- [ ] **Step 3: Implement core/cache.py**

```python
# core/cache.py
"""File-based cache with configurable TTL for market data."""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import platformdirs


def _get_cache_dir() -> Path:
    """Get cache directory — env var override or platform default."""
    env_dir = os.environ.get("NSE_SKILLS_CACHE_DIR")
    if env_dir:
        p = Path(env_dir)
    else:
        p = Path(platformdirs.user_cache_dir("nse-skills"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def make_cache_key(source: str, endpoint: str, **params) -> str:
    """Generate a deterministic cache key from source, endpoint, and params."""
    sorted_params = json.dumps(params, sort_keys=True)
    raw = f"{source}:{endpoint}:{sorted_params}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


class FileCache:
    """File-based cache with TTL, LRU eviction, and trading day boundary awareness."""

    MAX_CACHE_SIZE_MB = 500  # Evict LRU entries when cache exceeds this

    def __init__(self):
        self.cache_dir = _get_cache_dir()

    def _path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str) -> Any | None:
        """Get cached value if it exists and hasn't expired."""
        path = self._path(key)
        if not path.exists():
            return None
        try:
            with open(path, "r") as f:
                entry = json.load(f)
            if time.time() > entry["expires_at"]:
                path.unlink(missing_ok=True)
                return None
            # Touch file to update access time for LRU
            path.touch()
            return entry["data"]
        except (json.JSONDecodeError, KeyError):
            path.unlink(missing_ok=True)
            return None

    def set(self, key: str, data: Any, ttl_seconds: int = 900) -> None:
        """Cache data with a TTL in seconds."""
        entry = {
            "data": data,
            "created_at": time.time(),
            "expires_at": time.time() + ttl_seconds,
        }
        with open(self._path(key), "w") as f:
            json.dump(entry, f)
        self._evict_if_needed()

    def clear(self) -> None:
        """Remove all cached files."""
        for path in self.cache_dir.glob("*.json"):
            path.unlink(missing_ok=True)

    def invalidate_stale_trading_day(self) -> None:
        """Remove cache entries from previous trading days.
        Call at start of each new trading day to ensure fresh data.
        """
        from core.constants import today_ist, is_trading_day
        today = today_ist()
        if not is_trading_day(today):
            return  # No invalidation on non-trading days
        for path in self.cache_dir.glob("*.json"):
            try:
                with open(path, "r") as f:
                    entry = json.load(f)
                created = entry.get("created_at", 0)
                from datetime import datetime
                from core.constants import IST
                created_date = datetime.fromtimestamp(created, tz=IST).date()
                if created_date < today:
                    path.unlink(missing_ok=True)
            except (json.JSONDecodeError, KeyError, OSError):
                path.unlink(missing_ok=True)

    def _evict_if_needed(self) -> None:
        """Evict least-recently-used entries if cache exceeds max size."""
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))
        if total_size <= self.MAX_CACHE_SIZE_MB * 1024 * 1024:
            return
        # Sort by access time (oldest first) and delete until under limit
        files = sorted(self.cache_dir.glob("*.json"), key=lambda f: f.stat().st_atime)
        for f in files:
            if total_size <= self.MAX_CACHE_SIZE_MB * 1024 * 1024 * 0.8:
                break
            size = f.stat().st_size
            f.unlink(missing_ok=True)
            total_size -= size
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core/test_cache.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add core/cache.py tests/test_core/test_cache.py
git commit -m "feat: add file-based cache with TTL and cross-platform support"
```

---

### Task 5: Auth module (`core/auth.py`)

**Files:**
- Create: `core/auth.py`
- Create: `tests/test_core/test_auth.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_core/test_auth.py
import pytest
from pathlib import Path
from unittest.mock import patch


def test_load_credentials_missing_file():
    from core.auth import load_credentials
    with patch("core.auth._credentials_path", return_value=Path("/nonexistent/creds.yaml")):
        creds = load_credentials()
    assert creds == {}


def test_load_credentials_from_env():
    from core.auth import get_credential
    with patch.dict("os.environ", {"NSE_SKILLS_BSE_API_KEY": "test123"}):
        assert get_credential("bse_api_key") == "test123"


def test_get_credential_returns_none_when_missing():
    from core.auth import get_credential
    with patch.dict("os.environ", {}, clear=True):
        with patch("core.auth.load_credentials", return_value={}):
            assert get_credential("nonexistent_key") is None


def test_load_credentials_from_yaml_file(tmp_path):
    from core.auth import load_credentials
    creds_file = tmp_path / "credentials.yaml"
    creds_file.write_text("bse_api_key: yaml_key_123\namfi_api_key: amfi_456\n")
    with patch("core.auth._credentials_path", return_value=creds_file):
        creds = load_credentials()
    assert creds["bse_api_key"] == "yaml_key_123"
    assert creds["amfi_api_key"] == "amfi_456"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core/test_auth.py -v`
Expected: FAIL

- [ ] **Step 3: Implement core/auth.py**

```python
# core/auth.py
"""Optional credentials for enhanced data source access."""

import os
from pathlib import Path
from typing import Any

import yaml


def _credentials_path() -> Path:
    return Path.home() / ".nse-skills" / "credentials.yaml"


def load_credentials() -> dict[str, Any]:
    """Load credentials from YAML file. Returns empty dict if not found."""
    path = _credentials_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except (yaml.YAMLError, OSError):
        return {}


def get_credential(key: str) -> str | None:
    """Get a credential. Checks env vars first (NSE_SKILLS_<KEY>), then YAML file."""
    env_key = f"NSE_SKILLS_{key.upper()}"
    env_val = os.environ.get(env_key)
    if env_val:
        return env_val
    creds = load_credentials()
    val = creds.get(key)
    return val if val else None
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core/test_auth.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add core/auth.py tests/test_core/test_auth.py
git commit -m "feat: add auth module for optional API credentials"
```

---

### Task 6: Data sources — all fetchers (`core/data_sources.py`)

**Files:**
- Create: `core/data_sources.py`
- Create: `tests/test_core/test_data_sources.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_core/test_data_sources.py
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


def test_yfinance_fetcher_appends_ns_suffix():
    from core.data_sources import YFinanceFetcher
    fetcher = YFinanceFetcher()
    assert fetcher._normalize_symbol("RELIANCE") == "RELIANCE.NS"
    assert fetcher._normalize_symbol("RELIANCE.NS") == "RELIANCE.NS"
    assert fetcher._normalize_symbol("RELIANCE.BO") == "RELIANCE.BO"


def test_yfinance_fetcher_get_price_history_mocked():
    from core.data_sources import YFinanceFetcher
    fetcher = YFinanceFetcher()
    mock_df = pd.DataFrame({"Close": [2500, 2510, 2520]}, index=pd.date_range("2026-01-01", periods=3))
    with patch("yfinance.Ticker") as MockTicker:
        MockTicker.return_value.history.return_value = mock_df
        df = fetcher.get_price_history("RELIANCE", period="5d")
    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert len(df) == 3


def test_yfinance_fetcher_get_info_mocked():
    from core.data_sources import YFinanceFetcher
    fetcher = YFinanceFetcher()
    mock_info = {"marketCap": 1700000000000, "trailingPE": 25.0, "sector": "Energy"}
    with patch("yfinance.Ticker") as MockTicker:
        MockTicker.return_value.info = mock_info
        info = fetcher.get_info("RELIANCE")
    assert info["marketCap"] == 1700000000000


def test_nse_session_fetcher_init():
    from core.data_sources import NSESessionFetcher
    fetcher = NSESessionFetcher()
    assert fetcher.base_url == "https://www.nseindia.com"
    assert fetcher._rate_limit == 3


def test_nse_session_fetcher_has_rotating_ua():
    from core.data_sources import NSESessionFetcher
    fetcher = NSESessionFetcher()
    assert len(fetcher._user_agents) >= 3


def test_base_fetcher_interface():
    from core.data_sources import BaseFetcher
    with pytest.raises(TypeError):
        BaseFetcher()


def test_sebi_fetcher_exists():
    from core.data_sources import SEBIFetcher
    fetcher = SEBIFetcher()
    assert fetcher.name() == "sebi"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core/test_data_sources.py -v`
Expected: FAIL

- [ ] **Step 3: Implement core/data_sources.py**

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core/test_data_sources.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add core/data_sources.py tests/test_core/test_data_sources.py
git commit -m "feat: add data source fetchers — yfinance, NSE, BSE, AMFI, SEBI, RBI"
```

---

### Task 7: Formatters (`core/formatters.py`)

**Files:**
- Create: `core/formatters.py`
- Create: `tests/test_core/test_formatters.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_core/test_formatters.py
import pytest
import pandas as pd


def test_format_table_markdown():
    from core.formatters import format_table
    df = pd.DataFrame({"Symbol": ["RELIANCE", "TCS"], "Price": [2500.0, 3800.0]})
    result = format_table(df, fmt="markdown")
    assert "RELIANCE" in result
    assert "TCS" in result
    assert "|" in result


def test_format_table_rich():
    from core.formatters import format_table
    df = pd.DataFrame({"Symbol": ["RELIANCE"], "Price": [2500.0]})
    result = format_table(df, fmt="rich")
    assert "RELIANCE" in result


def test_sparkline():
    from core.formatters import sparkline
    data = [1, 3, 5, 7, 5, 3, 1]
    result = sparkline(data)
    assert isinstance(result, str)
    assert len(result) == 7


def test_sparkline_empty():
    from core.formatters import sparkline
    assert sparkline([]) == ""


def test_heatmap_color():
    from core.formatters import heatmap_color
    assert "green" in heatmap_color(100).lower() or "\033[32m" in heatmap_color(100)
    assert "red" in heatmap_color(-100).lower() or "\033[31m" in heatmap_color(-100)


def test_format_currency_inr():
    from core.formatters import format_inr
    assert format_inr(1500000) == "15,00,000"
    assert format_inr(125000.50) == "1,25,000.50"


def test_format_crores():
    from core.formatters import format_crores
    assert format_crores(15000000) == "1.50 Cr"
    assert format_crores(1500000000) == "150.00 Cr"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core/test_formatters.py -v`
Expected: FAIL

- [ ] **Step 3: Implement core/formatters.py**

```python
# core/formatters.py
"""Output formatters: tables, heatmaps, sparklines, INR formatting."""

import io
from typing import Sequence

import pandas as pd
from rich.console import Console
from rich.table import Table


SPARK_CHARS = "▁▂▃▄▅▆▇█"


def sparkline(data: Sequence[float | int]) -> str:
    """Generate an ASCII sparkline from a sequence of numbers."""
    if not data:
        return ""
    mn, mx = min(data), max(data)
    rng = mx - mn if mx != mn else 1
    return "".join(SPARK_CHARS[min(int((v - mn) / rng * (len(SPARK_CHARS) - 1)), len(SPARK_CHARS) - 1)] for v in data)


def heatmap_color(value: float) -> str:
    """Return ANSI color code based on value (green=positive, red=negative)."""
    if value > 0:
        return f"\033[32m{value:+.2f}\033[0m"
    elif value < 0:
        return f"\033[31m{value:+.2f}\033[0m"
    return f"{value:.2f}"


def format_table(df: pd.DataFrame, fmt: str = "markdown", title: str = "") -> str:
    """Format a DataFrame as a table string.

    Args:
        df: Data to format.
        fmt: 'markdown' or 'rich'.
        title: Optional table title.
    """
    if fmt == "markdown":
        return df.to_markdown(index=False)

    # Rich table
    console = Console(file=io.StringIO(), force_terminal=True, width=120)
    table = Table(title=title, show_lines=True)
    for col in df.columns:
        table.add_column(str(col))
    for _, row in df.iterrows():
        table.add_row(*[str(v) for v in row])
    console.print(table)
    return console.file.getvalue()


def format_inr(amount: float) -> str:
    """Format a number in Indian numbering system (lakhs, crores).
    Example: 1500000 -> '15,00,000'
    """
    is_negative = amount < 0
    amount = abs(amount)

    # Split into integer and decimal parts
    if isinstance(amount, float) and amount != int(amount):
        int_part = int(amount)
        dec_part = f".{str(amount).split('.')[1][:2]}"
    else:
        int_part = int(amount)
        dec_part = ""

    s = str(int_part)
    if len(s) <= 3:
        result = s
    else:
        result = s[-3:]
        s = s[:-3]
        while s:
            result = s[-2:] + "," + result
            s = s[:-2]

    return ("-" if is_negative else "") + result + dec_part


def format_crores(amount: float) -> str:
    """Format amount in crores. Example: 15000000 -> '1.50 Cr'"""
    return f"{amount / 10000000:.2f} Cr"


def format_percent(value: float, already_pct: bool = False) -> str:
    """Format as percentage string.

    Args:
        value: The value to format. By default treated as a decimal (0.156 -> '15.60%').
        already_pct: If True, value is already a percentage (15.6 -> '15.60%').
    """
    if already_pct:
        return f"{value:.2f}%"
    return f"{value * 100:.2f}%"


def narrative_summary(template: str, **kwargs) -> str:
    """Generate a narrative summary from a template and data."""
    return template.format(**kwargs)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core/test_formatters.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add core/formatters.py tests/test_core/test_formatters.py
git commit -m "feat: add formatters — tables, sparklines, heatmaps, INR formatting"
```

---

### Task 8: Exporters (`core/exporters.py`)

**Files:**
- Create: `core/exporters.py`
- Create: `tests/test_core/test_exporters.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_core/test_exporters.py
import pytest
import json
from pathlib import Path
import pandas as pd


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Symbol": ["RELIANCE", "TCS", "INFY"],
        "Price": [2500.0, 3800.0, 1600.0],
        "PE": [25.3, 30.1, 28.7],
    })


def test_export_csv(sample_df, tmp_path):
    from core.exporters import export_csv
    filepath = export_csv(sample_df, "test_export", output_dir=str(tmp_path))
    assert Path(filepath).exists()
    content = Path(filepath).read_text()
    assert "RELIANCE" in content
    assert "Symbol" in content


def test_export_json(sample_df, tmp_path):
    from core.exporters import export_json
    filepath = export_json(
        sample_df, "test_export",
        metadata={"query": "screener", "timestamp": "2026-03-26"},
        output_dir=str(tmp_path),
    )
    assert Path(filepath).exists()
    data = json.loads(Path(filepath).read_text())
    assert "data" in data
    assert "metadata" in data
    assert data["metadata"]["query"] == "screener"


def test_export_python_code(sample_df, tmp_path):
    from core.exporters import export_python
    filepath = export_python(
        skill_name="nse_screener",
        params={"sector": "IT", "limit": 20},
        output_dir=str(tmp_path),
    )
    assert Path(filepath).exists()
    code = Path(filepath).read_text()
    assert "import yfinance" in code or "import pandas" in code
    assert "nse_screener" in code.lower() or "sector" in code
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_core/test_exporters.py -v`
Expected: FAIL

- [ ] **Step 3: Implement core/exporters.py**

```python
# core/exporters.py
"""Export analysis results to CSV, JSON, or standalone Python scripts."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from core.constants import IST


def _timestamped_filename(prefix: str, ext: str) -> str:
    """Generate a timestamped filename."""
    ts = datetime.now(IST).strftime("%Y-%m-%d_%H%M%S")
    return f"{prefix}_{ts}.{ext}"


def export_csv(df: pd.DataFrame, prefix: str, output_dir: str = ".") -> str:
    """Export DataFrame to a timestamped CSV file."""
    filename = _timestamped_filename(prefix, "csv")
    filepath = Path(output_dir) / filename
    df.to_csv(filepath, index=False)
    return str(filepath)


def export_json(
    df: pd.DataFrame, prefix: str,
    metadata: dict[str, Any] | None = None,
    output_dir: str = ".",
) -> str:
    """Export DataFrame to JSON with metadata."""
    filename = _timestamped_filename(prefix, "json")
    filepath = Path(output_dir) / filename
    output = {
        "metadata": metadata or {},
        "data": df.to_dict(orient="records"),
        "exported_at": datetime.now(IST).isoformat(),
    }
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2, default=str)
    return str(filepath)


def export_python(
    skill_name: str,
    params: dict[str, Any],
    output_dir: str = ".",
) -> str:
    """Generate a standalone Python script that reproduces the analysis."""
    filename = _timestamped_filename(skill_name, "py")
    filepath = Path(output_dir) / filename

    params_str = json.dumps(params, indent=4)
    code = f'''#!/usr/bin/env python3
"""Standalone script generated by NSE Stock Analysis Skills.
Skill: {skill_name}
Generated: {datetime.now(IST).isoformat()}

Run: python {filename}
Requires: pip install yfinance pandas
"""

import yfinance as yf
import pandas as pd

# Parameters used
params = {params_str}


def main():
    """Reproduce the {skill_name} analysis."""
    print(f"Running {skill_name} with params: {{params}}")
    # TODO: Add skill-specific analysis code
    print("Analysis complete.")


if __name__ == "__main__":
    main()
'''
    with open(filepath, "w") as f:
        f.write(code)
    return str(filepath)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_core/test_exporters.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add core/exporters.py tests/test_core/test_exporters.py
git commit -m "feat: add exporters — CSV, JSON, Python code generation"
```

---

### Task 9: Core `__init__.py` — public API

**Files:**
- Modify: `core/__init__.py`

- [ ] **Step 1: Write the public API exports**

```python
# core/__init__.py
"""NSE Stock Analysis Skills — Shared Core Library."""

from core.constants import (
    IST,
    GRANDFATHERING_DATE,
    NIFTY_SECTORS,
    NIFTY_SECTORAL_INDICES,
    load_holidays,
    load_lot_sizes,
    load_tax_rules,
    load_stt_rates,
    load_sebi_categories,
    is_trading_day,
    get_current_fy,
    today_ist,
)
from core.cache import FileCache, make_cache_key
from core.auth import get_credential
from core.data_sources import (
    YFinanceFetcher,
    NSESessionFetcher,
    BSEFetcher,
    AMFIFetcher,
    SEBIFetcher,
    RBIFetcher,
)
from core.formatters import (
    format_table,
    sparkline,
    heatmap_color,
    format_inr,
    format_crores,
    format_percent,
)
from core.exporters import export_csv, export_json, export_python

__all__ = [
    "IST", "GRANDFATHERING_DATE", "NIFTY_SECTORS", "NIFTY_SECTORAL_INDICES",
    "load_holidays", "load_lot_sizes", "load_tax_rules", "load_stt_rates",
    "load_sebi_categories", "is_trading_day", "get_current_fy", "today_ist",
    "FileCache", "make_cache_key", "get_credential",
    "YFinanceFetcher", "NSESessionFetcher", "BSEFetcher", "AMFIFetcher", "SEBIFetcher", "RBIFetcher",
    "format_table", "sparkline", "heatmap_color", "format_inr", "format_crores", "format_percent",
    "export_csv", "export_json", "export_python",
]
```

- [ ] **Step 2: Run full core test suite**

Run: `pytest tests/test_core/ -v`
Expected: All PASS

- [ ] **Step 3: Commit**

```bash
git add core/__init__.py
git commit -m "feat: expose core public API via __init__.py"
```

---

## Phase 3: Skills 1-5

### Task 10: `/nse-screener` skill

**Files:**
- Create: `skills/nse_screener/screener.py`
- Create: `skills/nse_screener/nse-screener.md`
- Create: `tests/test_skills/test_nse_screener.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_nse_screener.py
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_yfinance_info():
    return {
        "RELIANCE": {"trailingPE": 25.0, "priceToBook": 2.5, "returnOnEquity": 0.15,
                      "debtToEquity": 40.0, "marketCap": 1700000000000, "sector": "Energy"},
        "TCS": {"trailingPE": 30.0, "priceToBook": 12.0, "returnOnEquity": 0.45,
                "debtToEquity": 5.0, "marketCap": 1300000000000, "sector": "Technology"},
        "INFY": {"trailingPE": 28.0, "priceToBook": 8.0, "returnOnEquity": 0.32,
                 "debtToEquity": 10.0, "marketCap": 600000000000, "sector": "Technology"},
    }


def test_compute_composite_score():
    from skills.nse_screener.screener import compute_composite_score
    stock = {
        "roe": 0.30, "roce": 0.25, "pe_percentile": 0.7,
        "debt_equity": 20.0, "pledge_pct": 0.0, "fii_trend": "increasing",
    }
    score = compute_composite_score(stock)
    assert 0 <= score <= 100


def test_apply_filters():
    from skills.nse_screener.screener import apply_filters
    stocks = pd.DataFrame({
        "symbol": ["A", "B", "C"],
        "pe": [15, 30, 50],
        "roe": [0.20, 0.10, 0.35],
        "market_cap_cr": [50000, 10000, 500],
    })
    filters = {"pe_max": 35, "roe_min": 0.15}
    result = apply_filters(stocks, filters)
    assert len(result) == 1  # Only A passes both filters
    assert result.iloc[0]["symbol"] == "A"


def test_screener_run_returns_dataframe():
    from skills.nse_screener.screener import run_screener
    with patch("skills.nse_screener.screener.YFinanceFetcher") as MockFetcher:
        mock = MockFetcher.return_value
        mock.get_info.side_effect = lambda s: {
            "trailingPE": 20, "returnOnEquity": 0.25, "returnOnAssets": 0.15,
            "debtToEquity": 30, "marketCap": 500000000000, "sector": "IT",
            "currentPrice": 1500,
        }
        result = run_screener(symbols=["INFY", "TCS"], limit=5)
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 5
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_skills/test_nse_screener.py -v`
Expected: FAIL

- [ ] **Step 3: Create __init__.py and implement screener.py**

All skill directories use underscores for Python import compatibility (e.g., `skills/nse_screener/`). The `.md` skill definition files keep hyphens in their filename (e.g., `nse-screener.md`).

```bash
touch skills/__init__.py skills/nse_screener/__init__.py
```

```python
# skills/nse_screener/screener.py
"""NSE Stock Screener — multi-factor screening with India-specific filters."""

import pandas as pd
import numpy as np
from typing import Any

from core.data_sources import YFinanceFetcher
from core.formatters import format_table, format_crores, heatmap_color, sparkline
from core.exporters import export_csv, export_json, export_python


# Default Nifty 50 symbols for screening
NIFTY_50 = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR",
    "SBIN", "BHARTIARTL", "ITC", "KOTAKBANK", "LT", "AXISBANK",
    "BAJFINANCE", "MARUTI", "TATAMOTORS", "SUNPHARMA", "TATASTEEL",
    "WIPRO", "ASIANPAINT", "HCLTECH", "ULTRACEMCO", "TITAN",
    "NESTLEIND", "BAJAJFINSV", "POWERGRID", "NTPC", "ONGC",
    "JSWSTEEL", "M&M", "ADANIENT", "TECHM", "COALINDIA",
    "GRASIM", "BRITANNIA", "DIVISLAB", "DRREDDY", "CIPLA",
    "EICHERMOT", "APOLLOHOSP", "HEROMOTOCO", "INDUSINDBK",
    "BPCL", "TATACONSUM", "SBILIFE", "HDFCLIFE", "BAJAJ-AUTO",
    "ADANIPORTS", "HINDALCO", "UPL", "SHRIRAMFIN",
]


def compute_composite_score(stock: dict[str, Any]) -> float:
    """Compute composite screening score (0-100).

    Weights: ROE 25%, ROCE 25%, PE percentile 20%, low D/E 15%, low pledge 15%.
    FII trend adjustment: +5 if increasing, -5 if decreasing.
    """
    roe_score = min(stock.get("roe", 0) / 0.30, 1.0) * 25
    roce_score = min(stock.get("roce", 0) / 0.25, 1.0) * 25
    pe_score = (1 - stock.get("pe_percentile", 0.5)) * 20

    de = stock.get("debt_equity", 100)
    de_score = max(0, (1 - de / 200)) * 15

    pledge = stock.get("pledge_pct", 0)
    pledge_score = max(0, (1 - pledge / 50)) * 15

    base = roe_score + roce_score + pe_score + de_score + pledge_score

    fii_trend = stock.get("fii_trend", "stable")
    if fii_trend == "increasing":
        base += 5
    elif fii_trend == "decreasing":
        base -= 5

    return max(0, min(100, base))


def apply_filters(df: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    """Apply screening filters to a DataFrame of stocks."""
    result = df.copy()
    if "pe_max" in filters:
        result = result[result["pe"] <= filters["pe_max"]]
    if "pe_min" in filters:
        result = result[result["pe"] >= filters["pe_min"]]
    if "roe_min" in filters:
        result = result[result["roe"] >= filters["roe_min"]]
    if "market_cap_min" in filters:
        result = result[result["market_cap_cr"] >= filters["market_cap_min"]]
    if "market_cap_max" in filters:
        result = result[result["market_cap_cr"] <= filters["market_cap_max"]]
    if "de_max" in filters:
        result = result[result.get("debt_equity", pd.Series(dtype=float)) <= filters["de_max"]]
    return result


def run_screener(
    symbols: list[str] | None = None,
    sector: str | None = None,
    filters: dict[str, Any] | None = None,
    sort_by: str = "composite_score",
    limit: int = 20,
) -> pd.DataFrame:
    """Run the stock screener and return ranked results."""
    if symbols is None:
        symbols = NIFTY_50

    fetcher = YFinanceFetcher()
    records = []

    for sym in symbols:
        try:
            info = fetcher.get_info(sym)
            if not info:
                continue

            record = {
                "symbol": sym,
                "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "pe": info.get("trailingPE", 0) or 0,
                "pb": info.get("priceToBook", 0) or 0,
                "roe": info.get("returnOnEquity", 0) or 0,
                "roce": info.get("returnOnAssets", 0) or 0,  # Proxy
                "debt_equity": info.get("debtToEquity", 0) or 0,
                "market_cap_cr": (info.get("marketCap", 0) or 0) / 10000000,
                "sector": info.get("sector", ""),
                "dividend_yield": info.get("dividendYield", 0) or 0,
            }
            records.append(record)
        except Exception:
            continue

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Filter by sector if specified
    if sector:
        df = df[df["sector"].str.contains(sector, case=False, na=False)]

    # Apply custom filters
    if filters:
        df = apply_filters(df, filters)

    # Compute PE percentile within results
    if len(df) > 0 and "pe" in df.columns:
        df["pe_percentile"] = df["pe"].rank(pct=True)
    else:
        df["pe_percentile"] = 0.5

    # Compute composite score
    df["composite_score"] = df.apply(
        lambda row: compute_composite_score({
            "roe": row["roe"],
            "roce": row["roce"],
            "pe_percentile": row.get("pe_percentile", 0.5),
            "debt_equity": row["debt_equity"],
            "pledge_pct": 0,
            "fii_trend": "stable",
        }),
        axis=1,
    )

    df = df.sort_values(sort_by, ascending=False).head(limit)
    return df.reset_index(drop=True)
```

- [ ] **Step 4: Write the skill .md file**

```markdown
---
name: nse-screener
description: Multi-factor stock screening with India-specific filters for NSE-listed stocks
---

# NSE Stock Screener

## Purpose
Screen NSE-listed stocks using fundamental, valuation, and India-specific filters (promoter holding, FII/DII %, pledge %). Returns ranked results with composite scores.

## Instructions
1. Parse user parameters. If no specific request, ask: "What would you like to screen for? (e.g., high ROE IT stocks, low PE large caps, low pledge midcaps)"
2. Run the screener by executing: `python -c "from skills.nse_screener.screener import run_screener; ..."`
3. Present results as a formatted markdown table
4. Highlight red flags (high pledge, declining promoter) and green flags (high ROE, low debt)
5. Offer export: "Would you like to export as CSV, JSON, or Python script?"

## Parameters
| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| sector | string | Nifty sectoral classification | All |
| market_cap | string | Large/Mid/Small/Micro or range in Cr | All |
| filters | dict | PE, PB, ROE, ROCE, D/E, div yield | None |
| india_filters | dict | Promoter %, FII %, DII %, pledge % | None |
| sort_by | string | Any metric | composite_score |
| limit | int | Number of results | 20 |
| export | string | csv/json/python/none | none |

## Example Usage

User: "Screen for high quality large cap IT stocks"
→ Run with sector="IT", market_cap="Large", filters={"roe_min": 0.15}

User: "Show me undervalued midcaps with low debt"
→ Run with market_cap="Mid", filters={"pe_max": 20, "de_max": 50}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_skills/test_nse_screener.py -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add skills/nse_screener/ tests/test_skills/test_nse_screener.py
git commit -m "feat: add /nse-screener skill — multi-factor stock screening"
```

---

### Task 11: `/fii-dii-tracker` skill

**Files:**
- Create: `skills/fii_dii_tracker/tracker.py`
- Create: `skills/fii_dii_tracker/fii-dii-tracker.md`
- Create: `tests/test_skills/test_fii_dii_tracker.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_fii_dii_tracker.py
import pytest
import pandas as pd


def test_classify_divergence():
    from skills.fii_dii_tracker.tracker import classify_divergence
    assert classify_divergence(fii_net=-500, dii_net=600) == "institutional_rotation"
    assert classify_divergence(fii_net=-500, dii_net=-300) == "risk_off"
    assert classify_divergence(fii_net=500, dii_net=300) == "broad_buying"
    assert classify_divergence(fii_net=500, dii_net=-100) == "fii_led_rally"


def test_compute_rolling_averages():
    from skills.fii_dii_tracker.tracker import compute_rolling_averages
    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=25, freq="B"),
        "fii_net": list(range(25)),
        "dii_net": list(range(25, 0, -1)),
    })
    result = compute_rolling_averages(df)
    assert "fii_net_5d_avg" in result.columns
    assert "fii_net_20d_avg" in result.columns
    assert "dii_net_5d_avg" in result.columns


def test_format_flow_summary():
    from skills.fii_dii_tracker.tracker import format_flow_summary
    summary = format_flow_summary(
        fii_total=-5000, dii_total=6000, nifty_change=2.5, period="1m"
    )
    assert "FII" in summary
    assert "DII" in summary
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_skills/test_fii_dii_tracker.py -v`
Expected: FAIL

- [ ] **Step 3: Implement skills/fii_dii_tracker/tracker.py**

```python
# skills/fii_dii_tracker/tracker.py
"""FII/DII Flow Tracker — institutional money flow analysis."""

import pandas as pd
from typing import Any

from core.data_sources import NSESessionFetcher, YFinanceFetcher
from core.formatters import format_table, sparkline, heatmap_color, format_crores


def classify_divergence(fii_net: float, dii_net: float) -> str:
    """Classify the FII/DII flow pattern."""
    if fii_net < 0 and dii_net > 0:
        return "institutional_rotation"
    elif fii_net < 0 and dii_net < 0:
        return "risk_off"
    elif fii_net > 0 and dii_net > 0:
        return "broad_buying"
    elif fii_net > 0 and dii_net < 0:
        return "fii_led_rally"
    return "neutral"


DIVERGENCE_SIGNALS = {
    "institutional_rotation": "FII selling + DII buying = Institutional rotation (historically mid-term bullish)",
    "risk_off": "Both selling = Risk-off environment (bearish signal)",
    "broad_buying": "Both buying = Broad rally fuel (bullish)",
    "fii_led_rally": "FII buying + DII selling = FII-led rally (watch for reversal)",
    "neutral": "Mixed signals — no clear directional bias",
}


def compute_rolling_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Add 5-day and 20-day rolling averages for FII and DII net flows."""
    result = df.copy()
    result["fii_net_5d_avg"] = result["fii_net"].rolling(5).mean()
    result["fii_net_20d_avg"] = result["fii_net"].rolling(20).mean()
    result["dii_net_5d_avg"] = result["dii_net"].rolling(5).mean()
    result["dii_net_20d_avg"] = result["dii_net"].rolling(20).mean()
    return result


def format_flow_summary(
    fii_total: float, dii_total: float, nifty_change: float, period: str
) -> str:
    """Generate narrative summary of flow data."""
    divergence = classify_divergence(fii_total, dii_total)
    signal = DIVERGENCE_SIGNALS.get(divergence, "")

    # fii_total and dii_total are in crores
    return (
        f"**FII/DII Flow Summary ({period})**\n\n"
        f"- FII Net: {fii_total:+,.0f} Cr "
        f"({'Bought' if fii_total > 0 else 'Sold'})\n"
        f"- DII Net: {dii_total:+,.0f} Cr "
        f"({'Bought' if dii_total > 0 else 'Sold'})\n"
        f"- Nifty Change: {nifty_change:+.2f}%\n\n"
        f"**Signal:** {signal}\n"
    )


def run_tracker(period: str = "1m", segment: str = "both", correlation: bool = True) -> dict[str, Any]:
    """Run the FII/DII tracker analysis.

    Returns dict with 'data' (DataFrame), 'summary' (str), 'divergence' (str).
    """
    nse = NSESessionFetcher()
    data = nse.get_fii_dii_data()

    if data is None:
        return {"data": pd.DataFrame(), "summary": "NSE data unavailable.", "divergence": "unknown"}

    # Parse NSE FII/DII response into DataFrame
    # Structure varies — handle both old and new NSE API formats
    records = []
    if isinstance(data, list):
        for entry in data:
            records.append({
                "category": entry.get("category", ""),
                "buy_value": float(entry.get("buyValue", 0)),
                "sell_value": float(entry.get("sellValue", 0)),
                "net_value": float(entry.get("netValue", 0)),
            })
    elif isinstance(data, dict):
        for key in ("fpiCashLast", "fpiCashPrev", "diiCashLast", "diiCashPrev"):
            if key in data:
                records.append({"category": key, **data[key]})

    df = pd.DataFrame(records) if records else pd.DataFrame()

    fii_total = sum(r["net_value"] for r in records if "fpi" in r.get("category", "").lower() or "fii" in r.get("category", "").lower())
    dii_total = sum(r["net_value"] for r in records if "dii" in r.get("category", "").lower())

    # Get Nifty performance for correlation
    nifty_change = 0.0
    if correlation:
        yf_fetcher = YFinanceFetcher()
        nifty_hist = yf_fetcher.get_price_history("^NSEI", period="1mo")
        if not nifty_hist.empty:
            nifty_change = ((nifty_hist["Close"].iloc[-1] / nifty_hist["Close"].iloc[0]) - 1) * 100

    divergence = classify_divergence(fii_total, dii_total)
    summary = format_flow_summary(fii_total, dii_total, nifty_change, period)

    return {"data": df, "summary": summary, "divergence": divergence}
```

- [ ] **Step 4: Create skill .md and __init__.py**

```bash
touch skills/fii_dii_tracker/__init__.py
```

Write `skills/fii_dii_tracker/fii-dii-tracker.md` with skill definition (same pattern as nse-screener.md).

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_skills/test_fii_dii_tracker.py -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add skills/fii_dii_tracker/ tests/test_skills/test_fii_dii_tracker.py
git commit -m "feat: add /fii-dii-tracker skill — institutional flow analysis"
```

---

### Task 12: `/nse-options-chain` skill

**Files:**
- Create: `skills/nse_options_chain/options_chain.py`
- Create: `skills/nse_options_chain/nse-options-chain.md`
- Create: `tests/test_skills/test_nse_options_chain.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_nse_options_chain.py
import pytest
import pandas as pd


def test_compute_pcr():
    from skills.nse_options_chain.options_chain import compute_pcr
    assert compute_pcr(put_oi=500000, call_oi=400000) == pytest.approx(1.25)
    assert compute_pcr(put_oi=0, call_oi=100) == 0.0


def test_compute_max_pain():
    from skills.nse_options_chain.options_chain import compute_max_pain
    strikes = [24000, 24100, 24200, 24300, 24400]
    call_oi = [50000, 40000, 30000, 20000, 10000]
    put_oi = [10000, 20000, 30000, 40000, 50000]
    max_pain = compute_max_pain(strikes, call_oi, put_oi)
    assert max_pain in strikes


def test_classify_oi_buildup():
    from skills.nse_options_chain.options_chain import classify_oi_buildup
    assert classify_oi_buildup(price_change=50, oi_change=1000) == "long_buildup"
    assert classify_oi_buildup(price_change=-50, oi_change=1000) == "short_buildup"
    assert classify_oi_buildup(price_change=50, oi_change=-1000) == "short_covering"
    assert classify_oi_buildup(price_change=-50, oi_change=-1000) == "long_unwinding"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_skills/test_nse_options_chain.py -v`
Expected: FAIL

- [ ] **Step 3: Implement options_chain.py**

```python
# skills/nse_options_chain/options_chain.py
"""NSE Options Chain Analyzer — PCR, max pain, OI buildup, IV skew."""

import pandas as pd
import numpy as np
from typing import Any

from core.data_sources import NSESessionFetcher
from core.constants import load_lot_sizes
from core.formatters import format_table, heatmap_color


def compute_pcr(put_oi: int, call_oi: int) -> float:
    """Compute Put-Call Ratio from OI."""
    if call_oi == 0:
        return 0.0
    return put_oi / call_oi


def compute_max_pain(
    strikes: list[int], call_oi: list[int], put_oi: list[int]
) -> int:
    """Compute max pain strike — the strike where total option buyers lose the most."""
    min_pain = float("inf")
    max_pain_strike = strikes[0]

    for i, strike in enumerate(strikes):
        total_pain = 0
        for j, s in enumerate(strikes):
            if s < strike:
                total_pain += put_oi[j] * (strike - s)
            elif s > strike:
                total_pain += call_oi[j] * (s - strike)
        if total_pain < min_pain:
            min_pain = total_pain
            max_pain_strike = strike

    return max_pain_strike


def classify_oi_buildup(price_change: float, oi_change: float) -> str:
    """Classify OI buildup type based on price and OI change."""
    if price_change > 0 and oi_change > 0:
        return "long_buildup"
    elif price_change < 0 and oi_change > 0:
        return "short_buildup"
    elif price_change > 0 and oi_change < 0:
        return "short_covering"
    elif price_change < 0 and oi_change < 0:
        return "long_unwinding"
    return "neutral"


OI_BUILDUP_LABELS = {
    "long_buildup": "Long Buildup (Bullish)",
    "short_buildup": "Short Buildup (Bearish)",
    "short_covering": "Short Covering (Bullish, weak)",
    "long_unwinding": "Long Unwinding (Bearish, weak)",
    "neutral": "Neutral",
}


def parse_nse_options_data(raw_data: dict) -> pd.DataFrame:
    """Parse NSE options chain API response into a clean DataFrame."""
    if not raw_data or "records" not in raw_data:
        return pd.DataFrame()

    records = raw_data["records"].get("data", [])
    parsed = []
    for record in records:
        row = {"strikePrice": record.get("strikePrice", 0)}
        if "CE" in record:
            ce = record["CE"]
            row.update({
                "ce_oi": ce.get("openInterest", 0),
                "ce_change_oi": ce.get("changeinOpenInterest", 0),
                "ce_volume": ce.get("totalTradedVolume", 0),
                "ce_iv": ce.get("impliedVolatility", 0),
                "ce_ltp": ce.get("lastPrice", 0),
            })
        if "PE" in record:
            pe = record["PE"]
            row.update({
                "pe_oi": pe.get("openInterest", 0),
                "pe_change_oi": pe.get("changeinOpenInterest", 0),
                "pe_volume": pe.get("totalTradedVolume", 0),
                "pe_iv": pe.get("impliedVolatility", 0),
                "pe_ltp": pe.get("lastPrice", 0),
            })
        parsed.append(row)

    return pd.DataFrame(parsed)


def run_options_analysis(
    symbol: str = "NIFTY",
    strikes: int = 10,
    analysis: str = "all",
) -> dict[str, Any]:
    """Run full options chain analysis."""
    nse = NSESessionFetcher()
    raw = nse.get_options_chain(symbol)

    if raw is None:
        return {"error": "Could not fetch options chain from NSE."}

    df = parse_nse_options_data(raw)
    if df.empty:
        return {"error": "No options data available."}

    # Find ATM strike
    spot = raw.get("records", {}).get("underlyingValue", 0)
    df["dist_from_atm"] = abs(df["strikePrice"] - spot)
    df = df.nsmallest(strikes * 2, "dist_from_atm").sort_values("strikePrice")

    results: dict[str, Any] = {"spot": spot, "data": df, "symbol": symbol}

    # PCR
    total_put_oi = df.get("pe_oi", pd.Series(dtype=int)).sum()
    total_call_oi = df.get("ce_oi", pd.Series(dtype=int)).sum()
    results["pcr"] = compute_pcr(total_put_oi, total_call_oi)

    # Max Pain
    results["max_pain"] = compute_max_pain(
        df["strikePrice"].tolist(),
        df.get("ce_oi", pd.Series(0, index=df.index)).tolist(),
        df.get("pe_oi", pd.Series(0, index=df.index)).tolist(),
    )

    # Support/Resistance from OI
    if "pe_oi" in df.columns:
        results["support"] = df.loc[df["pe_oi"].idxmax(), "strikePrice"]
    if "ce_oi" in df.columns:
        results["resistance"] = df.loc[df["ce_oi"].idxmax(), "strikePrice"]

    return results
```

- [ ] **Step 4: Create __init__.py and .md, run tests**

Run: `pytest tests/test_skills/test_nse_options_chain.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add skills/nse_options_chain/ tests/test_skills/test_nse_options_chain.py
git commit -m "feat: add /nse-options-chain skill — PCR, max pain, OI analysis"
```

---

### Task 13: `/sebi-deal-scanner` skill

**Files:**
- Create: `skills/sebi_deal_scanner/deal_scanner.py`
- Create: `skills/sebi_deal_scanner/sebi-deal-scanner.md`
- Create: `tests/test_skills/test_sebi_deal_scanner.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_sebi_deal_scanner.py
import pytest
import pandas as pd


def test_classify_entity():
    from skills.sebi_deal_scanner.deal_scanner import classify_entity
    assert classify_entity("GOLDMAN SACHS") == "FII"
    assert classify_entity("LIC OF INDIA") == "DII"
    assert classify_entity("MUKESH AMBANI") == "Promoter/HNI"
    assert classify_entity("RANDOM PERSON") == "Unknown"


def test_detect_patterns():
    from skills.sebi_deal_scanner.deal_scanner import detect_patterns
    deals = pd.DataFrame({
        "symbol": ["RELIANCE", "RELIANCE", "TCS"],
        "buyer": ["ENTITY A", "ENTITY A", "ENTITY B"],
        "value_cr": [10, 15, 5],
        "date": ["2026-03-20", "2026-03-21", "2026-03-22"],
    })
    patterns = detect_patterns(deals)
    assert any("repeated" in p.lower() for p in patterns)


def test_compute_liquidity_impact():
    from skills.sebi_deal_scanner.deal_scanner import compute_liquidity_impact
    # Deal of 50 Cr on stock with ADTV of 100 Cr = 50%
    assert compute_liquidity_impact(deal_value_cr=50, adtv_cr=100) == pytest.approx(50.0)
    assert compute_liquidity_impact(deal_value_cr=50, adtv_cr=0) == 0.0
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement deal_scanner.py**

```python
# skills/sebi_deal_scanner/deal_scanner.py
"""SEBI Insider & Bulk Deal Scanner."""

import pandas as pd
from typing import Any

from core.data_sources import NSESessionFetcher
from core.formatters import format_table, format_crores


KNOWN_FIIS = ["GOLDMAN SACHS", "MORGAN STANLEY", "JPMORGAN", "CITIGROUP",
              "CLSA", "NOMURA", "BARCLAYS", "HSBC", "DEUTSCHE", "UBS",
              "BNP PARIBAS", "SOCIETE GENERALE", "CREDIT SUISSE", "MACQUARIE"]

KNOWN_DIIS = ["LIC OF INDIA", "SBI MUTUAL FUND", "HDFC MUTUAL FUND",
              "ICICI PRUDENTIAL", "KOTAK MUTUAL", "NIPPON INDIA",
              "AXIS MUTUAL FUND", "UTI MUTUAL FUND", "ADITYA BIRLA"]


def classify_entity(name: str) -> str:
    """Classify a deal entity as FII, DII, Promoter/HNI, or Unknown."""
    name_upper = name.upper()
    for fii in KNOWN_FIIS:
        if fii in name_upper:
            return "FII"
    for dii in KNOWN_DIIS:
        if dii in name_upper:
            return "DII"
    # Heuristic: individual names (no corporate keywords) -> Promoter/HNI
    corporate_keywords = ["LIMITED", "LTD", "FUND", "CAPITAL", "SECURITIES", "INVESTMENTS", "PVT", "LLC"]
    if not any(kw in name_upper for kw in corporate_keywords):
        return "Promoter/HNI"
    return "Unknown"


def detect_patterns(deals: pd.DataFrame) -> list[str]:
    """Detect notable patterns in deal data."""
    patterns = []

    # Repeated buying by same entity
    if "buyer" in deals.columns:
        buyer_counts = deals["buyer"].value_counts()
        for buyer, count in buyer_counts.items():
            if count >= 2:
                patterns.append(f"Repeated buying by {buyer} ({count} deals)")

    # Large concentration in single stock
    if "symbol" in deals.columns and "value_cr" in deals.columns:
        by_symbol = deals.groupby("symbol")["value_cr"].sum()
        for sym, total in by_symbol.items():
            if total > 50:
                patterns.append(f"Large accumulation in {sym}: {format_crores(total * 10000000)}")

    return patterns


def compute_liquidity_impact(deal_value_cr: float, adtv_cr: float) -> float:
    """Compute deal value as % of Average Daily Traded Value."""
    if adtv_cr == 0:
        return 0.0
    return (deal_value_cr / adtv_cr) * 100


def run_deal_scanner(
    deal_type: str = "all",
    period: str = "1w",
    symbol: str | None = None,
    min_value: float = 1.0,
) -> dict[str, Any]:
    """Run the deal scanner."""
    nse = NSESessionFetcher()
    raw = nse.get_bulk_deals()

    if raw is None:
        return {"data": pd.DataFrame(), "patterns": [], "summary": "NSE data unavailable."}

    # Parse deals
    deals_list = raw if isinstance(raw, list) else raw.get("data", [])
    records = []
    for deal in deals_list:
        records.append({
            "symbol": deal.get("symbol", ""),
            "deal_type": deal.get("dealType", "Bulk"),
            "buyer": deal.get("clientName", ""),
            "value_cr": float(deal.get("value", 0)) / 10000000,
            "quantity": deal.get("quantity", 0),
            "price": deal.get("price", 0),
            "date": deal.get("dealDate", ""),
        })

    df = pd.DataFrame(records)
    if df.empty:
        return {"data": df, "patterns": [], "summary": "No deals found."}

    # Apply filters
    if symbol:
        df = df[df["symbol"] == symbol.upper()]
    if deal_type != "all":
        df = df[df["deal_type"].str.lower() == deal_type.lower()]
    df = df[df["value_cr"] >= min_value]

    # Classify entities
    if "buyer" in df.columns:
        df["entity_type"] = df["buyer"].apply(classify_entity)

    patterns = detect_patterns(df)

    return {"data": df, "patterns": patterns, "summary": f"Found {len(df)} deals."}
```

- [ ] **Step 4: Run tests, create __init__.py and .md**

- [ ] **Step 5: Commit**

```bash
git add skills/sebi_deal_scanner/ tests/test_skills/test_sebi_deal_scanner.py
git commit -m "feat: add /sebi-deal-scanner skill — bulk/block deal analysis"
```

---

### Task 14: `/promoter-analyzer` skill

**Files:**
- Create: `skills/promoter_analyzer/promoter.py`
- Create: `skills/promoter_analyzer/promoter-analyzer.md`
- Create: `tests/test_skills/test_promoter_analyzer.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_promoter_analyzer.py
import pytest
import pandas as pd


def test_detect_red_flags():
    from skills.promoter_analyzer.promoter import detect_red_flags
    holdings = pd.DataFrame({
        "quarter": ["Q1", "Q2", "Q3", "Q4"],
        "promoter_pct": [60, 58, 55, 52],
        "pledge_pct": [10, 15, 22, 45],
    })
    flags = detect_red_flags(holdings)
    assert any("pledge" in f.lower() for f in flags)
    assert any("declining" in f.lower() or "decreasing" in f.lower() for f in flags)


def test_detect_green_flags():
    from skills.promoter_analyzer.promoter import detect_green_flags
    holdings = pd.DataFrame({
        "quarter": ["Q1", "Q2", "Q3", "Q4"],
        "promoter_pct": [50, 52, 54, 56],
        "pledge_pct": [20, 15, 10, 5],
    })
    flags = detect_green_flags(holdings)
    assert any("increasing" in f.lower() for f in flags)
    assert any("pledge" in f.lower() and "reduc" in f.lower() for f in flags)


def test_compute_qoq_changes():
    from skills.promoter_analyzer.promoter import compute_qoq_changes
    holdings = pd.DataFrame({
        "promoter_pct": [60, 58, 55],
        "fii_pct": [20, 22, 25],
    })
    result = compute_qoq_changes(holdings)
    assert "promoter_pct_change" in result.columns
    assert result["promoter_pct_change"].iloc[1] == pytest.approx(-2.0)
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement promoter.py**

```python
# skills/promoter_analyzer/promoter.py
"""Promoter Holding & Pledge Analyzer."""

import pandas as pd
from typing import Any

from core.data_sources import BSEFetcher, YFinanceFetcher
from core.formatters import format_table, sparkline, format_percent


def compute_qoq_changes(df: pd.DataFrame) -> pd.DataFrame:
    """Compute quarter-over-quarter changes for all percentage columns."""
    result = df.copy()
    pct_cols = [c for c in df.columns if c.endswith("_pct")]
    for col in pct_cols:
        result[f"{col}_change"] = result[col].diff()
    return result


def detect_red_flags(holdings: pd.DataFrame) -> list[str]:
    """Detect red flags in promoter holding patterns."""
    flags = []

    # High pledge
    if "pledge_pct" in holdings.columns:
        latest_pledge = holdings["pledge_pct"].iloc[-1]
        if latest_pledge > 40:
            flags.append(f"RED FLAG: Pledge at {latest_pledge:.1f}% — dangerously high (>40%)")

        # Rising pledge for 3+ quarters
        if len(holdings) >= 3:
            recent = holdings["pledge_pct"].iloc[-3:]
            if all(recent.diff().dropna() > 0):
                flags.append("RED FLAG: Pledge increasing for 3+ consecutive quarters")

    # Declining promoter holding
    if "promoter_pct" in holdings.columns and len(holdings) >= 2:
        changes = holdings["promoter_pct"].diff().dropna()
        if all(changes.iloc[-3:] < 0) if len(changes) >= 3 else False:
            flags.append("RED FLAG: Promoter stake declining for 3+ quarters")

        # Double red: declining + rising pledge
        if "pledge_pct" in holdings.columns:
            if holdings["promoter_pct"].iloc[-1] < holdings["promoter_pct"].iloc[0]:
                if holdings["pledge_pct"].iloc[-1] > holdings["pledge_pct"].iloc[0]:
                    flags.append("DOUBLE RED FLAG: Promoter declining + pledge increasing")

    return flags


def detect_green_flags(holdings: pd.DataFrame) -> list[str]:
    """Detect green flags in promoter holding patterns."""
    flags = []

    if "promoter_pct" in holdings.columns and len(holdings) >= 2:
        changes = holdings["promoter_pct"].diff().dropna()
        if all(changes.iloc[-3:] > 0) if len(changes) >= 3 else changes.iloc[-1] > 0:
            flags.append("GREEN FLAG: Promoter increasing stake — positive conviction signal")

    if "pledge_pct" in holdings.columns and len(holdings) >= 3:
        recent = holdings["pledge_pct"].iloc[-3:]
        if all(recent.diff().dropna() < 0):
            flags.append("GREEN FLAG: Pledge reducing for 3+ quarters — de-leveraging")

    return flags


def run_promoter_analysis(symbol: str, quarters: int = 8) -> dict[str, Any]:
    """Run promoter holding analysis for a stock."""
    bse = BSEFetcher()
    yf = YFinanceFetcher()

    # Get basic stock info
    info = yf.get_info(symbol)
    stock_name = info.get("shortName", symbol) if info else symbol

    # Fetch shareholding data from BSE
    shareholding = bse.get_shareholding_pattern(symbol)

    if shareholding is None:
        return {"error": f"Could not fetch shareholding data for {symbol}"}

    # Parse into DataFrame (structure depends on BSE API response)
    # This is a simplified parser — actual BSE response may vary
    df = pd.DataFrame(shareholding) if isinstance(shareholding, list) else pd.DataFrame()

    if df.empty:
        return {"error": "No shareholding data available"}

    df = df.tail(quarters)
    df = compute_qoq_changes(df)
    red_flags = detect_red_flags(df)
    green_flags = detect_green_flags(df)

    return {
        "symbol": symbol,
        "name": stock_name,
        "data": df,
        "red_flags": red_flags,
        "green_flags": green_flags,
    }
```

- [ ] **Step 4: Run tests, create files**

- [ ] **Step 5: Commit**

```bash
git add skills/promoter_analyzer/ tests/test_skills/test_promoter_analyzer.py
git commit -m "feat: add /promoter-analyzer skill — holding & pledge analysis"
```

---

## Phase 4: Skills 6-10

### Task 15: `/fo-strategy` skill

**Files:**
- Create: `skills/fo_strategy/strategy.py`
- Create: `skills/fo_strategy/fo-strategy.md`
- Create: `tests/test_skills/test_fo_strategy.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_fo_strategy.py
import pytest


def test_compute_payoff_long_call():
    from skills.fo_strategy.strategy import compute_payoff
    # Long call: strike=24000, premium=200, spot=24500 -> payoff=300
    assert compute_payoff("long_call", strike=24000, premium=200, spot=24500) == 300
    # OTM: payoff = -premium
    assert compute_payoff("long_call", strike=24000, premium=200, spot=23500) == -200


def test_compute_payoff_long_put():
    from skills.fo_strategy.strategy import compute_payoff
    assert compute_payoff("long_put", strike=24000, premium=150, spot=23500) == 350
    assert compute_payoff("long_put", strike=24000, premium=150, spot=24500) == -150


def test_compute_breakeven():
    from skills.fo_strategy.strategy import compute_breakeven
    legs = [
        {"type": "long_call", "strike": 24000, "premium": 200},
    ]
    breakevens = compute_breakeven(legs)
    assert 24200 in breakevens


def test_generate_ascii_payoff():
    from skills.fo_strategy.strategy import generate_ascii_payoff
    legs = [{"type": "long_call", "strike": 24000, "premium": 200}]
    chart = generate_ascii_payoff(legs, spot=24000)
    assert isinstance(chart, str)
    assert len(chart) > 0


def test_recommend_strategy():
    from skills.fo_strategy.strategy import recommend_strategy
    strategies = recommend_strategy(outlook="bullish", iv_percentile=0.3)
    assert len(strategies) >= 1
    assert all("name" in s for s in strategies)
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement strategy.py**

```python
# skills/fo_strategy/strategy.py
"""Indian F&O Strategy Builder — build and evaluate derivative strategies."""

import numpy as np
from typing import Any

from core.constants import load_lot_sizes, load_stt_rates


def compute_payoff(
    leg_type: str, strike: float, premium: float, spot: float
) -> float:
    """Compute payoff for a single option leg at a given spot price."""
    if leg_type == "long_call":
        return max(spot - strike, 0) - premium
    elif leg_type == "short_call":
        return premium - max(spot - strike, 0)
    elif leg_type == "long_put":
        return max(strike - spot, 0) - premium
    elif leg_type == "short_put":
        return premium - max(strike - spot, 0)
    return 0


def compute_breakeven(legs: list[dict[str, Any]]) -> list[float]:
    """Compute breakeven points for a multi-leg strategy."""
    # For single legs
    breakevens = []
    for leg in legs:
        if leg["type"] == "long_call":
            breakevens.append(leg["strike"] + leg["premium"])
        elif leg["type"] == "long_put":
            breakevens.append(leg["strike"] - leg["premium"])
        elif leg["type"] == "short_call":
            breakevens.append(leg["strike"] + leg["premium"])
        elif leg["type"] == "short_put":
            breakevens.append(leg["strike"] - leg["premium"])
    return breakevens


def compute_strategy_payoff(
    legs: list[dict[str, Any]], spot_range: np.ndarray
) -> np.ndarray:
    """Compute total strategy payoff across a range of spot prices."""
    total = np.zeros_like(spot_range, dtype=float)
    for leg in legs:
        for i, spot in enumerate(spot_range):
            total[i] += compute_payoff(leg["type"], leg["strike"], leg["premium"], spot)
    return total


def generate_ascii_payoff(
    legs: list[dict[str, Any]], spot: float, width: int = 60, height: int = 15
) -> str:
    """Generate an ASCII payoff diagram."""
    # Create spot range around current price
    strikes = [leg["strike"] for leg in legs]
    min_s = min(strikes) - (spot * 0.05)
    max_s = max(strikes) + (spot * 0.05)
    spot_range = np.linspace(min_s, max_s, width)

    payoffs = compute_strategy_payoff(legs, spot_range)
    max_payoff = max(abs(payoffs.max()), abs(payoffs.min()), 1)

    lines = []
    for row in range(height, -1, -1):
        level = (row / height * 2 - 1) * max_payoff
        line = ""
        for col in range(width):
            if abs(payoffs[col] - level) < max_payoff / height:
                line += "*"
            elif abs(level) < max_payoff / height:
                line += "-"
            else:
                line += " "
        lines.append(f"{level:>10.0f} |{line}")

    return "\n".join(lines)


def recommend_strategy(
    outlook: str, iv_percentile: float = 0.5, capital: float | None = None
) -> list[dict[str, str]]:
    """Recommend strategies based on outlook and IV."""
    strategies = []

    if outlook == "bullish":
        if iv_percentile < 0.3:
            strategies.append({"name": "Long Call", "reason": "Low IV = cheap premium"})
            strategies.append({"name": "Bull Call Spread", "reason": "Defined risk bullish"})
        else:
            strategies.append({"name": "Bull Put Spread", "reason": "Collect premium, bullish bias"})
            strategies.append({"name": "Short Put", "reason": "High IV = rich premium"})
    elif outlook == "bearish":
        if iv_percentile < 0.3:
            strategies.append({"name": "Long Put", "reason": "Low IV = cheap premium"})
            strategies.append({"name": "Bear Put Spread", "reason": "Defined risk bearish"})
        else:
            strategies.append({"name": "Bear Call Spread", "reason": "Collect premium, bearish bias"})
    elif outlook == "neutral":
        strategies.append({"name": "Iron Condor", "reason": "Range-bound, collect premium"})
        strategies.append({"name": "Short Straddle", "reason": "Neutral, high premium but unlimited risk"})
    elif outlook == "high_vol":
        strategies.append({"name": "Long Straddle", "reason": "Expecting big move, direction unknown"})
        strategies.append({"name": "Long Strangle", "reason": "Cheaper than straddle, needs bigger move"})
    elif outlook == "low_vol":
        strategies.append({"name": "Iron Butterfly", "reason": "Tight range expected"})
        strategies.append({"name": "Short Strangle", "reason": "Collect premium, low vol"})

    return strategies


def compute_stt_impact(legs: list[dict], lot_size: int) -> dict[str, float]:
    """Compute STT impact for exercised ITM options."""
    stt_rates = load_stt_rates()
    exercise_rate = stt_rates.get("options", {}).get("exercise", 0.00125)
    sell_rate = stt_rates.get("options", {}).get("sell", 0.01)

    stt_on_sell = sum(
        leg["premium"] * lot_size * sell_rate
        for leg in legs if leg["type"].startswith("long")
    )
    stt_on_exercise = sum(
        max(0, leg.get("intrinsic", 0)) * lot_size * exercise_rate
        for leg in legs if leg["type"].startswith("long")
    )

    return {"stt_on_sell": stt_on_sell, "stt_on_exercise": stt_on_exercise}
```

- [ ] **Step 4: Run tests, create files**

- [ ] **Step 5: Commit**

```bash
git add skills/fo_strategy/ tests/test_skills/test_fo_strategy.py
git commit -m "feat: add /fo-strategy skill — F&O strategy builder with payoff analysis"
```

---

### Task 16: `/mf-flow-analyzer` skill

**Files:**
- Create: `skills/mf_flow_analyzer/mf_flows.py`
- Create: `skills/mf_flow_analyzer/mf-flow-analyzer.md`
- Create: `tests/test_skills/test_mf_flow_analyzer.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_mf_flow_analyzer.py
import pytest
import pandas as pd


def test_classify_category():
    from skills.mf_flow_analyzer.mf_flows import classify_category
    assert classify_category("HDFC Large Cap Fund") == "large_cap"
    assert classify_category("SBI Small Cap Fund") == "small_cap"
    assert classify_category("ICICI Prudential Balanced Advantage") == "hybrid"


def test_compute_flow_summary():
    from skills.mf_flow_analyzer.mf_flows import compute_flow_summary
    flows = pd.DataFrame({
        "category": ["equity", "equity", "debt"],
        "net_flow_cr": [5000, 3000, -2000],
        "month": ["2026-01", "2026-02", "2026-01"],
    })
    summary = compute_flow_summary(flows)
    assert summary["equity_total"] == 8000
    assert summary["debt_total"] == -2000
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement mf_flows.py**

```python
# skills/mf_flow_analyzer/mf_flows.py
"""Mutual Fund & SIP Flow Analyzer — track domestic savings flow."""

import pandas as pd
from typing import Any

from core.data_sources import AMFIFetcher
from core.formatters import format_table, sparkline, format_crores


CATEGORY_KEYWORDS = {
    "large_cap": ["large cap", "largecap", "large-cap", "bluechip"],
    "mid_cap": ["mid cap", "midcap", "mid-cap"],
    "small_cap": ["small cap", "smallcap", "small-cap"],
    "flexi_cap": ["flexi cap", "flexicap", "multi cap", "multicap"],
    "hybrid": ["balanced", "hybrid", "advantage", "aggressive"],
    "debt": ["liquid", "overnight", "money market", "gilt", "corporate bond"],
    "thematic": ["thematic", "sectoral", "infrastructure", "technology", "pharma"],
    "index": ["index", "nifty", "sensex", "etf"],
}


def classify_category(scheme_name: str) -> str:
    """Classify a MF scheme into a category based on its name."""
    name_lower = scheme_name.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in name_lower for kw in keywords):
            return category
    return "other"


def compute_flow_summary(flows: pd.DataFrame) -> dict[str, float]:
    """Compute summary statistics from flow data."""
    summary = {}
    if "category" in flows.columns and "net_flow_cr" in flows.columns:
        by_cat = flows.groupby("category")["net_flow_cr"].sum()
        for cat, total in by_cat.items():
            summary[f"{cat}_total"] = total
    summary["total_net"] = flows["net_flow_cr"].sum() if "net_flow_cr" in flows.columns else 0
    return summary


def compute_sip_trend(monthly_sip_data: list[dict]) -> dict[str, Any]:
    """Analyze SIP book size trend."""
    if not monthly_sip_data:
        return {"trend": "unknown", "data": []}
    amounts = [d.get("sip_amount_cr", 0) for d in monthly_sip_data]
    if len(amounts) >= 3:
        recent = amounts[-3:]
        if all(recent[i] >= recent[i-1] for i in range(1, len(recent))):
            trend = "increasing"
        elif all(recent[i] <= recent[i-1] for i in range(1, len(recent))):
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    return {"trend": trend, "sparkline": sparkline(amounts), "latest": amounts[-1] if amounts else 0}


def compare_mf_fii_flows(mf_net: float, fii_net: float) -> str:
    """Compare MF and FII flow directions for conviction signal."""
    if mf_net > 0 and fii_net < 0:
        return "Strong domestic conviction — MFs buying while FIIs sell"
    elif mf_net > 0 and fii_net > 0:
        return "Broad rally fuel — both MFs and FIIs buying"
    elif mf_net < 0 and fii_net > 0:
        return "FII-led — domestic redemption pressure"
    elif mf_net < 0 and fii_net < 0:
        return "Risk-off across the board"
    return "Neutral"


def run_mf_analysis(
    period: str = "3m", category: str = "all", analysis: str = "all"
) -> dict[str, Any]:
    """Run mutual fund flow analysis."""
    amfi = AMFIFetcher()
    navs = amfi.get_all_navs()

    if navs.empty:
        return {"data": pd.DataFrame(), "summary": "AMFI data unavailable."}

    # Classify schemes
    if "scheme_name" in navs.columns:
        navs["mf_category"] = navs["scheme_name"].apply(classify_category)

    if category != "all":
        navs = navs[navs["mf_category"] == category]

    return {
        "data": navs,
        "summary": f"Analyzed {len(navs)} schemes across categories.",
        "flow_summary": compute_flow_summary(navs) if "net_flow_cr" in navs.columns else {},
    }
```

- [ ] **Step 4: Run tests, create __init__.py and .md files**

- [ ] **Step 5: Commit**

```bash
git add skills/mf_flow_analyzer/ tests/test_skills/test_mf_flow_analyzer.py
git commit -m "feat: add /mf-flow-analyzer skill — mutual fund flow analysis"
```

---

### Task 17: `/sector-rotation` skill

**Files:**
- Create: `skills/sector_rotation/rotation.py`
- Create: `skills/sector_rotation/sector-rotation.md`
- Create: `tests/test_skills/test_sector_rotation.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_sector_rotation.py
import pytest
import pandas as pd


def test_compute_relative_strength():
    from skills.sector_rotation.rotation import compute_relative_strength
    sector = pd.Series([100, 102, 105, 108, 112])
    benchmark = pd.Series([100, 101, 102, 103, 104])
    rs = compute_relative_strength(sector, benchmark)
    assert rs > 1.0  # Sector outperforming


def test_classify_sector_cycle():
    from skills.sector_rotation.rotation import classify_sector_cycle
    assert classify_sector_cycle(momentum_1m=5, momentum_3m=10, momentum_6m=15) == "early_cycle"
    assert classify_sector_cycle(momentum_1m=-2, momentum_3m=-5, momentum_6m=10) == "late_cycle"


def test_get_macro_triggers():
    from skills.sector_rotation.rotation import get_macro_triggers
    triggers = get_macro_triggers("IT")
    assert any("USD/INR" in t for t in triggers)
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement rotation.py**

```python
# skills/sector_rotation/rotation.py
"""India Sector Rotation Tracker — sectoral cycles mapped to India-specific macro triggers."""

import pandas as pd
import numpy as np
from typing import Any

from core.data_sources import YFinanceFetcher, RBIFetcher
from core.constants import NIFTY_SECTORAL_INDICES
from core.formatters import format_table, sparkline


MACRO_TRIGGERS = {
    "IT": ["USD/INR appreciation (positive for IT exports)", "US tech spending cycles"],
    "Bank": ["RBI repo rate cuts (positive)", "Credit growth data", "NPA resolution"],
    "Pharma": ["USFDA approval/warning letters", "US generic pricing", "API cost trends"],
    "Auto": ["Monthly sales data (SIAM)", "Festive season demand", "EV policy push"],
    "FMCG": ["Monsoon quality (IMD data)", "Rural wage growth", "Commodity input costs"],
    "Metal": ["China demand/stimulus", "Global commodity cycle", "Govt infra capex"],
    "Realty": ["RBI rate policy", "Housing sales data (PropEquity)", "RERA compliance"],
    "Energy": ["Crude oil prices (inverse)", "Govt fuel pricing policy", "Renewable push"],
    "Infra": ["Union Budget capex allocation", "Order book inflows", "Railways modernization"],
    "PSU Bank": ["RBI policy", "NPA recovery", "Govt recapitalization"],
    "Private Bank": ["Credit growth", "NIM trends", "Digital banking adoption"],
    "Financial Services": ["RBI liquidity (NBFC)", "AUM growth", "Insurance penetration"],
    "Consumer Durables": ["Festive/summer demand", "Rural electrification", "BIS standards"],
    "Media": ["Ad revenue trends", "Digital subscription growth", "IPL/cricket seasons"],
}


def compute_relative_strength(sector: pd.Series, benchmark: pd.Series) -> float:
    """Compute relative strength of sector vs benchmark.
    RS > 1.0 means sector outperforming.
    """
    if len(sector) < 2 or len(benchmark) < 2:
        return 1.0
    sector_return = (sector.iloc[-1] / sector.iloc[0]) - 1
    bench_return = (benchmark.iloc[-1] / benchmark.iloc[0]) - 1
    if bench_return == 0:
        return 1.0
    return (1 + sector_return) / (1 + bench_return)


def classify_sector_cycle(
    momentum_1m: float, momentum_3m: float, momentum_6m: float
) -> str:
    """Classify sector in market cycle based on momentum across timeframes."""
    if momentum_1m > 0 and momentum_3m > 0 and momentum_6m > 0:
        if momentum_1m > momentum_3m:
            return "early_cycle"  # Accelerating
        return "mid_cycle"  # Steady outperformance
    elif momentum_6m > 0 and momentum_1m < 0:
        return "late_cycle"  # Decelerating
    elif momentum_1m < 0 and momentum_3m < 0 and momentum_6m < 0:
        return "defensive"  # Underperforming across all timeframes
    return "transitioning"


CYCLE_DESCRIPTIONS = {
    "early_cycle": "Accelerating — momentum building, early entry opportunity",
    "mid_cycle": "Steady outperformance — trend established",
    "late_cycle": "Decelerating — momentum fading, consider profit-taking",
    "defensive": "Underperforming — avoid or watch for reversal signals",
    "transitioning": "Mixed signals — watch for confirmation",
}


def get_macro_triggers(sector: str) -> list[str]:
    """Get India-specific macro triggers for a sector."""
    return MACRO_TRIGGERS.get(sector, ["No specific triggers mapped"])


def run_sector_rotation(
    period: str = "6m", benchmark: str = "nifty_50", triggers: bool = True
) -> dict[str, Any]:
    """Run sector rotation analysis."""
    yf = YFinanceFetcher()

    # Fetch benchmark
    bench_symbol = "^NSEI" if benchmark == "nifty_50" else "^CRSLDX"
    bench_data = yf.get_price_history(bench_symbol, period=period)

    results = []
    for sector_name, index_name in NIFTY_SECTORAL_INDICES.items():
        yf_symbol = index_name.replace(" ", "").upper()
        # NSE sectoral indices via yfinance use specific symbols
        sector_data = yf.get_price_history(f"^{yf_symbol}", period=period)

        if sector_data.empty or bench_data.empty:
            continue

        # Compute momentum at different timeframes
        close = sector_data["Close"]
        m1 = ((close.iloc[-1] / close.iloc[-min(22, len(close))]) - 1) * 100 if len(close) > 22 else 0
        m3 = ((close.iloc[-1] / close.iloc[-min(66, len(close))]) - 1) * 100 if len(close) > 66 else 0
        m6 = ((close.iloc[-1] / close.iloc[0]) - 1) * 100

        rs = compute_relative_strength(close, bench_data["Close"])
        cycle = classify_sector_cycle(m1, m3, m6)

        result = {
            "sector": sector_name,
            "1m_return": round(m1, 2),
            "3m_return": round(m3, 2),
            "6m_return": round(m6, 2),
            "relative_strength": round(rs, 3),
            "cycle": cycle,
            "cycle_signal": CYCLE_DESCRIPTIONS.get(cycle, ""),
        }
        if triggers:
            result["macro_triggers"] = get_macro_triggers(sector_name)

        results.append(result)

    df = pd.DataFrame(results).sort_values("relative_strength", ascending=False)
    return {"data": df, "benchmark": benchmark, "period": period}
```

- [ ] **Step 4: Run tests, create __init__.py and .md files**

- [ ] **Step 5: Commit**

```bash
git add skills/sector_rotation/ tests/test_skills/test_sector_rotation.py
git commit -m "feat: add /sector-rotation skill — India sector cycle tracker"
```

---

### Task 18: `/tax-calculator` skill

**Files:**
- Create: `skills/tax_calculator/tax_calc.py`
- Create: `skills/tax_calculator/tax-calculator.md`
- Create: `tests/test_skills/test_tax_calculator.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_tax_calculator.py
import pytest
from datetime import date


def test_classify_holding_stcg():
    from skills.tax_calculator.tax_calc import classify_holding
    result = classify_holding(buy_date=date(2026, 1, 1), sell_date=date(2026, 6, 1))
    assert result == "STCG"


def test_classify_holding_ltcg():
    from skills.tax_calculator.tax_calc import classify_holding
    result = classify_holding(buy_date=date(2025, 1, 1), sell_date=date(2026, 3, 1))
    assert result == "LTCG"


def test_grandfathered_cost():
    from skills.tax_calculator.tax_calc import compute_grandfathered_cost
    # Bought at 500, FMV on 31/01/2018 was 800, selling at 1000
    cost = compute_grandfathered_cost(actual_cost=500, fmv_jan2018=800, sell_price=1000)
    assert cost == 800  # max(500, 800) = 800, capped at sell_price 1000 → 800

    # Bought at 900, FMV was 800, selling at 1000
    cost = compute_grandfathered_cost(actual_cost=900, fmv_jan2018=800, sell_price=1000)
    assert cost == 900  # max(900, 800) = 900

    # FMV > sell price → cost = sell price (no loss allowed via grandfathering)
    cost = compute_grandfathered_cost(actual_cost=500, fmv_jan2018=1200, sell_price=1000)
    assert cost == 1000


def test_compute_ltcg_tax():
    from skills.tax_calculator.tax_calc import compute_ltcg_tax
    # Gain of 2,25,000 → exempt 1,25,000 → taxable 1,00,000 → tax = 12,500
    tax = compute_ltcg_tax(total_ltcg=225000)
    assert tax == pytest.approx(12500)


def test_compute_ltcg_tax_within_exemption():
    from skills.tax_calculator.tax_calc import compute_ltcg_tax
    tax = compute_ltcg_tax(total_ltcg=100000)
    assert tax == 0


def test_compute_stcg_tax():
    from skills.tax_calculator.tax_calc import compute_stcg_tax
    tax = compute_stcg_tax(total_stcg=100000)
    assert tax == pytest.approx(20000)


def test_tax_loss_harvesting_suggestion():
    from skills.tax_calculator.tax_calc import suggest_tax_loss_harvest
    holdings = [
        {"symbol": "A", "unrealized_gain": 50000},
        {"symbol": "B", "unrealized_gain": -30000},
        {"symbol": "C", "unrealized_gain": -10000},
    ]
    suggestions = suggest_tax_loss_harvest(holdings, realized_gain=50000)
    assert len(suggestions) > 0
    assert any(s["symbol"] == "B" for s in suggestions)
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement tax_calc.py**

```python
# skills/tax_calculator/tax_calc.py
"""Indian Tax-Aware P&L Calculator."""

from datetime import date
from typing import Any

from core.constants import GRANDFATHERING_DATE, load_tax_rules, get_current_fy


def classify_holding(buy_date: date, sell_date: date) -> str:
    """Classify as STCG (<12 months) or LTCG (>=12 months)."""
    delta = (sell_date - buy_date).days
    return "LTCG" if delta >= 365 else "STCG"


def compute_grandfathered_cost(
    actual_cost: float, fmv_jan2018: float, sell_price: float
) -> float:
    """Compute cost of acquisition with grandfathering for pre-31-Jan-2018 holdings.

    Cost = max(actual_cost, FMV_31Jan2018), but capped at sell_price.
    If FMV > sell_price, cost = sell_price (no artificial loss).
    """
    if fmv_jan2018 > sell_price:
        return sell_price
    return max(actual_cost, fmv_jan2018)


def compute_ltcg_tax(total_ltcg: float) -> float:
    """Compute LTCG tax with Rs 1.25L exemption at 12.5% rate."""
    rules = load_tax_rules()
    eq = rules["equity_listed"]
    exemption = eq["ltcg_exemption_per_fy"]
    rate = eq["ltcg_rate"]
    taxable = max(0, total_ltcg - exemption)
    return taxable * rate


def compute_stcg_tax(total_stcg: float) -> float:
    """Compute STCG tax at 20% flat rate."""
    rules = load_tax_rules()
    rate = rules["equity_listed"]["stcg_rate"]
    return max(0, total_stcg) * rate


def suggest_tax_loss_harvest(
    holdings: list[dict[str, Any]], realized_gain: float
) -> list[dict[str, Any]]:
    """Suggest holdings to sell for tax-loss harvesting."""
    losers = [h for h in holdings if h["unrealized_gain"] < 0]
    losers.sort(key=lambda h: h["unrealized_gain"])  # Biggest loss first

    suggestions = []
    remaining_gain = realized_gain
    for h in losers:
        if remaining_gain <= 0:
            break
        loss = abs(h["unrealized_gain"])
        offset = min(loss, remaining_gain)
        suggestions.append({
            "symbol": h["symbol"],
            "loss": h["unrealized_gain"],
            "tax_saved": offset * 0.20,  # STCG offset saves at 20%
        })
        remaining_gain -= offset

    return suggestions


def run_tax_calculator(
    holdings: list[dict[str, Any]],
    sell_price: str = "current",
    financial_year: str | None = None,
) -> dict[str, Any]:
    """Run the full tax calculation."""
    if financial_year is None:
        financial_year = get_current_fy()

    from core.data_sources import YFinanceFetcher
    yf = YFinanceFetcher()

    results = []
    total_ltcg = 0
    total_stcg = 0

    for h in holdings:
        symbol = h["symbol"]
        buy_date = date.fromisoformat(h["buy_date"]) if isinstance(h["buy_date"], str) else h["buy_date"]
        buy_price = h["buy_price"]
        qty = h["quantity"]

        # Get current price
        if sell_price == "current":
            info = yf.get_info(symbol)
            current = info.get("currentPrice", buy_price) if info else buy_price
        else:
            current = float(sell_price)

        today = date.today()
        classification = classify_holding(buy_date, today)

        # Grandfathering for pre-2018 holdings
        effective_cost = buy_price
        if buy_date <= GRANDFATHERING_DATE and classification == "LTCG":
            hist = yf.get_price_history(symbol, period="max")
            fmv = buy_price  # Fallback
            if not hist.empty:
                jan2018 = hist[hist.index.date <= GRANDFATHERING_DATE]
                if not jan2018.empty:
                    fmv = float(jan2018["Close"].iloc[-1])
            effective_cost = compute_grandfathered_cost(buy_price, fmv, current)

        gain = (current - effective_cost) * qty

        if classification == "LTCG":
            total_ltcg += gain
        else:
            total_stcg += gain

        results.append({
            "symbol": symbol,
            "buy_date": str(buy_date),
            "buy_price": buy_price,
            "sell_price": current,
            "quantity": qty,
            "gain": gain,
            "classification": classification,
            "effective_cost": effective_cost,
        })

    ltcg_tax = compute_ltcg_tax(total_ltcg)
    stcg_tax = compute_stcg_tax(total_stcg)

    return {
        "holdings": results,
        "total_ltcg": total_ltcg,
        "total_stcg": total_stcg,
        "ltcg_tax": ltcg_tax,
        "stcg_tax": stcg_tax,
        "total_tax": ltcg_tax + stcg_tax,
        "financial_year": financial_year,
    }
```

- [ ] **Step 4: Run tests, create files**

- [ ] **Step 5: Commit**

```bash
git add skills/tax_calculator/ tests/test_skills/test_tax_calculator.py
git commit -m "feat: add /tax-calculator skill — Indian capital gains tax with grandfathering"
```

---

### Task 19: `/smallcap-discovery` skill

**Files:**
- Create: `skills/smallcap_discovery/discovery.py`
- Create: `skills/smallcap_discovery/smallcap-discovery.md`
- Create: `tests/test_skills/test_smallcap_discovery.py`

- [ ] **Step 1: Write failing tests**

```python
# tests/test_skills/test_smallcap_discovery.py
import pytest


def test_piotroski_f_score():
    from skills.smallcap_discovery.discovery import compute_piotroski_score
    financials = {
        "roa": 0.08, "cfo": 0.10, "delta_roa": 0.01, "accruals": -0.02,
        "delta_leverage": -0.05, "delta_current_ratio": 0.1, "equity_dilution": False,
        "delta_gross_margin": 0.02, "delta_asset_turnover": 0.03,
    }
    score = compute_piotroski_score(financials)
    assert 0 <= score <= 9
    assert score >= 7  # All positive signals


def test_altman_z_score_emerging():
    from skills.smallcap_discovery.discovery import compute_altman_z_em
    z = compute_altman_z_em(
        working_capital=500, total_assets=2000,
        retained_earnings=300, ebit=250,
        book_equity=800, total_liabilities=1200,
    )
    assert z > 2.60  # Safe zone


def test_cash_flow_quality():
    from skills.smallcap_discovery.discovery import compute_cash_flow_quality
    assert compute_cash_flow_quality(cfo=90, net_income=100) == pytest.approx(0.9)
    assert compute_cash_flow_quality(cfo=0, net_income=0) == 0.0


def test_composite_discovery_score():
    from skills.smallcap_discovery.discovery import compute_discovery_score
    score = compute_discovery_score(quality=80, momentum=60, liquidity=70)
    # 80*0.6 + 60*0.25 + 70*0.15 = 48 + 15 + 10.5 = 73.5
    assert score == pytest.approx(73.5)
```

- [ ] **Step 2: Run tests, verify fail**

- [ ] **Step 3: Implement discovery.py**

```python
# skills/smallcap_discovery/discovery.py
"""Smallcap & Microcap Discovery — quality scoring for under-researched stocks."""

import pandas as pd
from typing import Any


def compute_piotroski_score(f: dict[str, Any]) -> int:
    """Compute Piotroski F-Score (0-9) with Ind-AS adjustments.

    Profitability (4): ROA>0, CFO>0, delta ROA>0, accruals<0
    Leverage (3): delta leverage<0, delta current ratio>0, no equity dilution
    Efficiency (2): delta gross margin>0, delta asset turnover>0
    """
    score = 0
    # Profitability
    if f.get("roa", 0) > 0: score += 1
    if f.get("cfo", 0) > 0: score += 1
    if f.get("delta_roa", 0) > 0: score += 1
    if f.get("accruals", 0) < 0: score += 1  # Accruals < 0 means cash > earnings
    # Leverage (Ind-AS 116 adjusted: exclude lease liabilities)
    if f.get("delta_leverage", 0) < 0: score += 1
    if f.get("delta_current_ratio", 0) > 0: score += 1
    if not f.get("equity_dilution", True): score += 1
    # Efficiency (total assets adjusted for ROU assets)
    if f.get("delta_gross_margin", 0) > 0: score += 1
    if f.get("delta_asset_turnover", 0) > 0: score += 1
    return score


def compute_altman_z_em(
    working_capital: float, total_assets: float,
    retained_earnings: float, ebit: float,
    book_equity: float, total_liabilities: float,
) -> float:
    """Compute Altman Z-Score Emerging Markets adaptation.

    Z'' = 3.25 + 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4
    """
    if total_assets == 0 or total_liabilities == 0:
        return 0.0
    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = book_equity / total_liabilities
    return 3.25 + 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4


def compute_cash_flow_quality(cfo: float, net_income: float) -> float:
    """Compute CFO/Net Income ratio as earnings quality indicator."""
    if net_income == 0:
        return 0.0
    return cfo / net_income


def compute_discovery_score(quality: float, momentum: float, liquidity: float) -> float:
    """Compute composite discovery score.
    Weights: quality 60%, momentum 25%, liquidity 15%.
    """
    return quality * 0.60 + momentum * 0.25 + liquidity * 0.15


def screen_stock(symbol: str, yf_fetcher: Any) -> dict[str, Any] | None:
    """Screen a single stock for quality metrics. Returns None if insufficient data."""
    try:
        info = yf_fetcher.get_info(symbol)
        if not info:
            return None

        mcap_cr = (info.get("marketCap", 0) or 0) / 10000000
        financials = yf_fetcher.get_financials(symbol)

        # Check data completeness (need 4+ quarters)
        income = financials.get("income_stmt", pd.DataFrame())
        if income.empty or len(income.columns) < 4:
            return None

        # Extract key metrics for scoring
        net_income = float(income.iloc[0, 0]) if not income.empty else 0
        total_assets = 1  # Fallback
        bs = financials.get("balance_sheet", pd.DataFrame())
        if not bs.empty:
            ta_row = bs.loc[bs.index.str.contains("Total Assets", case=False, na=False)]
            if not ta_row.empty:
                total_assets = float(ta_row.iloc[0, 0]) or 1

        roa = net_income / total_assets if total_assets else 0
        cfo = 0
        cf = financials.get("cashflow", pd.DataFrame())
        if not cf.empty:
            cfo_row = cf.loc[cf.index.str.contains("Operating Cash Flow", case=False, na=False)]
            if not cfo_row.empty:
                cfo = float(cfo_row.iloc[0, 0])

        # Compute scores
        f_score_inputs = {
            "roa": roa, "cfo": cfo / total_assets if total_assets else 0,
            "delta_roa": 0, "accruals": (cfo - net_income) / total_assets if total_assets else 0,
            "delta_leverage": 0, "delta_current_ratio": 0, "equity_dilution": False,
            "delta_gross_margin": 0, "delta_asset_turnover": 0,
        }
        f_score = compute_piotroski_score(f_score_inputs)
        cfq = compute_cash_flow_quality(cfo, net_income)

        # Price momentum
        hist = yf_fetcher.get_price_history(symbol, period="6mo")
        momentum = 0
        if not hist.empty and len(hist) > 1:
            momentum = ((hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1) * 100

        # ADTV for liquidity
        adtv = hist["Volume"].mean() * hist["Close"].mean() / 10000000 if not hist.empty else 0  # In lakhs

        return {
            "symbol": symbol,
            "market_cap_cr": round(mcap_cr, 1),
            "piotroski": f_score,
            "cash_flow_quality": round(cfq, 2),
            "momentum_6m": round(momentum, 2),
            "adtv_lakhs": round(adtv, 1),
            "sector": info.get("sector", ""),
        }
    except Exception:
        return None


def run_discovery(
    market_cap_min: float = 50,
    market_cap_max: float = 1000,
    symbols: list[str] | None = None,
    limit: int = 15,
) -> dict[str, Any]:
    """Run the smallcap discovery scan.

    Args:
        symbols: List of symbols to scan. If None, uses a default small-cap universe.
    """
    from core.data_sources import YFinanceFetcher
    import pandas as pd

    yf = YFinanceFetcher()

    # Default universe: known small-cap stocks (expandable)
    if symbols is None:
        symbols = [
            "ROUTE.NS", "CAMPUS.NS", "KAYNES.NS", "CDSL.NS", "CAMS.NS",
            "HAPPSTMNDS.NS", "AFFLE.NS", "CLEAN.NS", "OLECTRA.NS", "RATEGAIN.NS",
            "DOMS.NS", "JYOTICNC.NS", "NETWEB.NS", "KFINTECH.NS", "ZENTEC.NS",
        ]

    results = []
    for sym in symbols:
        stock = screen_stock(sym.replace(".NS", ""), yf)
        if stock is None:
            continue
        # Apply filters
        if not (market_cap_min <= stock["market_cap_cr"] <= market_cap_max):
            continue
        if stock["adtv_lakhs"] < 10:  # Liquidity filter: ADTV > Rs 10 lakh
            continue

        # Compute composite score
        quality = min(stock["piotroski"] / 9 * 100, 100)
        mom = min(max(stock["momentum_6m"], 0), 100)
        liq = min(stock["adtv_lakhs"] / 100 * 100, 100)
        stock["discovery_score"] = round(compute_discovery_score(quality, mom, liq), 1)
        results.append(stock)

    df = pd.DataFrame(results)
    if not df.empty:
        df = df.sort_values("discovery_score", ascending=False).head(limit)

    return {
        "data": df.reset_index(drop=True) if not df.empty else pd.DataFrame(),
        "filters_applied": {
            "market_cap_range": f"{market_cap_min}-{market_cap_max} Cr",
            "min_quarters": 4,
            "min_adtv_lakhs": 10,
        },
        "summary": f"Discovery scan complete. Found {len(df)} candidates from {len(symbols)} screened.",
    }
```

- [ ] **Step 4: Run tests, create files**

- [ ] **Step 5: Commit**

```bash
git add skills/smallcap_discovery/ tests/test_skills/test_smallcap_discovery.py
git commit -m "feat: add /smallcap-discovery skill — Piotroski, Altman Z, quality scoring"
```

---

## Phase 5: Skill .md Files & README

### Task 20: Create all 10 skill .md files

**Files:** Each skill directory gets a `.md` file following the template in spec section 5.

- [ ] **Step 1: Create remaining skill .md files**

Write `.md` files for all 10 skills following the template:
- `skills/nse_screener/nse-screener.md` (already done in Task 10)
- `skills/fii_dii_tracker/fii-dii-tracker.md`
- `skills/nse_options_chain/nse-options-chain.md`
- `skills/sebi_deal_scanner/sebi-deal-scanner.md`
- `skills/promoter_analyzer/promoter-analyzer.md`
- `skills/fo_strategy/fo-strategy.md`
- `skills/mf_flow_analyzer/mf-flow-analyzer.md`
- `skills/sector_rotation/sector-rotation.md`
- `skills/tax_calculator/tax-calculator.md`
- `skills/smallcap_discovery/smallcap-discovery.md`

Each `.md` follows the format in spec section 5 with: frontmatter (name, description), Purpose, Instructions, Parameters table, Example Usage.

- [ ] **Step 2: Create __init__.py for each skill directory**

```bash
for dir in nse_screener fii_dii_tracker nse_options_chain sebi_deal_scanner promoter_analyzer fo_strategy mf_flow_analyzer sector_rotation tax_calculator smallcap_discovery; do
  touch skills/$dir/__init__.py
done
touch skills/__init__.py
```

- [ ] **Step 3: Commit**

```bash
git add skills/
git commit -m "feat: add Claude Code skill definitions (.md) for all 10 skills"
```

---

### Task 21: README.md and LICENSE

**Files:**
- Create: `README.md`
- Create: `LICENSE`

- [ ] **Step 1: Write README.md**

Comprehensive README with:
- Project overview and badge icons
- Table of all 10 skills with descriptions
- Architecture diagram (mermaid)
- Installation steps (3-step from spec)
- Usage examples
- Configuration section
- Contributing guidelines
- License

- [ ] **Step 2: Add MIT LICENSE**

- [ ] **Step 3: Run full test suite**

Run: `pytest tests/ -v --tb=short`
Expected: All tests PASS

- [ ] **Step 4: Commit**

```bash
git add README.md LICENSE
git commit -m "docs: add comprehensive README and MIT license"
```

---

## Phase 6: Push to GitHub

### Task 22: Push to remote repository

- [ ] **Step 1: Add remote and push**

```bash
git remote add origin https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS.git
git push -u origin main
```

- [ ] **Step 2: Verify repo on GitHub**

Check that all files are visible at https://github.com/SuminPillai/NSE-STOCK-ANALYSIS-CLAUDE-SKILLS

---

## Task Dependencies

```
Task 1 (scaffold) → Task 2 (config)
Task 2 → Task 3 (constants)
Task 3 → Tasks 4, 5 (cache, auth — parallel)
Tasks 3, 4, 5 → Tasks 6, 7, 8 (data sources, formatters, exporters — parallel, no interdependency)
Tasks 6, 7, 8 → Task 9 (core init)
Task 9 → Tasks 10-19 (all 10 skills — parallel)
Tasks 10-19 → Task 20 (skill .md files)
Task 20 → Task 21 (README) → Task 22 (push)
```

**Parallelizable:**
- Tasks 4 + 5 (cache, auth) — independent, can run in parallel
- Tasks 6 + 7 + 8 (data sources, formatters, exporters) — independent, can run in parallel
- Tasks 10-19 (all 10 skills) — independent, can be dispatched to parallel subagents
