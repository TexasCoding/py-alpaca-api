# Stock Module

The stock module provides market data access and analysis tools for stocks.

```{toctree}
:maxdepth: 2

assets
history
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

# Get top gainers
gainers = api.stock.screener.get_gainers(top=10)
```
