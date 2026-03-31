# tests/test_skills/test_mf_flow_analyzer.py
import pytest
import pandas as pd


def test_classify_category():
    from skills.mf_flow_analyzer.mf_flows import classify_category
    assert classify_category("HDFC Large Cap Fund") == "large_cap"
    assert classify_category("SBI Small Cap Fund") == "small_cap"
    assert classify_category("ICICI Prudential Balanced Advantage") == "hybrid"


def test_compute_flow_summary():
    from skills.mf_flow_analyzer.mf_flows import compute_flow_summary
    flows = pd.DataFrame({
        "category": ["equity", "equity", "debt"],
        "net_flow_cr": [5000, 3000, -2000],
        "month": ["2026-01", "2026-02", "2026-01"],
    })
    summary = compute_flow_summary(flows)
    assert summary["equity_total"] == 8000
    assert summary["debt_total"] == -2000
