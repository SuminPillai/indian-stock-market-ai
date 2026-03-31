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
