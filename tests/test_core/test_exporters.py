# tests/test_core/test_exporters.py
import pytest
import json
from pathlib import Path
import pandas as pd


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Symbol": ["RELIANCE", "TCS", "INFY"],
        "Price": [2500.0, 3800.0, 1600.0],
        "PE": [25.3, 30.1, 28.7],
    })


def test_export_csv(sample_df, tmp_path):
    from core.exporters import export_csv
    filepath = export_csv(sample_df, "test_export", output_dir=str(tmp_path))
    assert Path(filepath).exists()
    content = Path(filepath).read_text()
    assert "RELIANCE" in content
    assert "Symbol" in content


def test_export_json(sample_df, tmp_path):
    from core.exporters import export_json
    filepath = export_json(
        sample_df, "test_export",
        metadata={"query": "screener", "timestamp": "2026-03-26"},
        output_dir=str(tmp_path),
    )
    assert Path(filepath).exists()
    data = json.loads(Path(filepath).read_text())
    assert "data" in data
    assert "metadata" in data
    assert data["metadata"]["query"] == "screener"


def test_export_python_code(sample_df, tmp_path):
    from core.exporters import export_python
    filepath = export_python(
        skill_name="nse_screener",
        params={"sector": "IT", "limit": 20},
        output_dir=str(tmp_path),
    )
    assert Path(filepath).exists()
    code = Path(filepath).read_text()
    assert "import yfinance" in code or "import pandas" in code
    assert "nse_screener" in code.lower() or "sector" in code
