# tests/test_skills/test_tax_calculator.py
import pytest
from datetime import date


def test_classify_holding_stcg():
    from skills.tax_calculator.tax_calc import classify_holding
    result = classify_holding(buy_date=date(2026, 1, 1), sell_date=date(2026, 6, 1))
    assert result == "STCG"


def test_classify_holding_ltcg():
    from skills.tax_calculator.tax_calc import classify_holding
    result = classify_holding(buy_date=date(2025, 1, 1), sell_date=date(2026, 3, 1))
    assert result == "LTCG"


def test_grandfathered_cost():
    from skills.tax_calculator.tax_calc import compute_grandfathered_cost
    # Bought at 500, FMV on 31/01/2018 was 800, selling at 1000
    cost = compute_grandfathered_cost(actual_cost=500, fmv_jan2018=800, sell_price=1000)
    assert cost == 800  # max(500, 800) = 800, capped at sell_price 1000 -> 800

    # Bought at 900, FMV was 800, selling at 1000
    cost = compute_grandfathered_cost(actual_cost=900, fmv_jan2018=800, sell_price=1000)
    assert cost == 900  # max(900, 800) = 900

    # FMV > sell price -> cost = sell_price (no loss allowed via grandfathering)
    cost = compute_grandfathered_cost(actual_cost=500, fmv_jan2018=1200, sell_price=1000)
    assert cost == 1000


def test_compute_ltcg_tax():
    from skills.tax_calculator.tax_calc import compute_ltcg_tax
    # Gain of 2,25,000 -> exempt 1,25,000 -> taxable 1,00,000 -> tax = 12,500
    tax = compute_ltcg_tax(total_ltcg=225000)
    assert tax == pytest.approx(12500)


def test_compute_ltcg_tax_within_exemption():
    from skills.tax_calculator.tax_calc import compute_ltcg_tax
    tax = compute_ltcg_tax(total_ltcg=100000)
    assert tax == 0


def test_compute_stcg_tax():
    from skills.tax_calculator.tax_calc import compute_stcg_tax
    tax = compute_stcg_tax(total_stcg=100000)
    assert tax == pytest.approx(20000)


def test_tax_loss_harvesting_suggestion():
    from skills.tax_calculator.tax_calc import suggest_tax_loss_harvest
    holdings = [
        {"symbol": "A", "unrealized_gain": 50000},
        {"symbol": "B", "unrealized_gain": -30000},
        {"symbol": "C", "unrealized_gain": -10000},
    ]
    suggestions = suggest_tax_loss_harvest(holdings, realized_gain=50000)
    assert len(suggestions) > 0
    assert any(s["symbol"] == "B" for s in suggestions)
