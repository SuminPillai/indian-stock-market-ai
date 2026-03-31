# tests/test_core/test_formatters.py
import pytest
import pandas as pd


def test_format_table_markdown():
    from core.formatters import format_table
    df = pd.DataFrame({"Symbol": ["RELIANCE", "TCS"], "Price": [2500.0, 3800.0]})
    result = format_table(df, fmt="markdown")
    assert "RELIANCE" in result
    assert "TCS" in result
    assert "|" in result


def test_format_table_rich():
    from core.formatters import format_table
    df = pd.DataFrame({"Symbol": ["RELIANCE"], "Price": [2500.0]})
    result = format_table(df, fmt="rich")
    assert "RELIANCE" in result


def test_sparkline():
    from core.formatters import sparkline
    data = [1, 3, 5, 7, 5, 3, 1]
    result = sparkline(data)
    assert isinstance(result, str)
    assert len(result) == 7


def test_sparkline_empty():
    from core.formatters import sparkline
    assert sparkline([]) == ""


def test_heatmap_color():
    from core.formatters import heatmap_color
    assert "green" in heatmap_color(100).lower() or "\033[32m" in heatmap_color(100)
    assert "red" in heatmap_color(-100).lower() or "\033[31m" in heatmap_color(-100)


def test_format_currency_inr():
    from core.formatters import format_inr
    assert format_inr(1500000) == "15,00,000"
    assert format_inr(125000.50) == "1,25,000.50"


def test_format_crores():
    from core.formatters import format_crores
    assert format_crores(15000000) == "1.50 Cr"
    assert format_crores(1500000000) == "150.00 Cr"
