# Feed Management

PyAlpacaAPI includes intelligent feed management that automatically detects your subscription level and falls back to available data feeds.

## Overview

Alpaca provides different data feed levels:
- **SIP**: Full market data (requires subscription)
- **IEX**: IEX Exchange data (free tier available)
- **OTC**: Over-the-counter market data

## Automatic Feed Detection

The feed manager automatically detects your subscription level and uses the best available feed:

```python
from py_alpaca_api import PyAlpacaAPI

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key"
)

# Automatic feed selection
quote = api.stock.latest_quote.get("AAPL")
# Tries: SIP → IEX → OTC
```

### How It Works

1. **First Request**: Tries the highest tier feed (SIP)
2. **On Failure**: Falls back to next tier (IEX, then OTC)
3. **Caching**: Remembers successful feed for future requests
4. **Per-Endpoint**: Different endpoints may have different available feeds

## Manual Feed Selection

Override automatic detection by specifying a feed:

```python
# Force specific feed
quote = api.stock.latest_quote.get("AAPL", feed="iex")
bars = api.stock.history.get_bars("AAPL", feed="sip")

# Available feeds
FEEDS = ["sip", "iex", "otc"]
```

## Feed Availability

Different endpoints support different feeds:

| Endpoint | SIP | IEX | OTC |
|----------|-----|-----|-----|
| Latest Quote | ✅ | ✅ | ✅ |
| Historical Bars | ✅ | ✅ | ❌ |
| Trades | ✅ | ✅ | ✅ |
| Snapshots | ✅ | ✅ | ❌ |

## Feed Characteristics

### SIP Feed
- **Coverage**: All US exchanges
- **Latency**: Lowest latency
- **Cost**: Requires paid subscription
- **Use Case**: Professional trading

### IEX Feed
- **Coverage**: IEX Exchange only (~2-3% of market volume)
- **Latency**: Low latency
- **Cost**: Free tier available
- **Use Case**: Development, testing, basic trading

### OTC Feed
- **Coverage**: OTC markets
- **Latency**: Variable
- **Cost**: Included with account
- **Use Case**: OTC securities

## Feed Manager Configuration

```python
from py_alpaca_api.http.feed_manager import FeedManager

# Access feed manager
feed_manager = api.feed_manager

# Get current feed for endpoint
current_feed = feed_manager.get_feed("latest_quote")

# Clear feed cache (force re-detection)
feed_manager.clear_cache()

# Check feed availability
is_available = feed_manager.is_feed_available("sip", "latest_quote")
```

## Handling Feed Errors

```python
from py_alpaca_api.exceptions import FeedNotAvailableError

try:
    # Force SIP feed when not subscribed
    quote = api.stock.latest_quote.get("AAPL", feed="sip")
except FeedNotAvailableError as e:
    print(f"Feed not available: {e}")
    # Falls back automatically if feed not specified
    quote = api.stock.latest_quote.get("AAPL")
```

## Multi-Symbol Requests

Feed management works seamlessly with batch operations:

```python
# Automatic feed detection for multiple symbols
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
quotes = api.stock.latest_quote.get_multiple(symbols)
# Uses the best available feed for all symbols
```

## Feed Performance

### Latency Comparison

| Feed | Average Latency | Update Frequency |
|------|----------------|------------------|
| SIP | < 1ms | Real-time |
| IEX | 1-5ms | Real-time (IEX only) |
| OTC | 5-15ms | Near real-time |

### Data Quality

- **SIP**: Complete market picture, all trades
- **IEX**: ~2-3% of market volume, IEX trades only
- **OTC**: OTC market trades only

## Best Practices

1. **Use Automatic Detection**: Let the system choose the best feed
2. **Test with IEX**: Develop using the free IEX feed
3. **Upgrade for Production**: Consider SIP for production trading
4. **Cache Feed Results**: Reduce detection overhead
5. **Handle Fallbacks**: Design for graceful degradation

## Feed Subscription

To upgrade your data subscription:

1. Log into your Alpaca account
2. Navigate to Account → Market Data Subscriptions
3. Choose your subscription level
4. Changes take effect immediately

## Troubleshooting

### Common Issues

**Issue**: Getting IEX data when expecting SIP
```python
# Solution: Check subscription status
account = api.trading.account.get()
print(f"Data subscription: {account.multiplier}")
```

**Issue**: Feed detection slow on first request
```python
# Solution: Pre-warm the feed cache
api.stock.latest_quote.get("AAPL")  # Detects feed
# Subsequent requests use cached feed
```

**Issue**: Different feeds for different symbols
```python
# Solution: Some symbols may only be available on specific feeds
# OTC symbols won't be on IEX, for example
```

## Feed Costs

| Subscription | Monthly Cost | Features |
|--------------|--------------|----------|
| Free | $0 | IEX feed only |
| Algo Trader | $9 | SIP for quotes/trades |
| Algo Trader Pro | $99 | Full SIP access |

*Prices subject to change. Check Alpaca for current pricing.*
