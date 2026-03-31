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

    if "scheme_name" in navs.columns:
        navs["mf_category"] = navs["scheme_name"].apply(classify_category)

    if category != "all":
        navs = navs[navs["mf_category"] == category]

    return {
        "data": navs,
        "summary": f"Analyzed {len(navs)} schemes across categories.",
        "flow_summary": compute_flow_summary(navs) if "net_flow_cr" in navs.columns else {},
    }
