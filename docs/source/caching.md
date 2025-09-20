# Caching

PyAlpacaAPI includes a sophisticated caching system to reduce API calls and improve performance.

## Overview

The caching system provides:
- **LRU Memory Cache**: Default in-memory caching
- **Redis Cache**: Distributed caching for production
- **Automatic Fallback**: Falls back to memory cache if Redis is unavailable
- **Configurable TTLs**: Different cache durations per data type
- **Cache Invalidation**: Smart cache invalidation on updates

## Memory Cache

The default caching mechanism uses an LRU (Least Recently Used) in-memory cache:

```python
from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.cache import CacheConfig, CacheType

cache_config = CacheConfig(
    cache_type=CacheType.MEMORY,
    max_size=1000,  # Maximum number of cached items
    default_ttl=300  # Default time-to-live in seconds
)

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    cache_config=cache_config
)
```

## Redis Cache

For production environments or distributed systems:

```python
from py_alpaca_api.cache import CacheConfig, CacheType

cache_config = CacheConfig(
    cache_type=CacheType.REDIS,
    redis_host="localhost",
    redis_port=6379,
    redis_password="optional_password",
    redis_db=0,
    default_ttl=300
)

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    cache_config=cache_config
)
```

### Redis Installation

```bash
# Install Redis support
pip install py-alpaca-api[redis]

# Start Redis server
redis-server
```

## TTL Configuration

Different data types have optimized cache durations:

| Data Type | Default TTL | Description |
|-----------|------------|-------------|
| Market Hours | 86400s (1 day) | Market calendar rarely changes |
| Assets | 3600s (1 hour) | Asset information is relatively static |
| Account | 60s (1 minute) | Account data updates frequently |
| Positions | 10s | Position data is highly dynamic |
| Orders | 5s | Order status changes rapidly |
| Quotes | 1s | Real-time data needs minimal caching |
| Historical Bars | 300s (5 minutes) | Historical data is static |
| News | 600s (10 minutes) | News updates periodically |
| Market Metadata | 86400s (1 day) | Exchange info rarely changes |

### Custom TTL Configuration

```python
from py_alpaca_api.cache import CacheConfig, CacheType

cache_config = CacheConfig(
    cache_type=CacheType.MEMORY,
    ttl_config={
        "market_hours": 86400,  # 1 day
        "assets": 7200,         # 2 hours
        "account": 30,          # 30 seconds
        "positions": 5,         # 5 seconds
        "orders": 2,            # 2 seconds
        "quotes": 0,            # No caching
        "bars": 600,            # 10 minutes
        "news": 300,            # 5 minutes
    }
)
```

## Cache Keys

Cache keys are automatically generated based on:
- Endpoint
- Parameters
- Symbol(s)
- Time range (for historical data)

Example cache key format:
```
py_alpaca_api:quotes:AAPL:iex
py_alpaca_api:bars:AAPL:1Day:2024-01-01:2024-01-31
py_alpaca_api:account:status
```

## Cache Invalidation

The cache is automatically invalidated when:
- TTL expires
- Trading operations modify state (orders, positions)
- Manual cache clearing

### Manual Cache Management

```python
from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.cache import CacheManager

api = PyAlpacaAPI(...)

# Access the cache manager
cache_manager = api.cache_manager

# Clear specific cache entry
cache_manager.delete("py_alpaca_api:quotes:AAPL")

# Clear all cache entries
cache_manager.clear()

# Check if key exists
exists = cache_manager.exists("py_alpaca_api:account:status")

# Get cache statistics (Redis only)
if cache_config.cache_type == CacheType.REDIS:
    info = cache_manager.info()
    print(f"Cache size: {info['used_memory_human']}")
```

## Performance Considerations

### Memory Cache

- **Pros**:
  - Zero latency
  - No external dependencies
  - Simple setup
- **Cons**:
  - Limited by process memory
  - Not shared across processes
  - Lost on restart

### Redis Cache

- **Pros**:
  - Distributed caching
  - Persistent storage
  - Shared across processes
  - Advanced features (expiration, pub/sub)
- **Cons**:
  - Network latency
  - External dependency
  - Additional infrastructure

## Best Practices

1. **Use Redis in Production**: For multi-process applications
2. **Set Appropriate TTLs**: Balance freshness vs performance
3. **Monitor Cache Hit Ratio**: Optimize TTLs based on usage
4. **Clear Cache on Errors**: Prevent stale data propagation
5. **Use Batch Operations**: Cache multiple items efficiently

## Cache Metrics

Monitor cache effectiveness:

```python
# Example cache monitoring
import time

start = time.time()
quote1 = api.stock.latest_quote.get("AAPL")  # Cache miss
time1 = time.time() - start

start = time.time()
quote2 = api.stock.latest_quote.get("AAPL")  # Cache hit
time2 = time.time() - start

print(f"Cache miss: {time1:.3f}s")
print(f"Cache hit: {time2:.3f}s")
print(f"Speed improvement: {time1/time2:.1f}x")
```

## Disabling Cache

To disable caching entirely:

```python
api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    cache_config=None  # No caching
)
```
