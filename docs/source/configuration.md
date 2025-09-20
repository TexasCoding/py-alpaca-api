# Configuration

PyAlpacaAPI offers various configuration options to customize its behavior.

## API Configuration

### Basic Configuration

```python
from py_alpaca_api import PyAlpacaAPI

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    api_paper=True,  # Use paper trading (default)
    api_version="v2"  # API version (default)
)
```

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | str | Required | Your Alpaca API key |
| `api_secret` | str | Required | Your Alpaca secret key |
| `api_paper` | bool | `True` | Use paper trading endpoint |
| `api_version` | str | `"v2"` | Alpaca API version |
| `cache_config` | CacheConfig | `None` | Cache configuration |

## Cache Configuration

### Memory Cache (Default)

```python
from py_alpaca_api.cache import CacheConfig, CacheType

cache_config = CacheConfig(
    cache_type=CacheType.MEMORY,
    max_size=1000,  # Maximum cache entries
    default_ttl=300  # Default TTL in seconds
)

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    cache_config=cache_config
)
```

### Redis Cache

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

### Custom TTL Configuration

Different data types have different optimal cache durations:

```python
cache_config = CacheConfig(
    cache_type=CacheType.MEMORY,
    ttl_config={
        "market_hours": 86400,  # 1 day
        "assets": 3600,         # 1 hour
        "account": 60,          # 1 minute
        "positions": 10,        # 10 seconds
        "orders": 5,            # 5 seconds
        "quotes": 1,            # 1 second
        "bars": 300,            # 5 minutes
        "news": 600,            # 10 minutes
    }
)
```

## Feed Configuration

PyAlpacaAPI automatically detects your data subscription level and falls back to available feeds.

### Automatic Feed Detection

```python
# Automatic feed selection (recommended)
quote = api.stock.latest_quote.get("AAPL")
# Tries SIP → IEX → OTC automatically
```

### Manual Feed Selection

```python
# Force specific feed
quote = api.stock.latest_quote.get("AAPL", feed="iex")

# Available feeds:
# - "sip": Full market data (requires subscription)
# - "iex": IEX Exchange data
# - "otc": OTC market data
```

## Environment Variables

### Using .env File

Create a `.env` file in your project root:

```bash
# API Credentials
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here

# Optional Configuration
ALPACA_API_PAPER=true
ALPACA_API_VERSION=v2

# Redis Configuration (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
REDIS_DB=0

# Cache Configuration
CACHE_TYPE=redis  # or memory
CACHE_DEFAULT_TTL=300
CACHE_MAX_SIZE=1000
```

### Loading Environment Variables

```python
import os
from dotenv import load_dotenv
from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.cache import CacheConfig, CacheType

# Load environment variables
load_dotenv()

# Configure cache from environment
cache_type = CacheType.REDIS if os.getenv("CACHE_TYPE") == "redis" else CacheType.MEMORY

cache_config = CacheConfig(
    cache_type=cache_type,
    redis_host=os.getenv("REDIS_HOST", "localhost"),
    redis_port=int(os.getenv("REDIS_PORT", 6379)),
    redis_password=os.getenv("REDIS_PASSWORD"),
    default_ttl=int(os.getenv("CACHE_DEFAULT_TTL", 300)),
    max_size=int(os.getenv("CACHE_MAX_SIZE", 1000))
)

# Initialize API
api = PyAlpacaAPI(
    api_key=os.getenv("ALPACA_API_KEY"),
    api_secret=os.getenv("ALPACA_SECRET_KEY"),
    api_paper=os.getenv("ALPACA_API_PAPER", "true").lower() == "true",
    cache_config=cache_config
)
```

## Request Configuration

### Retry Configuration

PyAlpacaAPI automatically retries failed requests with exponential backoff:

- Maximum retries: 3
- Backoff factor: 2
- Retry on: 429 (Rate Limit), 500, 502, 503, 504

### Timeout Configuration

Default timeouts:
- Connect timeout: 10 seconds
- Read timeout: 30 seconds

## Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Set PyAlpacaAPI logging level
logging.getLogger("py_alpaca_api").setLevel(logging.DEBUG)
```

## Performance Configuration

### Batch Size Configuration

For operations involving multiple symbols:

```python
# Automatic batching for 200+ symbols
symbols = ["AAPL", "GOOGL", ...] # 500 symbols
quotes = api.stock.latest_quote.get_multiple(symbols)
# Automatically batched into 3 requests (200, 200, 100)
```

### Concurrent Request Configuration

```python
# Concurrent processing for large datasets
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for symbol_batch in symbol_batches:
        future = executor.submit(api.stock.history.get_bars, symbol_batch)
        futures.append(future)

    results = [future.result() for future in futures]
```

## Best Practices

1. **Use Environment Variables**: Never hardcode API credentials
2. **Enable Caching**: Reduce API calls and improve performance
3. **Use Paper Trading**: Always test with paper trading first
4. **Configure Logging**: Monitor API interactions and errors
5. **Handle Rate Limits**: Implement proper retry logic
6. **Batch Operations**: Use batch methods for multiple symbols
7. **Set Appropriate TTLs**: Balance freshness vs performance
