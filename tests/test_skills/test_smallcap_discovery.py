# tests/test_skills/test_smallcap_discovery.py
import pytest


def test_piotroski_f_score():
    from skills.smallcap_discovery.discovery import compute_piotroski_score
    financials = {
        "roa": 0.08, "cfo": 0.10, "delta_roa": 0.01, "accruals": -0.02,
        "delta_leverage": -0.05, "delta_current_ratio": 0.1, "equity_dilution": False,
        "delta_gross_margin": 0.02, "delta_asset_turnover": 0.03,
    }
    score = compute_piotroski_score(financials)
    assert 0 <= score <= 9
    assert score >= 7  # All positive signals


def test_altman_z_score_emerging():
    from skills.smallcap_discovery.discovery import compute_altman_z_em
    z = compute_altman_z_em(
        working_capital=500, total_assets=2000,
        retained_earnings=300, ebit=250,
        book_equity=800, total_liabilities=1200,
    )
    assert z > 2.60  # Safe zone


def test_cash_flow_quality():
    from skills.smallcap_discovery.discovery import compute_cash_flow_quality
    assert compute_cash_flow_quality(cfo=90, net_income=100) == pytest.approx(0.9)
    assert compute_cash_flow_quality(cfo=0, net_income=0) == 0.0


def test_composite_discovery_score():
    from skills.smallcap_discovery.discovery import compute_discovery_score
    score = compute_discovery_score(quality=80, momentum=60, liquidity=70)
    # 80*0.6 + 60*0.25 + 70*0.15 = 48 + 15 + 10.5 = 73.5
    assert score == pytest.approx(73.5)
