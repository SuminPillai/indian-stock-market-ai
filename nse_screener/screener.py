"""NSE Stock Screener — multi-factor screening with India-specific filters."""
import pandas as pd
import numpy as np
from typing import Any
from core.data_sources import YFinanceFetcher
from core.formatters import format_table, format_crores, heatmap_color, sparkline
from core.exporters import export_csv, export_json, export_python

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
    roe_score = min(stock.get("roe", 0) / 0.30, 1.0) * 25
    roce_score = min(stock.get("roce", 0) / 0.25, 1.0) * 25
    pe_score = (1 - stock.get("pe_percentile", 0.5)) * 20
    de = stock.get("debt_equity", 100)
    de_score = max(0, (1 - de / 200)) * 15
    pledge = stock.get("pledge_pct", 0)
    pledge_score = max(0, (1 - pledge / 50)) * 15
    base = roe_score + roce_score + pe_score + de_score + pledge_score
    fii_trend = stock.get("fii_trend", "stable")
    if fii_trend == "increasing": base += 5
    elif fii_trend == "decreasing": base -= 5
    return max(0, min(100, base))

def apply_filters(df: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
    result = df.copy()
    if "pe_max" in filters: result = result[result["pe"] <= filters["pe_max"]]
    if "pe_min" in filters: result = result[result["pe"] >= filters["pe_min"]]
    if "roe_min" in filters: result = result[result["roe"] >= filters["roe_min"]]
    if "market_cap_min" in filters: result = result[result["market_cap_cr"] >= filters["market_cap_min"]]
    if "market_cap_max" in filters: result = result[result["market_cap_cr"] <= filters["market_cap_max"]]
    return result

def run_screener(symbols=None, sector=None, filters=None, sort_by="composite_score", limit=20):
    if symbols is None: symbols = NIFTY_50
    fetcher = YFinanceFetcher()
    records = []
    for sym in symbols:
        try:
            info = fetcher.get_info(sym)
            if not info: continue
            record = {
                "symbol": sym,
                "price": info.get("currentPrice", info.get("regularMarketPrice", 0)),
                "pe": info.get("trailingPE", 0) or 0,
                "pb": info.get("priceToBook", 0) or 0,
                "roe": info.get("returnOnEquity", 0) or 0,
                "roce": info.get("returnOnAssets", 0) or 0,
                "debt_equity": info.get("debtToEquity", 0) or 0,
                "market_cap_cr": (info.get("marketCap", 0) or 0) / 10000000,
                "sector": info.get("sector", ""),
                "dividend_yield": info.get("dividendYield", 0) or 0,
            }
            records.append(record)
        except Exception: continue
    if not records: return pd.DataFrame()
    df = pd.DataFrame(records)
    if sector: df = df[df["sector"].str.contains(sector, case=False, na=False)]
    if filters: df = apply_filters(df, filters)
    if len(df) > 0 and "pe" in df.columns: df["pe_percentile"] = df["pe"].rank(pct=True)
    else: df["pe_percentile"] = 0.5
    df["composite_score"] = df.apply(lambda row: compute_composite_score({
        "roe": row["roe"], "roce": row["roce"],
        "pe_percentile": row.get("pe_percentile", 0.5),
        "debt_equity": row["debt_equity"], "pledge_pct": 0, "fii_trend": "stable",
    }), axis=1)
    df = df.sort_values(sort_by, ascending=False).head(limit)
    return df.reset_index(drop=True)
