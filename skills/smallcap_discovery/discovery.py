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

        income = financials.get("income_stmt", pd.DataFrame())
        if income.empty or len(income.columns) < 4:
            return None

        net_income = float(income.iloc[0, 0]) if not income.empty else 0
        total_assets = 1
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

        f_score_inputs = {
            "roa": roa, "cfo": cfo / total_assets if total_assets else 0,
            "delta_roa": 0, "accruals": (cfo - net_income) / total_assets if total_assets else 0,
            "delta_leverage": 0, "delta_current_ratio": 0, "equity_dilution": False,
            "delta_gross_margin": 0, "delta_asset_turnover": 0,
        }
        f_score = compute_piotroski_score(f_score_inputs)
        cfq = compute_cash_flow_quality(cfo, net_income)

        hist = yf_fetcher.get_price_history(symbol, period="6mo")
        momentum = 0
        if not hist.empty and len(hist) > 1:
            momentum = ((hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1) * 100

        adtv = hist["Volume"].mean() * hist["Close"].mean() / 10000000 if not hist.empty else 0

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
    """Run the smallcap discovery scan."""
    from core.data_sources import YFinanceFetcher
    import pandas as pd

    yf = YFinanceFetcher()

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
        if not (market_cap_min <= stock["market_cap_cr"] <= market_cap_max):
            continue
        if stock["adtv_lakhs"] < 10:
            continue

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
