# Stock Module

The stock module provides market data access and analysis tools for stocks.

```{toctree}
:maxdepth: 2

assets
history
quotes
auctions
logos
screener
predictor
latest_quote
trades
snapshots
metadata
```

## Overview

The stock module includes:

- **Assets**: Stock asset information and metadata
- **History**: Historical price data and bars
- **Quotes**: Historical bid/ask quote data
- **Auctions**: Opening and closing auction data
- **Logos**: Company logo retrieval
- **Screener**: Screen for top gainers and losers
- **Predictor**: ML-based price predictions using Prophet
- **Latest Quote**: Real-time quote data
- **Trades**: Trade execution data
- **Snapshots**: Market snapshots
- **Metadata**: Market metadata, conditions, and exchanges

## Features

### Batch Operations

The stock module automatically handles batch operations for multiple symbols:

```python
# Automatic batching for 200+ symbols
symbols = ["AAPL", "GOOGL", "MSFT", ...] # 500 symbols
quotes = api.stock.latest_quote.get_multiple(symbols)
# Automatically split into optimal batches
```

### Feed Management

Automatic feed detection and fallback:

```python
# Automatic feed selection
quote = api.stock.latest_quote.get("AAPL")
# Tries SIP → IEX → OTC based on subscription

# Manual feed selection
quote = api.stock.latest_quote.get("AAPL", feed="iex")
```

## Quick Example

```python
from py_alpaca_api import PyAlpacaAPI
import pendulum

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key"
)

# Get latest quote
quote = api.stock.latest_quote.get("AAPL")

# Get historical data
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.now().subtract(days=30),
    end=pendulum.now(),
    timeframe="1Day"
)

# Get historical quotes with bid/ask spread
quotes = api.stock.quotes.get_historical_quotes(
    "AAPL",
    start="2024-01-01",
    end="2024-01-31"
)

# Get auction data
auctions = api.stock.auctions.get_auctions(
    "AAPL",
    start="2024-01-01",
    end="2024-01-31"
)

# Get company logo
logo_url = api.stock.logos.get_logo_url("AAPL")
logo_data = api.stock.logos.get_logo("AAPL")

# Get top gainers
gainers = api.stock.screener.get_gainers(top=10)
```
