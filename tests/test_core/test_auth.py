# tests/test_core/test_auth.py
import pytest
from pathlib import Path
from unittest.mock import patch


def test_load_credentials_missing_file():
    from core.auth import load_credentials
    with patch("core.auth._credentials_path", return_value=Path("/nonexistent/creds.yaml")):
        creds = load_credentials()
    assert creds == {}


def test_load_credentials_from_env():
    from core.auth import get_credential
    with patch.dict("os.environ", {"NSE_SKILLS_BSE_API_KEY": "test123"}):
        assert get_credential("bse_api_key") == "test123"


def test_get_credential_returns_none_when_missing():
    from core.auth import get_credential
    with patch.dict("os.environ", {}, clear=True):
        with patch("core.auth.load_credentials", return_value={}):
            assert get_credential("nonexistent_key") is None


def test_load_credentials_from_yaml_file(tmp_path):
    from core.auth import load_credentials
    creds_file = tmp_path / "credentials.yaml"
    creds_file.write_text("bse_api_key: yaml_key_123\namfi_api_key: amfi_456\n")
    with patch("core.auth._credentials_path", return_value=creds_file):
        creds = load_credentials()
    assert creds["bse_api_key"] == "yaml_key_123"
    assert creds["amfi_api_key"] == "amfi_456"
