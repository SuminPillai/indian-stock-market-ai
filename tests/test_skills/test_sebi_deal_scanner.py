import pytest
import pandas as pd

def test_classify_entity():
    from skills.sebi_deal_scanner.deal_scanner import classify_entity
    assert classify_entity("GOLDMAN SACHS") == "FII"
    assert classify_entity("LIC OF INDIA") == "DII"
    assert classify_entity("MUKESH AMBANI") == "Promoter/HNI"
    assert classify_entity("RANDOM PERSON") == "Unknown"

def test_detect_patterns():
    from skills.sebi_deal_scanner.deal_scanner import detect_patterns
    deals = pd.DataFrame({
        "symbol": ["RELIANCE", "RELIANCE", "TCS"],
        "buyer": ["ENTITY A", "ENTITY A", "ENTITY B"],
        "value_cr": [10, 15, 5],
        "date": ["2026-03-20", "2026-03-21", "2026-03-22"],
    })
    patterns = detect_patterns(deals)
    assert any("repeated" in p.lower() for p in patterns)

def test_compute_liquidity_impact():
    from skills.sebi_deal_scanner.deal_scanner import compute_liquidity_impact
    assert compute_liquidity_impact(deal_value_cr=50, adtv_cr=100) == pytest.approx(50.0)
    assert compute_liquidity_impact(deal_value_cr=50, adtv_cr=0) == 0.0
