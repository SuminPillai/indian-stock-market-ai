import pytest
import pandas as pd

def test_detect_red_flags():
    from skills.promoter_analyzer.promoter import detect_red_flags
    holdings = pd.DataFrame({
        "quarter": ["Q1", "Q2", "Q3", "Q4"],
        "promoter_pct": [60, 58, 55, 52],
        "pledge_pct": [10, 15, 22, 45],
    })
    flags = detect_red_flags(holdings)
    assert any("pledge" in f.lower() for f in flags)
    assert any("declining" in f.lower() or "decreasing" in f.lower() for f in flags)

def test_detect_green_flags():
    from skills.promoter_analyzer.promoter import detect_green_flags
    holdings = pd.DataFrame({
        "quarter": ["Q1", "Q2", "Q3", "Q4"],
        "promoter_pct": [50, 52, 54, 56],
        "pledge_pct": [20, 15, 10, 5],
    })
    flags = detect_green_flags(holdings)
    assert any("increasing" in f.lower() for f in flags)
    assert any("pledge" in f.lower() and "reduc" in f.lower() for f in flags)

def test_compute_qoq_changes():
    from skills.promoter_analyzer.promoter import compute_qoq_changes
    holdings = pd.DataFrame({
        "promoter_pct": [60, 58, 55],
        "fii_pct": [20, 22, 25],
    })
    result = compute_qoq_changes(holdings)
    assert "promoter_pct_change" in result.columns
    assert result["promoter_pct_change"].iloc[1] == pytest.approx(-2.0)
