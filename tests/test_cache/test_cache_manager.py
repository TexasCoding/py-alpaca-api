"""Tests for cache manager."""

from __future__ import annotations

import time
from dataclasses import dataclass
from unittest.mock import patch

from py_alpaca_api.cache import CacheConfig, CacheManager, CacheType
from py_alpaca_api.cache.cache_manager import LRUCache, RedisCache


class TestLRUCache:
    """Test LRU cache implementation."""

    def test_init(self):
        """Test LRU cache initialization."""
        cache = LRUCache(max_size=100)
        assert cache.max_size == 100
        assert cache.size() == 0

    def test_set_and_get(self):
        """Test setting and getting items."""
        cache = LRUCache()
        cache.set("key1", "value1", ttl=60)

        assert cache.get("key1") == "value1"
        assert cache.size() == 1

    def test_expiry(self):
        """Test item expiry."""
        cache = LRUCache()
        cache.set("key1", "value1", ttl=0)  # Already expired

        time.sleep(0.01)  # Small delay to ensure expiry
        assert cache.get("key1") is None
        assert cache.size() == 0

    def test_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        cache = LRUCache(max_size=3)

        cache.set("key1", "value1", ttl=60)
        cache.set("key2", "value2", ttl=60)
        cache.set("key3", "value3", ttl=60)

        assert cache.size() == 3

        # Add another item, should evict key1
        cache.set("key4", "value4", ttl=60)

        assert cache.size() == 3
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"

    def test_lru_order(self):
        """Test LRU ordering on access."""
        cache = LRUCache(max_size=3)

        cache.set("key1", "value1", ttl=60)
        cache.set("key2", "value2", ttl=60)
        cache.set("key3", "value3", ttl=60)

        # Access key1 to make it recently used
        _ = cache.get("key1")

        # Add key4, should evict key2 (least recently used)
        cache.set("key4", "value4", ttl=60)

        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None  # Evicted
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"

    def test_delete(self):
        """Test deleting items."""
        cache = LRUCache()
        cache.set("key1", "value1", ttl=60)

        assert cache.delete("key1") is True
        assert cache.get("key1") is None
        assert cache.delete("key1") is False  # Already deleted

    def test_clear(self):
        """Test clearing cache."""
        cache = LRUCache()
        cache.set("key1", "value1", ttl=60)
        cache.set("key2", "value2", ttl=60)

        cache.clear()
        assert cache.size() == 0
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_cleanup_expired(self):
        """Test cleaning up expired items."""
        cache = LRUCache()
        cache.set("key1", "value1", ttl=0)  # Already expired
        cache.set("key2", "value2", ttl=60)  # Not expired

        time.sleep(0.01)  # Small delay to ensure expiry
        removed = cache.cleanup_expired()

        assert removed == 1
        assert cache.size() == 1
        assert cache.get("key2") == "value2"


class TestCacheConfig:
    """Test cache configuration."""

    def test_default_config(self):
        """Test default configuration."""
        config = CacheConfig()

        assert config.cache_type == CacheType.MEMORY
        assert config.max_size == 1000
        assert config.default_ttl == 300
        assert config.enabled is True

    def test_custom_config(self):
        """Test custom configuration."""
        config = CacheConfig(
            cache_type=CacheType.REDIS,
            max_size=500,
            default_ttl=600,
            enabled=False,
        )

        assert config.cache_type == CacheType.REDIS
        assert config.max_size == 500
        assert config.default_ttl == 600
        assert config.enabled is False

    def test_get_ttl(self):
        """Test getting TTL for data types."""
        config = CacheConfig()

        assert config.get_ttl("market_hours") == 86400
        assert config.get_ttl("positions") == 10
        assert config.get_ttl("unknown") == 300  # Default TTL

    def test_custom_data_ttls(self):
        """Test custom data TTLs."""
        config = CacheConfig(data_ttls={"custom_type": 120})

        assert config.get_ttl("custom_type") == 120
        assert config.get_ttl("unknown") == 300  # Default TTL


class TestCacheManager:
    """Test cache manager."""

    def test_init_default(self):
        """Test default initialization."""
        manager = CacheManager()

        assert manager.config.cache_type == CacheType.MEMORY
        assert manager.config.enabled is True
        assert isinstance(manager._cache, LRUCache)

    def test_init_disabled(self):
        """Test disabled cache."""
        config = CacheConfig(enabled=False)
        manager = CacheManager(config)

        # Should still work but not store anything
        manager.set("key1", "value1", "test")
        assert manager.get("key1") is None

    def test_generate_key(self):
        """Test cache key generation."""
        manager = CacheManager()

        key1 = manager.generate_key("bars", symbol="AAPL", timeframe="1d")
        key2 = manager.generate_key("bars", symbol="AAPL", timeframe="1d")
        key3 = manager.generate_key("bars", symbol="GOOGL", timeframe="1d")

        assert key1 == key2  # Same parameters
        assert key1 != key3  # Different parameters

    def test_generate_key_long(self):
        """Test cache key generation with long parameters."""
        manager = CacheManager()

        long_value = "x" * 200
        key = manager.generate_key("test", value=long_value)

        # Should use hash for long keys
        assert len(key) < 100
        assert ":" in key

    def test_get_and_set(self):
        """Test getting and setting cache items."""
        manager = CacheManager()

        manager.set("key1", {"data": "value"}, "test", ttl=60)
        value = manager.get("key1", "test")

        assert value == {"data": "value"}
        assert manager._hit_count == 1
        assert manager._miss_count == 0

    def test_cache_miss(self):
        """Test cache miss."""
        manager = CacheManager()

        value = manager.get("nonexistent", "test")

        assert value is None
        assert manager._hit_count == 0
        assert manager._miss_count == 1

    def test_dataclass_serialization(self):
        """Test caching dataclass objects."""

        @dataclass
        class TestModel:
            id: int
            name: str

        manager = CacheManager()
        model = TestModel(id=1, name="test")

        manager.set("key1", model, "test")
        value = manager.get("key1")

        assert value == {"id": 1, "name": "test"}

    def test_list_of_dataclasses(self):
        """Test caching list of dataclass objects."""

        @dataclass
        class TestModel:
            id: int

        manager = CacheManager()
        models = [TestModel(id=1), TestModel(id=2)]

        manager.set("key1", models, "test")
        value = manager.get("key1")

        assert value == [{"id": 1}, {"id": 2}]

    def test_delete(self):
        """Test deleting cache items."""
        manager = CacheManager()

        manager.set("key1", "value1", "test")
        assert manager.delete("key1") is True
        assert manager.get("key1") is None
        assert manager.delete("key1") is False

    def test_clear_all(self):
        """Test clearing entire cache."""
        manager = CacheManager()

        manager.set("key1", "value1", "test")
        manager.set("key2", "value2", "test")

        count = manager.clear()

        assert count == 2
        assert manager.get("key1") is None
        assert manager.get("key2") is None

    def test_clear_prefix(self):
        """Test clearing cache by prefix."""
        manager = CacheManager()

        # Generate proper keys
        bars_key1 = manager.generate_key("bars", key="key1")
        bars_key2 = manager.generate_key("bars", key="key2")
        quotes_key1 = manager.generate_key("quotes", key="key1")

        manager.set(bars_key1, "value1", "bars")
        manager.set(bars_key2, "value2", "bars")
        manager.set(quotes_key1, "value3", "quotes")

        count = manager.clear("bars")

        assert count == 2
        assert manager.get(bars_key1) is None
        assert manager.get(bars_key2) is None
        assert manager.get(quotes_key1) == "value3"

    def test_invalidate_pattern(self):
        """Test invalidating by pattern."""
        manager = CacheManager()

        manager._cache.set("bars:AAPL:1d", "value1", 60)
        manager._cache.set("bars:AAPL:1h", "value2", 60)
        manager._cache.set("bars:GOOGL:1d", "value3", 60)

        count = manager.invalidate_pattern("bars:AAPL*")

        assert count == 2
        assert manager._cache.get("bars:AAPL:1d") is None
        assert manager._cache.get("bars:AAPL:1h") is None
        assert manager._cache.get("bars:GOOGL:1d") == "value3"

    def test_get_stats(self):
        """Test getting cache statistics."""
        manager = CacheManager()

        manager.set("key1", "value1", "test")
        _ = manager.get("key1")  # Hit
        _ = manager.get("key2")  # Miss

        stats = manager.get_stats()

        assert stats["enabled"] is True
        assert stats["type"] == "memory"
        assert stats["size"] == 1
        assert stats["hit_count"] == 1
        assert stats["miss_count"] == 1
        assert stats["hit_rate"] == 0.5
        assert stats["total_requests"] == 2

    def test_reset_stats(self):
        """Test resetting statistics."""
        manager = CacheManager()

        _ = manager.get("key1")  # Miss
        manager.reset_stats()

        stats = manager.get_stats()

        assert stats["hit_count"] == 0
        assert stats["miss_count"] == 0

    def test_cached_decorator(self):
        """Test cached decorator."""
        manager = CacheManager()

        call_count = 0

        @manager.cached("test", ttl=60)
        def expensive_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call should execute function
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call should use cache
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1  # Not incremented

        # Different argument should execute function
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2

    def test_redis_fallback(self):
        """Test fallback to memory cache when Redis unavailable."""
        config = CacheConfig(cache_type=CacheType.REDIS)

        # Mock the RedisCache._get_client to simulate Redis unavailable
        with patch.object(
            RedisCache, "_get_client", side_effect=Exception("Connection failed")
        ):
            manager = CacheManager(config)

            # Should fall back to memory cache
            assert isinstance(manager._cache, LRUCache)

    def test_disabled_cache(self):
        """Test disabled cache type."""
        config = CacheConfig(cache_type=CacheType.DISABLED)
        manager = CacheManager(config)

        manager.set("key1", "value1", "test")
        assert manager.get("key1") is None
        assert manager._cache.size() == 0
