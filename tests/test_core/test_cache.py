# tests/test_core/test_cache.py
import pytest
import json
import time
from pathlib import Path
from unittest.mock import patch


@pytest.fixture
def tmp_cache(tmp_path):
    with patch.dict("os.environ", {"NSE_SKILLS_CACHE_DIR": str(tmp_path)}):
        from core.cache import FileCache
        return FileCache()


def test_cache_set_and_get(tmp_cache):
    tmp_cache.set("test_key", {"price": 100.5}, ttl_seconds=60)
    result = tmp_cache.get("test_key")
    assert result == {"price": 100.5}


def test_cache_miss(tmp_cache):
    result = tmp_cache.get("nonexistent")
    assert result is None


def test_cache_expiry(tmp_cache):
    tmp_cache.set("expire_key", {"data": 1}, ttl_seconds=1)
    time.sleep(1.1)
    result = tmp_cache.get("expire_key")
    assert result is None


def test_cache_clear(tmp_cache):
    tmp_cache.set("key1", "val1", ttl_seconds=60)
    tmp_cache.set("key2", "val2", ttl_seconds=60)
    tmp_cache.clear()
    assert tmp_cache.get("key1") is None
    assert tmp_cache.get("key2") is None


def test_cache_key_hashing(tmp_cache):
    """Identical params should produce same cache key."""
    from core.cache import make_cache_key
    k1 = make_cache_key("nse", "options_chain", symbol="NIFTY", expiry="nearest")
    k2 = make_cache_key("nse", "options_chain", symbol="NIFTY", expiry="nearest")
    assert k1 == k2


def test_cache_different_params(tmp_cache):
    from core.cache import make_cache_key
    k1 = make_cache_key("nse", "options_chain", symbol="NIFTY")
    k2 = make_cache_key("nse", "options_chain", symbol="BANKNIFTY")
    assert k1 != k2
