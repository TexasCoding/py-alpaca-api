"""Cache manager for py-alpaca-api."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import logging
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any

from py_alpaca_api.cache.cache_config import CacheConfig, CacheType

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class LRUCache:
    """Least Recently Used (LRU) cache implementation."""

    def __init__(self, max_size: int = 1000):
        """Initialize LRU cache.

        Args:
            max_size: Maximum number of items to store
        """
        self.max_size = max_size
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Any | None:
        """Get item from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self.cache:
            return None

        value, expiry = self.cache[key]

        if time.time() > expiry:
            del self.cache[key]
            return None

        # Move to end to mark as recently used
        self.cache.move_to_end(key)
        return value

    def set(self, key: str, value: Any, ttl: int) -> None:
        """Set item in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        expiry = time.time() + ttl
        self.cache[key] = (value, expiry)
        self.cache.move_to_end(key)

        # Enforce size limit
        while len(self.cache) > self.max_size:
            self.cache.popitem(last=False)

    def delete(self, key: str) -> bool:
        """Delete item from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all items from cache."""
        self.cache.clear()

    def size(self) -> int:
        """Get current cache size.

        Returns:
            Number of items in cache
        """
        return len(self.cache)

    def cleanup_expired(self) -> int:
        """Remove expired items from cache.

        Returns:
            Number of items removed
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items() if current_time > expiry
        ]

        for key in expired_keys:
            del self.cache[key]

        return len(expired_keys)


class RedisCache:
    """Redis cache implementation."""

    def __init__(self, config: CacheConfig):
        """Initialize Redis cache.

        Args:
            config: Cache configuration
        """
        self.config = config
        self._client: Any = None

    def _get_client(self):
        """Get or create Redis client."""
        if self._client is None:
            try:
                import redis  # type: ignore[import-untyped]
            except ImportError:
                logger.warning("Redis not installed, falling back to memory cache")
                raise

            try:
                self._client = redis.Redis(
                    host=self.config.redis_host,
                    port=self.config.redis_port,
                    db=self.config.redis_db,
                    password=self.config.redis_password,
                    decode_responses=True,
                )
                # Test connection
                self._client.ping()
                logger.info("Redis cache connected successfully")
            except Exception:
                logger.exception("Failed to connect to Redis")
                raise

        return self._client

    def get(self, key: str) -> Any | None:
        """Get item from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            client = self._get_client()
            value = client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.warning(f"Redis get failed: {e}")
        return None

    def set(self, key: str, value: Any, ttl: int) -> None:
        """Set item in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        try:
            client = self._get_client()
            json_value = json.dumps(value, default=str)
            client.setex(key, ttl, json_value)
        except Exception as e:
            logger.warning(f"Redis set failed: {e}")

    def delete(self, key: str) -> bool:
        """Delete item from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        try:
            client = self._get_client()
            return bool(client.delete(key))
        except Exception as e:
            logger.warning(f"Redis delete failed: {e}")
            return False

    def clear(self) -> None:
        """Clear all items from cache."""
        try:
            client = self._get_client()
            client.flushdb()
        except Exception as e:
            logger.warning(f"Redis clear failed: {e}")

    def size(self) -> int:
        """Get current cache size.

        Returns:
            Number of items in cache
        """
        try:
            client = self._get_client()
            return client.dbsize()
        except Exception as e:
            logger.warning(f"Redis size failed: {e}")
            return 0


class CacheManager:
    """Manages caching for py-alpaca-api."""

    def __init__(self, config: CacheConfig | None = None):
        """Initialize cache manager.

        Args:
            config: Cache configuration. If None, uses defaults.
        """
        self.config = config or CacheConfig()
        self._cache = self._create_cache()
        self._hit_count = 0
        self._miss_count = 0

    def _create_cache(self) -> LRUCache | RedisCache:
        """Create appropriate cache backend.

        Returns:
            Cache implementation
        """
        if not self.config.enabled or self.config.cache_type == CacheType.DISABLED:
            logger.info("Caching disabled")
            return LRUCache(max_size=0)  # Dummy cache that stores nothing

        if self.config.cache_type == CacheType.REDIS:
            try:
                cache = RedisCache(self.config)
                # Test the connection
                cache._get_client()
            except Exception as e:
                logger.warning(
                    f"Failed to create Redis cache: {e}, falling back to memory cache"
                )
                return LRUCache(self.config.max_size)
            else:
                return cache

        return LRUCache(self.config.max_size)

    def generate_key(self, prefix: str, **kwargs) -> str:
        """Generate cache key from prefix and parameters.

        Args:
            prefix: Key prefix (e.g., "bars", "quotes")
            **kwargs: Parameters to include in key

        Returns:
            Cache key
        """
        # Sort kwargs for consistent key generation
        sorted_params = sorted(kwargs.items())
        param_str = json.dumps(sorted_params, sort_keys=True, default=str)

        # Create hash for long keys
        if len(param_str) > 100:
            param_hash = hashlib.md5(param_str.encode()).hexdigest()
            return f"{prefix}:{param_hash}"

        return f"{prefix}:{param_str}"

    def get(self, key: str, data_type: str | None = None) -> Any | None:  # noqa: ARG002
        """Get item from cache.

        Args:
            key: Cache key
            data_type: Optional data type for metrics

        Returns:
            Cached value or None if not found
        """
        if not self.config.enabled:
            return None

        value = self._cache.get(key)

        if value is not None:
            self._hit_count += 1
            logger.debug(f"Cache hit for {key}")
        else:
            self._miss_count += 1
            logger.debug(f"Cache miss for {key}")

        return value

    def set(self, key: str, value: Any, data_type: str, ttl: int | None = None) -> None:
        """Set item in cache.

        Args:
            key: Cache key
            value: Value to cache
            data_type: Type of data (for TTL lookup)
            ttl: Optional TTL override in seconds
        """
        if not self.config.enabled:
            return

        if ttl is None:
            ttl = self.config.get_ttl(data_type)

        # Convert dataclass to dict for JSON serialization
        if is_dataclass(value):
            if not isinstance(value, type):
                value = asdict(value)  # type: ignore[unreachable]
        elif (
            isinstance(value, list)
            and value
            and is_dataclass(value[0])
            and not isinstance(value[0], type)
        ):
            value = [asdict(item) for item in value]  # type: ignore[unreachable]

        self._cache.set(key, value, ttl)
        logger.debug(f"Cached {key} with TTL {ttl}s")

    def delete(self, key: str) -> bool:
        """Delete item from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        if not self.config.enabled:
            return False

        return self._cache.delete(key)

    def clear(self, prefix: str | None = None) -> int:
        """Clear cache items.

        Args:
            prefix: Optional prefix to clear only specific items

        Returns:
            Number of items cleared
        """
        if not self.config.enabled:
            return 0

        if prefix is None:
            # Clear everything
            size_before = self._cache.size()
            self._cache.clear()
            logger.info(f"Cleared entire cache ({size_before} items)")
            return size_before

        # Clear items with specific prefix
        if isinstance(self._cache, LRUCache):
            keys_to_delete = [
                key for key in self._cache.cache if key.startswith(f"{prefix}:")
            ]
            for key in keys_to_delete:
                self._cache.delete(key)

            logger.info(f"Cleared {len(keys_to_delete)} items with prefix '{prefix}'")
            return len(keys_to_delete)

        # For Redis, we'd need to scan keys (expensive operation)
        logger.warning("Prefix-based clearing not fully supported for Redis cache")
        return 0

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate cache items matching a pattern.

        Args:
            pattern: Pattern to match (e.g., "bars:*AAPL*")

        Returns:
            Number of items invalidated
        """
        if not self.config.enabled:
            return 0

        count = 0
        if isinstance(self._cache, LRUCache):
            keys_to_delete = [
                key for key in self._cache.cache if fnmatch.fnmatch(key, pattern)
            ]
            for key in keys_to_delete:
                self._cache.delete(key)
                count += 1

        logger.info(f"Invalidated {count} items matching pattern '{pattern}'")
        return count

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        hit_rate = 0.0
        total = self._hit_count + self._miss_count
        if total > 0:
            hit_rate = self._hit_count / total

        return {
            "enabled": self.config.enabled,
            "type": self.config.cache_type.value,
            "size": self._cache.size() if self.config.enabled else 0,
            "max_size": self.config.max_size,
            "hit_count": self._hit_count,
            "miss_count": self._miss_count,
            "hit_rate": hit_rate,
            "total_requests": total,
        }

    def reset_stats(self) -> None:
        """Reset cache statistics."""
        self._hit_count = 0
        self._miss_count = 0
        logger.debug("Cache statistics reset")

    def cached(self, data_type: str, ttl: int | None = None) -> Callable:
        """Decorator for caching function results.

        Args:
            data_type: Type of data being cached
            ttl: Optional TTL override

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                cache_key = self.generate_key(
                    f"{func.__module__}.{func.__name__}",
                    args=str(args),
                    kwargs=str(kwargs),
                )

                # Try to get from cache
                cached_value = self.get(cache_key, data_type)
                if cached_value is not None:
                    return cached_value

                # Call function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, data_type, ttl)
                return result

            return wrapper

        return decorator
