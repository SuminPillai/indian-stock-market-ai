"""Promoter Holding & Pledge Analyzer."""
import pandas as pd
from typing import Any
from core.data_sources import BSEFetcher, YFinanceFetcher
from core.formatters import format_table, sparkline, format_percent

def compute_qoq_changes(df):
    result = df.copy()
    pct_cols = [c for c in df.columns if c.endswith("_pct")]
    for col in pct_cols:
        result[f"{col}_change"] = result[col].diff()
    return result

def detect_red_flags(holdings):
    flags = []
    if "pledge_pct" in holdings.columns:
        latest_pledge = holdings["pledge_pct"].iloc[-1]
        if latest_pledge > 40:
            flags.append(f"RED FLAG: Pledge at {latest_pledge:.1f}% — dangerously high (>40%)")
        if len(holdings) >= 3:
            recent = holdings["pledge_pct"].iloc[-3:]
            if all(recent.diff().dropna() > 0):
                flags.append("RED FLAG: Pledge increasing for 3+ consecutive quarters")
    if "promoter_pct" in holdings.columns and len(holdings) >= 2:
        changes = holdings["promoter_pct"].diff().dropna()
        if all(changes.iloc[-3:] < 0) if len(changes) >= 3 else False:
            flags.append("RED FLAG: Promoter stake declining for 3+ quarters")
        if "pledge_pct" in holdings.columns:
            if holdings["promoter_pct"].iloc[-1] < holdings["promoter_pct"].iloc[0]:
                if holdings["pledge_pct"].iloc[-1] > holdings["pledge_pct"].iloc[0]:
                    flags.append("DOUBLE RED FLAG: Promoter declining + pledge increasing")
    return flags

def detect_green_flags(holdings):
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

def run_promoter_analysis(symbol, quarters=8):
    bse = BSEFetcher()
    yf = YFinanceFetcher()
    info = yf.get_info(symbol)
    stock_name = info.get("shortName", symbol) if info else symbol
    shareholding = bse.get_shareholding_pattern(symbol)
    if shareholding is None: return {"error": f"Could not fetch shareholding data for {symbol}"}
    df = pd.DataFrame(shareholding) if isinstance(shareholding, list) else pd.DataFrame()
    if df.empty: return {"error": "No shareholding data available"}
    df = df.tail(quarters)
    df = compute_qoq_changes(df)
    red_flags = detect_red_flags(df)
    green_flags = detect_green_flags(df)
    return {"symbol": symbol, "name": stock_name, "data": df, "red_flags": red_flags, "green_flags": green_flags}
