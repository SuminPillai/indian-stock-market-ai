# tests/test_core/test_constants.py
import pytest
from datetime import date


def test_load_holidays():
    from core.constants import load_holidays
    holidays = load_holidays()
    assert isinstance(holidays, list)
    assert all(isinstance(h, date) for h in holidays)
    assert date(2025, 8, 15) in holidays  # Independence Day


def test_load_lot_sizes():
    from core.constants import load_lot_sizes
    lots = load_lot_sizes()
    assert lots["NIFTY"] == 75
    assert lots["BANKNIFTY"] == 30
    assert lots["RELIANCE"] == 250


def test_load_tax_rules():
    from core.constants import load_tax_rules
    rules = load_tax_rules()
    assert rules["equity_listed"]["stcg_rate"] == 0.20
    assert rules["equity_listed"]["ltcg_rate"] == 0.125
    assert rules["equity_listed"]["ltcg_exemption_per_fy"] == 125000


def test_load_stt_rates():
    from core.constants import load_stt_rates
    rates = load_stt_rates()
    assert rates["options"]["exercise"] == 0.00125


def test_is_trading_day():
    from core.constants import is_trading_day
    # Independence Day is a holiday
    assert is_trading_day(date(2025, 8, 15)) is False
    # Saturday
    assert is_trading_day(date(2025, 8, 16)) is False
    # Regular Monday (not a holiday)
    assert is_trading_day(date(2025, 8, 18)) is True


def test_get_current_fy():
    from core.constants import get_current_fy
    # March 2026 is still FY 2025-26
    assert get_current_fy(date(2026, 3, 26)) == "FY2025-26"
    # April 2026 starts FY 2026-27
    assert get_current_fy(date(2026, 4, 1)) == "FY2026-27"


# Static constants
def test_grandfathering_date():
    from core.constants import GRANDFATHERING_DATE
    assert GRANDFATHERING_DATE == date(2018, 1, 31)


def test_nifty_sectors():
    from core.constants import NIFTY_SECTORS
    assert "IT" in NIFTY_SECTORS
    assert "Bank" in NIFTY_SECTORS
    assert "Pharma" in NIFTY_SECTORS
