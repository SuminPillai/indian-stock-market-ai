# tests/test_core/test_data_sources.py
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


def test_yfinance_fetcher_appends_ns_suffix():
    from core.data_sources import YFinanceFetcher
    fetcher = YFinanceFetcher()
    assert fetcher._normalize_symbol("RELIANCE") == "RELIANCE.NS"
    assert fetcher._normalize_symbol("RELIANCE.NS") == "RELIANCE.NS"
    assert fetcher._normalize_symbol("RELIANCE.BO") == "RELIANCE.BO"


def test_yfinance_fetcher_get_price_history_mocked():
    from core.data_sources import YFinanceFetcher
    fetcher = YFinanceFetcher()
    mock_df = pd.DataFrame({"Close": [2500, 2510, 2520]}, index=pd.date_range("2026-01-01", periods=3))
    with patch("yfinance.Ticker") as MockTicker:
        MockTicker.return_value.history.return_value = mock_df
        df = fetcher.get_price_history("RELIANCE", period="5d")
    assert isinstance(df, pd.DataFrame)
    assert "Close" in df.columns
    assert len(df) == 3


def test_yfinance_fetcher_get_info_mocked():
    from core.data_sources import YFinanceFetcher
    fetcher = YFinanceFetcher()
    mock_info = {"marketCap": 1700000000000, "trailingPE": 25.0, "sector": "Energy"}
    with patch("yfinance.Ticker") as MockTicker:
        MockTicker.return_value.info = mock_info
        info = fetcher.get_info("RELIANCE")
    assert info["marketCap"] == 1700000000000


def test_nse_session_fetcher_init():
    from core.data_sources import NSESessionFetcher
    fetcher = NSESessionFetcher()
    assert fetcher.base_url == "https://www.nseindia.com"
    assert fetcher._rate_limit == 3


def test_nse_session_fetcher_has_rotating_ua():
    from core.data_sources import NSESessionFetcher
    fetcher = NSESessionFetcher()
    assert len(fetcher._user_agents) >= 3


def test_base_fetcher_interface():
    from core.data_sources import BaseFetcher
    with pytest.raises(TypeError):
        BaseFetcher()


def test_sebi_fetcher_exists():
    from core.data_sources import SEBIFetcher
    fetcher = SEBIFetcher()
    assert fetcher.name() == "sebi"
