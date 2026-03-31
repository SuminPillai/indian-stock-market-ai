# core/auth.py
"""Optional credentials for enhanced data source access."""

import os
from pathlib import Path
from typing import Any

import yaml


def _credentials_path() -> Path:
    return Path.home() / ".nse-skills" / "credentials.yaml"


def load_credentials() -> dict[str, Any]:
    """Load credentials from YAML file. Returns empty dict if not found."""
    path = _credentials_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}
    except (yaml.YAMLError, OSError):
        return {}


def get_credential(key: str) -> str | None:
    """Get a credential. Checks env vars first (NSE_SKILLS_<KEY>), then YAML file."""
    env_key = f"NSE_SKILLS_{key.upper()}"
    env_val = os.environ.get(env_key)
    if env_val:
        return env_val
    creds = load_credentials()
    val = creds.get(key)
    return val if val else None
