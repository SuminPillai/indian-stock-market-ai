# core/constants.py
"""Indian market constants and YAML config loader."""

import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
GRANDFATHERING_DATE = date(2018, 1, 31)

NIFTY_SECTORS = [
    "IT", "Bank", "Pharma", "Auto", "FMCG", "Metal", "Realty",
    "Energy", "Infra", "PSU Bank", "Private Bank", "Media",
    "Financial Services", "Consumer Durables",
]

NIFTY_SECTORAL_INDICES = {
    "IT": "NIFTY IT",
    "Bank": "NIFTY BANK",
    "Pharma": "NIFTY PHARMA",
    "Auto": "NIFTY AUTO",
    "FMCG": "NIFTY FMCG",
    "Metal": "NIFTY METAL",
    "Realty": "NIFTY REALTY",
    "Energy": "NIFTY ENERGY",
    "Infra": "NIFTY INFRA",
    "PSU Bank": "NIFTY PSU BANK",
    "Private Bank": "NIFTY PRIVATE BANK",
    "Media": "NIFTY MEDIA",
    "Financial Services": "NIFTY FINANCIAL SERVICES",
    "Consumer Durables": "NIFTY CONSUMER DURABLES",
}

_CONFIG_DIR = Path(__file__).parent.parent / "config"


def _load_yaml(filename: str) -> dict[str, Any]:
    """Load a YAML config file from the config/ directory."""
    filepath = _CONFIG_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Config file not found: {filepath}")
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def load_holidays() -> list[date]:
    """Load trading holidays as a list of date objects."""
    data = _load_yaml("holidays.yaml")
    return [
        datetime.strptime(h["date"], "%Y-%m-%d").date()
        for h in data.get("holidays", [])
    ]


def load_lot_sizes() -> dict[str, int]:
    """Load F&O lot sizes. Returns dict mapping symbol -> lot size."""
    data = _load_yaml("lot_sizes.yaml")
    lots = {}
    lots.update(data.get("index_lots", {}))
    lots.update(data.get("stock_lots", {}))
    return lots


def load_tax_rules() -> dict[str, Any]:
    """Load tax rules from config."""
    return _load_yaml("tax_rules.yaml")


def load_stt_rates() -> dict[str, Any]:
    """Load STT rates from config."""
    return _load_yaml("stt_rates.yaml")


def load_sebi_categories() -> dict[str, Any]:
    """Load SEBI MF categorization norms."""
    return _load_yaml("sebi_categories.yaml")


def is_trading_day(d: date) -> bool:
    """Check if a date is a trading day (not weekend, not holiday)."""
    if d.weekday() >= 5:  # Saturday=5, Sunday=6
        return False
    holidays = load_holidays()
    return d not in holidays


def get_current_fy(d: date | None = None) -> str:
    """Get financial year string (e.g., 'FY2025-26') for a given date.
    FY runs April 1 to March 31. If no date given, uses today in IST.
    """
    if d is None:
        d = datetime.now(IST).date()
    if d.month >= 4:
        return f"FY{d.year}-{str(d.year + 1)[2:]}"
    else:
        return f"FY{d.year - 1}-{str(d.year)[2:]}"


def today_ist() -> date:
    """Get today's date in IST."""
    return datetime.now(IST).date()
