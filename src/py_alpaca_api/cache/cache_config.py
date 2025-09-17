"""Cache configuration for py-alpaca-api."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CacheType(Enum):
    """Types of cache backends supported."""

    MEMORY = "memory"
    REDIS = "redis"
    DISABLED = "disabled"


@dataclass
class CacheConfig:
    """Configuration for cache system.

    Attributes:
        cache_type: Type of cache backend to use
        max_size: Maximum number of items in memory cache
        default_ttl: Default time-to-live in seconds
        data_ttls: TTL overrides per data type
        redis_host: Redis host (if using Redis)
        redis_port: Redis port (if using Redis)
        redis_db: Redis database number (if using Redis)
        redis_password: Redis password (if using Redis)
        enabled: Whether caching is enabled
    """

    cache_type: CacheType = CacheType.MEMORY
    max_size: int = 1000
    default_ttl: int = 300  # 5 minutes default
    data_ttls: dict[str, int] = field(
        default_factory=lambda: {
            "market_hours": 86400,  # 1 day
            "calendar": 86400,  # 1 day
            "assets": 3600,  # 1 hour
            "account": 60,  # 1 minute
            "positions": 10,  # 10 seconds
            "orders": 5,  # 5 seconds
            "quotes": 1,  # 1 second
            "bars": 60,  # 1 minute
            "trades": 60,  # 1 minute
            "news": 300,  # 5 minutes
            "watchlists": 300,  # 5 minutes
            "snapshots": 1,  # 1 second
            "metadata": 86400,  # 1 day (condition codes, exchanges)
        }
    )
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    enabled: bool = True

    def get_ttl(self, data_type: str) -> int:
        """Get TTL for a specific data type.

        Args:
            data_type: Type of data to get TTL for

        Returns:
            TTL in seconds
        """
        return self.data_ttls.get(data_type, self.default_ttl)
