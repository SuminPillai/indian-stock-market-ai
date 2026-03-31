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
            return "early_cycle"
        return "mid_cycle"
    elif momentum_6m > 0 and momentum_1m < 0:
        return "late_cycle"
    elif momentum_1m < 0 and momentum_3m < 0 and momentum_6m < 0:
        return "defensive"
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

    bench_symbol = "^NSEI" if benchmark == "nifty_50" else "^CRSLDX"
    bench_data = yf.get_price_history(bench_symbol, period=period)

    results = []
    for sector_name, index_name in NIFTY_SECTORAL_INDICES.items():
        yf_symbol = index_name.replace(" ", "").upper()
        sector_data = yf.get_price_history(f"^{yf_symbol}", period=period)

        if sector_data.empty or bench_data.empty:
            continue

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
