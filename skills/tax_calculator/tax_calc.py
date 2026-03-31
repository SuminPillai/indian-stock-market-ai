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

        if sell_price == "current":
            info = yf.get_info(symbol)
            current = info.get("currentPrice", buy_price) if info else buy_price
        else:
            current = float(sell_price)

        today = date.today()
        classification = classify_holding(buy_date, today)

        effective_cost = buy_price
        if buy_date <= GRANDFATHERING_DATE and classification == "LTCG":
            hist = yf.get_price_history(symbol, period="max")
            fmv = buy_price
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
