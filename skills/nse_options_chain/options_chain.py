"""NSE Options Chain Analyzer — PCR, max pain, OI buildup, IV skew."""
import pandas as pd
import numpy as np
from typing import Any
from core.data_sources import NSESessionFetcher
from core.constants import load_lot_sizes
from core.formatters import format_table, heatmap_color

def compute_pcr(put_oi: int, call_oi: int) -> float:
    if call_oi == 0: return 0.0
    return put_oi / call_oi

def compute_max_pain(strikes, call_oi, put_oi):
    min_pain = float("inf")
    max_pain_strike = strikes[0]
    for i, strike in enumerate(strikes):
        total_pain = 0
        for j, s in enumerate(strikes):
            if s < strike: total_pain += put_oi[j] * (strike - s)
            elif s > strike: total_pain += call_oi[j] * (s - strike)
        if total_pain < min_pain:
            min_pain = total_pain
            max_pain_strike = strike
    return max_pain_strike

def classify_oi_buildup(price_change, oi_change):
    if price_change > 0 and oi_change > 0: return "long_buildup"
    elif price_change < 0 and oi_change > 0: return "short_buildup"
    elif price_change > 0 and oi_change < 0: return "short_covering"
    elif price_change < 0 and oi_change < 0: return "long_unwinding"
    return "neutral"

OI_BUILDUP_LABELS = {
    "long_buildup": "Long Buildup (Bullish)",
    "short_buildup": "Short Buildup (Bearish)",
    "short_covering": "Short Covering (Bullish, weak)",
    "long_unwinding": "Long Unwinding (Bearish, weak)",
    "neutral": "Neutral",
}

def parse_nse_options_data(raw_data):
    if not raw_data or "records" not in raw_data: return pd.DataFrame()
    records = raw_data["records"].get("data", [])
    parsed = []
    for record in records:
        row = {"strikePrice": record.get("strikePrice", 0)}
        if "CE" in record:
            ce = record["CE"]
            row.update({"ce_oi": ce.get("openInterest", 0), "ce_change_oi": ce.get("changeinOpenInterest", 0), "ce_volume": ce.get("totalTradedVolume", 0), "ce_iv": ce.get("impliedVolatility", 0), "ce_ltp": ce.get("lastPrice", 0)})
        if "PE" in record:
            pe = record["PE"]
            row.update({"pe_oi": pe.get("openInterest", 0), "pe_change_oi": pe.get("changeinOpenInterest", 0), "pe_volume": pe.get("totalTradedVolume", 0), "pe_iv": pe.get("impliedVolatility", 0), "pe_ltp": pe.get("lastPrice", 0)})
        parsed.append(row)
    return pd.DataFrame(parsed)

def run_options_analysis(symbol="NIFTY", strikes=10, analysis="all"):
    nse = NSESessionFetcher()
    raw = nse.get_options_chain(symbol)
    if raw is None: return {"error": "Could not fetch options chain from NSE."}
    df = parse_nse_options_data(raw)
    if df.empty: return {"error": "No options data available."}
    spot = raw.get("records", {}).get("underlyingValue", 0)
    df["dist_from_atm"] = abs(df["strikePrice"] - spot)
    df = df.nsmallest(strikes * 2, "dist_from_atm").sort_values("strikePrice")
    results = {"spot": spot, "data": df, "symbol": symbol}
    total_put_oi = df.get("pe_oi", pd.Series(dtype=int)).sum()
    total_call_oi = df.get("ce_oi", pd.Series(dtype=int)).sum()
    results["pcr"] = compute_pcr(total_put_oi, total_call_oi)
    results["max_pain"] = compute_max_pain(df["strikePrice"].tolist(), df.get("ce_oi", pd.Series(0, index=df.index)).tolist(), df.get("pe_oi", pd.Series(0, index=df.index)).tolist())
    if "pe_oi" in df.columns: results["support"] = df.loc[df["pe_oi"].idxmax(), "strikePrice"]
    if "ce_oi" in df.columns: results["resistance"] = df.loc[df["ce_oi"].idxmax(), "strikePrice"]
    return results
