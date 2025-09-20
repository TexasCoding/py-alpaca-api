# Error Handling

PyAlpacaAPI provides a comprehensive exception hierarchy for proper error handling.

## Exception Hierarchy

```
PyAlpacaAPIError (base exception)
├── AuthenticationError
├── APIRequestError
├── ValidationError
├── RateLimitError
├── FeedNotAvailableError
└── CacheError
```

## Common Exceptions

### PyAlpacaAPIError

Base exception for all PyAlpacaAPI errors:

```python
from py_alpaca_api.exceptions import PyAlpacaAPIError

try:
    # Any API operation
    order = api.trading.orders.market("AAPL", qty=10)
except PyAlpacaAPIError as e:
    print(f"API error occurred: {e}")
```

### AuthenticationError

Raised when authentication fails:

```python
from py_alpaca_api.exceptions import AuthenticationError

try:
    api = PyAlpacaAPI(
        api_key="invalid_key",
        api_secret="invalid_secret"
    )
    account = api.trading.account.get()
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Check your API credentials
```

### APIRequestError

Raised when API requests fail:

```python
from py_alpaca_api.exceptions import APIRequestError

try:
    order = api.trading.orders.get("invalid_order_id")
except APIRequestError as e:
    print(f"API request failed: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Response: {e.response}")
```

### ValidationError

Raised for invalid input parameters:

```python
from py_alpaca_api.exceptions import ValidationError

try:
    # Invalid quantity (negative)
    order = api.trading.orders.market("AAPL", qty=-10)
except ValidationError as e:
    print(f"Invalid input: {e}")
```

### RateLimitError

Raised when hitting API rate limits:

```python
from py_alpaca_api.exceptions import RateLimitError
import time

try:
    # Rapid API calls
    for i in range(1000):
        quote = api.stock.latest_quote.get("AAPL")
except RateLimitError as e:
    print(f"Rate limit hit: {e}")
    print(f"Retry after: {e.retry_after} seconds")
    time.sleep(e.retry_after)
```

## Error Handling Patterns

### Basic Error Handling

```python
from py_alpaca_api.exceptions import (
    AuthenticationError,
    APIRequestError,
    ValidationError
)

def place_order(symbol, qty):
    try:
        order = api.trading.orders.market(symbol, qty=qty)
        return order
    except ValidationError as e:
        print(f"Invalid order parameters: {e}")
        return None
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        raise  # Re-raise for critical errors
    except APIRequestError as e:
        print(f"API error: {e}")
        return None
```

### Retry Pattern

```python
import time
from py_alpaca_api.exceptions import RateLimitError, APIRequestError

def get_quote_with_retry(symbol, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api.stock.latest_quote.get(symbol)
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(e.retry_after)
        except APIRequestError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Graceful Degradation

```python
from py_alpaca_api.exceptions import FeedNotAvailableError

def get_best_quote(symbol):
    """Get quote from best available feed"""
    feeds = ["sip", "iex", "otc"]

    for feed in feeds:
        try:
            return api.stock.latest_quote.get(symbol, feed=feed)
        except FeedNotAvailableError:
            continue

    # Let automatic detection handle it
    return api.stock.latest_quote.get(symbol)
```

## HTTP Status Codes

Common HTTP status codes and their meanings:

| Status Code | Exception | Description |
|------------|-----------|-------------|
| 401 | AuthenticationError | Invalid API credentials |
| 403 | AuthenticationError | Forbidden (check permissions) |
| 404 | APIRequestError | Resource not found |
| 422 | ValidationError | Invalid request parameters |
| 429 | RateLimitError | Too many requests |
| 500 | APIRequestError | Internal server error |
| 503 | APIRequestError | Service unavailable |

## Logging Errors

Configure logging to track errors:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('py_alpaca_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def safe_order_placement(symbol, qty):
    try:
        order = api.trading.orders.market(symbol, qty=qty)
        logger.info(f"Order placed: {order.id}")
        return order
    except Exception as e:
        logger.error(f"Failed to place order: {e}", exc_info=True)
        raise
```

## Custom Error Handling

Create custom error handlers:

```python
from functools import wraps
from py_alpaca_api.exceptions import PyAlpacaAPIError

def handle_api_errors(default_return=None):
    """Decorator for handling API errors"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except PyAlpacaAPIError as e:
                print(f"API error in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator

@handle_api_errors(default_return=[])
def get_all_positions():
    return api.trading.positions.get_all()
```

## Error Recovery Strategies

### 1. Circuit Breaker Pattern

```python
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.is_open = False

    def call(self, func, *args, **kwargs):
        if self.is_open:
            if datetime.now() - self.last_failure_time > timedelta(seconds=self.timeout):
                self.is_open = False
                self.failure_count = 0
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.is_open = True

            raise
```

### 2. Fallback Values

```python
def get_account_value(fallback=0.0):
    """Get account value with fallback"""
    try:
        account = api.trading.account.get()
        return float(account.portfolio_value)
    except PyAlpacaAPIError as e:
        logger.warning(f"Failed to get account value: {e}")
        return fallback
```

## Best Practices

1. **Catch Specific Exceptions**: Don't catch generic Exception
2. **Log Errors**: Always log errors for debugging
3. **Use Retries**: Implement retry logic for transient failures
4. **Validate Input**: Check parameters before API calls
5. **Handle Rate Limits**: Respect API rate limits
6. **Graceful Degradation**: Provide fallback behavior
7. **Monitor Errors**: Track error rates and patterns
8. **Test Error Cases**: Write tests for error scenarios
