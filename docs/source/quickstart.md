# Quickstart Guide

This guide will help you get started with PyAlpacaAPI quickly.

## Basic Setup

```python
from py_alpaca_api import PyAlpacaAPI
import os

# Initialize the API client
api = PyAlpacaAPI(
    api_key=os.environ.get("ALPACA_API_KEY"),
    api_secret=os.environ.get("ALPACA_SECRET_KEY"),
    api_paper=True  # Use paper trading
)
```

## Trading Operations

### Get Account Information

```python
# Get account details
account = api.trading.account.get()
print(f"Buying Power: ${account.buying_power}")
print(f"Portfolio Value: ${account.portfolio_value}")
```

### Place Orders

```python
# Place a market order
order = api.trading.orders.market(
    symbol="AAPL",
    qty=10,
    side="buy"
)
print(f"Order placed: {order.id}")

# Place a limit order with stop loss and take profit
order = api.trading.orders.limit(
    symbol="AAPL",
    qty=10,
    limit_price=150.00,
    side="buy",
    stop_loss=145.00,
    take_profit=160.00
)
```

### Manage Positions

```python
# Get all positions
positions = api.trading.positions.get_all()
for position in positions:
    print(f"{position.symbol}: {position.qty} shares at ${position.avg_entry_price}")

# Get specific position
aapl_position = api.trading.positions.get("AAPL")
```

## Market Data

### Get Stock Quotes

```python
# Get latest quote for a single symbol
quote = api.stock.latest_quote.get("AAPL")
print(f"AAPL: ${quote.ask_price} / ${quote.bid_price}")

# Get quotes for multiple symbols (automatic batching)
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
quotes = api.stock.latest_quote.get_multiple(symbols)
for symbol, quote in quotes.items():
    print(f"{symbol}: ${quote.ask_price}")
```

### Get Historical Data

```python
import pendulum

# Get historical bars
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.now().subtract(days=30),
    end=pendulum.now(),
    timeframe="1Day"
)
print(bars.head())
```

## Stock Analysis

### Screen for Top Performers

```python
# Get top gainers
gainers = api.stock.screener.get_gainers(top=10)
for stock in gainers:
    print(f"{stock['symbol']}: +{stock['change_percentage']:.2f}%")

# Get top losers
losers = api.stock.screener.get_losers(top=10)
```

### Get Stock Predictions

```python
# Get ML prediction for a stock
prediction = api.stock.predictor.predict(
    symbol="AAPL",
    days=30  # Predict 30 days ahead
)
print(f"Predicted price in 30 days: ${prediction['predicted_price']}")
```

### Get News and Sentiment

```python
# Get latest news
news = api.trading.news.get(symbols=["AAPL"], limit=5)
for article in news:
    print(f"{article.headline} - {article.created_at}")

# Get analyst recommendations
recommendations = api.trading.recommendations.get("AAPL")
print(f"Consensus: {recommendations['consensus']}")
print(f"Target Price: ${recommendations['target_price']}")
```

## Watchlists

```python
# Create a watchlist
watchlist = api.trading.watchlists.create(
    name="Tech Stocks",
    symbols=["AAPL", "GOOGL", "MSFT", "AMZN"]
)

# Get all watchlists
watchlists = api.trading.watchlists.get_all()
for wl in watchlists:
    print(f"{wl.name}: {len(wl.symbols)} symbols")
```

## Using Caching

```python
from py_alpaca_api.cache import CacheConfig, CacheType

# Configure caching
cache_config = CacheConfig(
    cache_type=CacheType.REDIS,  # or CacheType.MEMORY
    redis_host="localhost",
    redis_port=6379,
    default_ttl=300  # 5 minutes
)

# Initialize API with caching
api = PyAlpacaAPI(
    api_key=os.environ.get("ALPACA_API_KEY"),
    api_secret=os.environ.get("ALPACA_SECRET_KEY"),
    api_paper=True,
    cache_config=cache_config
)
```

## Error Handling

```python
from py_alpaca_api.exceptions import (
    PyAlpacaAPIError,
    AuthenticationError,
    APIRequestError,
    ValidationError
)

try:
    order = api.trading.orders.market(
        symbol="INVALID",
        qty=10,
        side="buy"
    )
except ValidationError as e:
    print(f"Invalid input: {e}")
except APIRequestError as e:
    print(f"API error: {e}")
except PyAlpacaAPIError as e:
    print(f"General error: {e}")
```

## Next Steps

- Explore the [Trading Documentation](trading/index.md) for advanced order types
- Learn about [Market Data](stock/index.md) capabilities
- Read about [Caching](caching.md) for performance optimization
- Check out [Examples](examples/index.md) for complete working examples
