# tests/test_skills/test_sector_rotation.py
import pytest
import pandas as pd


def test_compute_relative_strength():
    from skills.sector_rotation.rotation import compute_relative_strength
    sector = pd.Series([100, 102, 105, 108, 112])
    benchmark = pd.Series([100, 101, 102, 103, 104])
    rs = compute_relative_strength(sector, benchmark)
    assert rs > 1.0  # Sector outperforming


def test_classify_sector_cycle():
    from skills.sector_rotation.rotation import classify_sector_cycle
    assert classify_sector_cycle(momentum_1m=15, momentum_3m=10, momentum_6m=5) == "early_cycle"
    assert classify_sector_cycle(momentum_1m=-2, momentum_3m=-5, momentum_6m=10) == "late_cycle"


def test_get_macro_triggers():
    from skills.sector_rotation.rotation import get_macro_triggers
    triggers = get_macro_triggers("IT")
    assert any("USD/INR" in t for t in triggers)
