"""FII/DII Flow Tracker — institutional money flow analysis."""
import pandas as pd
from typing import Any
from core.data_sources import NSESessionFetcher, YFinanceFetcher
from core.formatters import format_table, sparkline, heatmap_color, format_crores

def classify_divergence(fii_net: float, dii_net: float) -> str:
    if fii_net < 0 and dii_net > 0: return "institutional_rotation"
    elif fii_net < 0 and dii_net < 0: return "risk_off"
    elif fii_net > 0 and dii_net > 0: return "broad_buying"
    elif fii_net > 0 and dii_net < 0: return "fii_led_rally"
    return "neutral"

DIVERGENCE_SIGNALS = {
    "institutional_rotation": "FII selling + DII buying = Institutional rotation (historically mid-term bullish)",
    "risk_off": "Both selling = Risk-off environment (bearish signal)",
    "broad_buying": "Both buying = Broad rally fuel (bullish)",
    "fii_led_rally": "FII buying + DII selling = FII-led rally (watch for reversal)",
    "neutral": "Mixed signals — no clear directional bias",
}

def compute_rolling_averages(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["fii_net_5d_avg"] = result["fii_net"].rolling(5).mean()
    result["fii_net_20d_avg"] = result["fii_net"].rolling(20).mean()
    result["dii_net_5d_avg"] = result["dii_net"].rolling(5).mean()
    result["dii_net_20d_avg"] = result["dii_net"].rolling(20).mean()
    return result

def format_flow_summary(fii_total, dii_total, nifty_change, period):
    divergence = classify_divergence(fii_total, dii_total)
    signal = DIVERGENCE_SIGNALS.get(divergence, "")
    return (
        f"**FII/DII Flow Summary ({period})**\n\n"
        f"- FII Net: {fii_total:+,.0f} Cr ({'Bought' if fii_total > 0 else 'Sold'})\n"
        f"- DII Net: {dii_total:+,.0f} Cr ({'Bought' if dii_total > 0 else 'Sold'})\n"
        f"- Nifty Change: {nifty_change:+.2f}%\n\n"
        f"**Signal:** {signal}\n"
    )

def run_tracker(period="1m", segment="both", correlation=True):
    nse = NSESessionFetcher()
    data = nse.get_fii_dii_data()
    if data is None:
        return {"data": pd.DataFrame(), "summary": "NSE data unavailable.", "divergence": "unknown"}
    records = []
    if isinstance(data, list):
        for entry in data:
            records.append({"category": entry.get("category", ""), "buy_value": float(entry.get("buyValue", 0)), "sell_value": float(entry.get("sellValue", 0)), "net_value": float(entry.get("netValue", 0))})
    df = pd.DataFrame(records) if records else pd.DataFrame()
    fii_total = sum(r["net_value"] for r in records if "fpi" in r.get("category", "").lower() or "fii" in r.get("category", "").lower())
    dii_total = sum(r["net_value"] for r in records if "dii" in r.get("category", "").lower())
    nifty_change = 0.0
    if correlation:
        yf_fetcher = YFinanceFetcher()
        nifty_hist = yf_fetcher.get_price_history("^NSEI", period="1mo")
        if not nifty_hist.empty:
            nifty_change = ((nifty_hist["Close"].iloc[-1] / nifty_hist["Close"].iloc[0]) - 1) * 100
    divergence = classify_divergence(fii_total, dii_total)
    summary = format_flow_summary(fii_total, dii_total, nifty_change, period)
    return {"data": df, "summary": summary, "divergence": divergence}
