import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_yfinance_info():
    return {
        "RELIANCE": {"trailingPE": 25.0, "priceToBook": 2.5, "returnOnEquity": 0.15,
                      "debtToEquity": 40.0, "marketCap": 1700000000000, "sector": "Energy"},
        "TCS": {"trailingPE": 30.0, "priceToBook": 12.0, "returnOnEquity": 0.45,
                "debtToEquity": 5.0, "marketCap": 1300000000000, "sector": "Technology"},
        "INFY": {"trailingPE": 28.0, "priceToBook": 8.0, "returnOnEquity": 0.32,
                 "debtToEquity": 10.0, "marketCap": 600000000000, "sector": "Technology"},
    }

def test_compute_composite_score():
    from skills.nse_screener.screener import compute_composite_score
    stock = {
        "roe": 0.30, "roce": 0.25, "pe_percentile": 0.7,
        "debt_equity": 20.0, "pledge_pct": 0.0, "fii_trend": "increasing",
    }
    score = compute_composite_score(stock)
    assert 0 <= score <= 100

def test_apply_filters():
    from skills.nse_screener.screener import apply_filters
    stocks = pd.DataFrame({
        "symbol": ["A", "B", "C"],
        "pe": [15, 30, 50],
        "roe": [0.20, 0.10, 0.35],
        "market_cap_cr": [50000, 10000, 500],
    })
    filters = {"pe_max": 35, "roe_min": 0.15}
    result = apply_filters(stocks, filters)
    assert len(result) == 1
    assert result.iloc[0]["symbol"] == "A"

def test_screener_run_returns_dataframe():
    from skills.nse_screener.screener import run_screener
    with patch("skills.nse_screener.screener.YFinanceFetcher") as MockFetcher:
        mock = MockFetcher.return_value
        mock.get_info.side_effect = lambda s: {
            "trailingPE": 20, "returnOnEquity": 0.25, "returnOnAssets": 0.15,
            "debtToEquity": 30, "marketCap": 500000000000, "sector": "IT",
            "currentPrice": 1500,
        }
        result = run_screener(symbols=["INFY", "TCS"], limit=5)
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 5
