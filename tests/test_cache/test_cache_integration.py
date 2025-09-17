"""Integration tests for cache system."""

from __future__ import annotations

import os
import time
from unittest.mock import patch

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.cache import CacheConfig, CacheManager, CacheType


@pytest.fixture
def cache_manager():
    """Create cache manager for testing."""
    config = CacheConfig(
        cache_type=CacheType.MEMORY,
        max_size=100,
        default_ttl=60,
    )
    return CacheManager(config)


@pytest.fixture
def alpaca():
    """Create PyAlpacaAPI client for testing."""
    api_key = os.getenv("ALPACA_API_KEY", "test_key")
    api_secret = os.getenv("ALPACA_SECRET_KEY", "test_secret")

    return PyAlpacaAPI(
        api_key=api_key,
        api_secret=api_secret,
        api_paper=True,
    )


class TestCacheIntegration:
    """Integration tests for cache system."""

    def test_cache_with_bars_data(self, cache_manager):
        """Test caching bar data."""
        # Simulate bar data
        bars_data = {
            "symbol": "AAPL",
            "bars": [
                {
                    "t": "2024-01-01T00:00:00Z",
                    "o": 100,
                    "h": 105,
                    "l": 99,
                    "c": 103,
                    "v": 1000,
                },
                {
                    "t": "2024-01-02T00:00:00Z",
                    "o": 103,
                    "h": 108,
                    "l": 102,
                    "c": 106,
                    "v": 1200,
                },
            ],
        }

        # Generate cache key
        cache_key = cache_manager.generate_key(
            "bars",
            symbol="AAPL",
            start="2024-01-01",
            end="2024-01-02",
            timeframe="1d",
        )

        # Set in cache
        cache_manager.set(cache_key, bars_data, "bars")

        # Get from cache
        cached_data = cache_manager.get(cache_key, "bars")

        assert cached_data == bars_data
        assert cache_manager._hit_count == 1

    def test_cache_with_quotes_data(self, cache_manager):
        """Test caching quote data."""
        quote_data = {
            "symbol": "AAPL",
            "bid": 150.25,
            "ask": 150.30,
            "bid_size": 100,
            "ask_size": 200,
            "timestamp": "2024-01-01T10:30:00Z",
        }

        cache_key = cache_manager.generate_key("quotes", symbol="AAPL")
        cache_manager.set(cache_key, quote_data, "quotes", ttl=1)  # 1 second TTL

        # Immediate get should work
        assert cache_manager.get(cache_key) == quote_data

        # After expiry should return None
        time.sleep(1.1)
        assert cache_manager.get(cache_key) is None

    def test_cache_with_market_hours(self, cache_manager):
        """Test caching market hours data."""
        market_hours = {
            "date": "2024-01-01",
            "open": "09:30",
            "close": "16:00",
            "is_open": True,
        }

        cache_key = cache_manager.generate_key("market_hours", date="2024-01-01")
        cache_manager.set(cache_key, market_hours, "market_hours")

        # Should have 1 day TTL
        cached_data = cache_manager.get(cache_key)
        assert cached_data == market_hours

        # Check TTL is set correctly (86400 seconds)
        assert cache_manager.config.get_ttl("market_hours") == 86400

    def test_cache_invalidation_on_symbol(self, cache_manager):
        """Test invalidating cache for specific symbol."""
        # Add multiple entries
        cache_manager._cache.set("bars:AAPL:1d", {"data": "aapl_daily"}, 60)
        cache_manager._cache.set("bars:AAPL:1h", {"data": "aapl_hourly"}, 60)
        cache_manager._cache.set("quotes:AAPL", {"data": "aapl_quote"}, 60)
        cache_manager._cache.set("bars:GOOGL:1d", {"data": "googl_daily"}, 60)

        # Invalidate all AAPL data
        count = cache_manager.invalidate_pattern("*AAPL*")

        assert count == 3
        assert cache_manager._cache.get("bars:GOOGL:1d") == {"data": "googl_daily"}

    def test_cache_size_limit(self, cache_manager):
        """Test cache size limit enforcement."""
        cache_manager.config.max_size = 5
        cache_manager._cache.max_size = 5

        # Add more items than max size
        for i in range(10):
            key = cache_manager.generate_key("test", id=i)
            cache_manager.set(key, f"value_{i}", "test")

        # Should only have 5 items
        assert cache_manager._cache.size() == 5

        # Latest items should be present
        for i in range(5, 10):
            key = cache_manager.generate_key("test", id=i)
            assert cache_manager.get(key) is not None

        # Oldest items should be evicted
        for i in range(0, 5):
            key = cache_manager.generate_key("test", id=i)
            assert cache_manager.get(key) is None

    def test_cache_decorator_with_api_call(self, cache_manager):
        """Test cached decorator with simulated API call."""
        api_call_count = 0

        @cache_manager.cached("assets", ttl=3600)
        def get_asset(symbol: str) -> dict:
            nonlocal api_call_count
            api_call_count += 1
            # Simulate API call
            return {"symbol": symbol, "name": f"{symbol} Company", "exchange": "NASDAQ"}

        # First call should make API call
        result1 = get_asset("AAPL")
        assert result1["symbol"] == "AAPL"
        assert api_call_count == 1

        # Second call should use cache
        result2 = get_asset("AAPL")
        assert result2 == result1
        assert api_call_count == 1  # No additional API call

        # Different symbol should make API call
        result3 = get_asset("GOOGL")
        assert result3["symbol"] == "GOOGL"
        assert api_call_count == 2

    def test_concurrent_cache_access(self, cache_manager):
        """Test concurrent access to cache."""
        import threading

        results = []
        errors = []

        def cache_operation(thread_id: int):
            try:
                # Each thread sets and gets its own key
                key = cache_manager.generate_key("thread", id=thread_id)
                cache_manager.set(key, f"value_{thread_id}", "test")
                time.sleep(0.01)  # Small delay
                value = cache_manager.get(key)
                results.append(value == f"value_{thread_id}")
            except Exception as e:
                errors.append(e)

        # Create multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=cache_operation, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All operations should succeed
        assert len(errors) == 0
        assert all(results)

    def test_cache_stats_accuracy(self, cache_manager):
        """Test accuracy of cache statistics."""
        # Perform various operations
        cache_manager.set("key1", "value1", "test")
        cache_manager.set("key2", "value2", "test")

        _ = cache_manager.get("key1")  # Hit
        _ = cache_manager.get("key2")  # Hit
        _ = cache_manager.get("key3")  # Miss
        _ = cache_manager.get("key4")  # Miss

        cache_manager.delete("key1")

        stats = cache_manager.get_stats()

        assert stats["size"] == 1  # Only key2 remains
        assert stats["hit_count"] == 2
        assert stats["miss_count"] == 2
        assert stats["hit_rate"] == 0.5
        assert stats["total_requests"] == 4

    def test_cache_clear_by_data_type(self, cache_manager):
        """Test clearing cache by data type prefix."""
        # Add items of different types
        bars_key = cache_manager.generate_key("bars", symbol="AAPL")
        quotes_key = cache_manager.generate_key("quotes", symbol="AAPL")
        trades_key = cache_manager.generate_key("trades", symbol="AAPL")

        cache_manager.set(bars_key, "bars_data", "bars")
        cache_manager.set(quotes_key, "quotes_data", "quotes")
        cache_manager.set(trades_key, "trades_data", "trades")

        # Clear only bars
        count = cache_manager.clear("bars")

        assert count == 1
        assert cache_manager.get(bars_key) is None
        assert cache_manager.get(quotes_key) == "quotes_data"
        assert cache_manager.get(trades_key) == "trades_data"

    def test_cache_memory_efficiency(self, cache_manager):
        """Test memory efficiency with large datasets."""
        # Create a large dataset
        large_data = {
            "symbol": "AAPL",
            "bars": [
                {"t": f"2024-01-{i:02d}", "o": 100 + i, "c": 100 + i + 1}
                for i in range(1, 32)  # 31 days of data
            ],
        }

        key = cache_manager.generate_key("bars", symbol="AAPL", month="2024-01")
        cache_manager.set(key, large_data, "bars")

        # Should be able to retrieve
        cached = cache_manager.get(key)
        assert cached == large_data
        assert len(cached["bars"]) == 31

    def test_redis_cache_simulation(self):
        """Test Redis cache configuration (simulated)."""
        from py_alpaca_api.cache.cache_manager import LRUCache, RedisCache

        config = CacheConfig(
            cache_type=CacheType.REDIS,
            redis_host="localhost",
            redis_port=6379,
            redis_password="test_password",
        )

        # Mock the RedisCache to simulate unavailable Redis server
        with patch.object(
            RedisCache, "_get_client", side_effect=Exception("Redis not available")
        ):
            # Should fall back to memory cache gracefully
            manager = CacheManager(config)
            assert isinstance(manager._cache, LRUCache)

            # Should still work with memory cache
            manager.set("key1", "value1", "test")
            assert manager.get("key1") == "value1"
