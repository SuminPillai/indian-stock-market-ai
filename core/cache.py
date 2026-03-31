# core/cache.py
"""File-based cache with configurable TTL for market data."""

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import platformdirs


def _get_cache_dir() -> Path:
    """Get cache directory — env var override or platform default."""
    env_dir = os.environ.get("NSE_SKILLS_CACHE_DIR")
    if env_dir:
        p = Path(env_dir)
    else:
        p = Path(platformdirs.user_cache_dir("nse-skills"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def make_cache_key(source: str, endpoint: str, **params) -> str:
    """Generate a deterministic cache key from source, endpoint, and params."""
    sorted_params = json.dumps(params, sort_keys=True)
    raw = f"{source}:{endpoint}:{sorted_params}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


class FileCache:
    """File-based cache with TTL, LRU eviction, and trading day boundary awareness."""

    MAX_CACHE_SIZE_MB = 500  # Evict LRU entries when cache exceeds this

    def __init__(self):
        self.cache_dir = _get_cache_dir()

    def _path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    def get(self, key: str) -> Any | None:
        """Get cached value if it exists and hasn't expired."""
        path = self._path(key)
        if not path.exists():
            return None
        try:
            with open(path, "r") as f:
                entry = json.load(f)
            if time.time() > entry["expires_at"]:
                path.unlink(missing_ok=True)
                return None
            # Touch file to update access time for LRU
            path.touch()
            return entry["data"]
        except (json.JSONDecodeError, KeyError):
            path.unlink(missing_ok=True)
            return None

    def set(self, key: str, data: Any, ttl_seconds: int = 900) -> None:
        """Cache data with a TTL in seconds."""
        entry = {
            "data": data,
            "created_at": time.time(),
            "expires_at": time.time() + ttl_seconds,
        }
        with open(self._path(key), "w") as f:
            json.dump(entry, f, default=str)
        self._evict_if_needed()

    def clear(self) -> None:
        """Remove all cached files."""
        for path in self.cache_dir.glob("*.json"):
            path.unlink(missing_ok=True)

    def invalidate_stale_trading_day(self) -> None:
        """Remove cache entries from previous trading days.
        Call at start of each new trading day to ensure fresh data.
        """
        from core.constants import today_ist, is_trading_day
        today = today_ist()
        if not is_trading_day(today):
            return  # No invalidation on non-trading days
        for path in self.cache_dir.glob("*.json"):
            try:
                with open(path, "r") as f:
                    entry = json.load(f)
                created = entry.get("created_at", 0)
                from datetime import datetime
                from core.constants import IST
                created_date = datetime.fromtimestamp(created, tz=IST).date()
                if created_date < today:
                    path.unlink(missing_ok=True)
            except (json.JSONDecodeError, KeyError, OSError):
                path.unlink(missing_ok=True)

    def _evict_if_needed(self) -> None:
        """Evict least-recently-used entries if cache exceeds max size."""
        total_size = sum(f.stat().st_size for f in self.cache_dir.glob("*.json"))
        if total_size <= self.MAX_CACHE_SIZE_MB * 1024 * 1024:
            return
        # Sort by access time (oldest first) and delete until under limit
        files = sorted(self.cache_dir.glob("*.json"), key=lambda f: f.stat().st_atime)
        for f in files:
            if total_size <= self.MAX_CACHE_SIZE_MB * 1024 * 1024 * 0.8:
                break
            size = f.stat().st_size
            f.unlink(missing_ok=True)
            total_size -= size
