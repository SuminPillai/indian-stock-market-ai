import pytest
import pandas as pd

def test_compute_pcr():
    from skills.nse_options_chain.options_chain import compute_pcr
    assert compute_pcr(put_oi=500000, call_oi=400000) == pytest.approx(1.25)
    assert compute_pcr(put_oi=0, call_oi=100) == 0.0

def test_compute_max_pain():
    from skills.nse_options_chain.options_chain import compute_max_pain
    strikes = [24000, 24100, 24200, 24300, 24400]
    call_oi = [50000, 40000, 30000, 20000, 10000]
    put_oi = [10000, 20000, 30000, 40000, 50000]
    max_pain = compute_max_pain(strikes, call_oi, put_oi)
    assert max_pain in strikes

def test_classify_oi_buildup():
    from skills.nse_options_chain.options_chain import classify_oi_buildup
    assert classify_oi_buildup(price_change=50, oi_change=1000) == "long_buildup"
    assert classify_oi_buildup(price_change=-50, oi_change=1000) == "short_buildup"
    assert classify_oi_buildup(price_change=50, oi_change=-1000) == "short_covering"
    assert classify_oi_buildup(price_change=-50, oi_change=-1000) == "long_unwinding"
