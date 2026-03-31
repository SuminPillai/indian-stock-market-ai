import pytest
import pandas as pd

def test_classify_divergence():
    from skills.fii_dii_tracker.tracker import classify_divergence
    assert classify_divergence(fii_net=-500, dii_net=600) == "institutional_rotation"
    assert classify_divergence(fii_net=-500, dii_net=-300) == "risk_off"
    assert classify_divergence(fii_net=500, dii_net=300) == "broad_buying"
    assert classify_divergence(fii_net=500, dii_net=-100) == "fii_led_rally"

def test_compute_rolling_averages():
    from skills.fii_dii_tracker.tracker import compute_rolling_averages
    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=25, freq="B"),
        "fii_net": list(range(25)),
        "dii_net": list(range(25, 0, -1)),
    })
    result = compute_rolling_averages(df)
    assert "fii_net_5d_avg" in result.columns
    assert "fii_net_20d_avg" in result.columns
    assert "dii_net_5d_avg" in result.columns

def test_format_flow_summary():
    from skills.fii_dii_tracker.tracker import format_flow_summary
    summary = format_flow_summary(fii_total=-5000, dii_total=6000, nifty_change=2.5, period="1m")
    assert "FII" in summary
    assert "DII" in summary
