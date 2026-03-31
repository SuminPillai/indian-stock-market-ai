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
