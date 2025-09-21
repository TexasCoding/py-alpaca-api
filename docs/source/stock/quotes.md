# Historical Quotes

The quotes module provides access to historical bid/ask quote data with spread analysis.

## Overview

The quotes module allows you to retrieve historical quote data including:
- Bid and ask prices
- Bid and ask sizes
- Spread calculation
- Spread percentage
- Exchange and condition codes

## Usage

### Single Symbol Quotes

```python
from py_alpaca_api import PyAlpacaAPI

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key"
)

# Get historical quotes for a single symbol
quotes = api.stock.quotes.get_historical_quotes(
    "AAPL",
    start="2024-01-01T09:30:00Z",
    end="2024-01-01T16:00:00Z",
    limit=1000
)

# Returns a DataFrame with columns:
# - ask_price: The ask price
# - ask_size: The ask size
# - bid_price: The bid price
# - bid_size: The bid size
# - spread: The bid-ask spread
# - spread_pct: The spread as a percentage
```

### Multiple Symbol Quotes

```python
# Get quotes for multiple symbols
symbols = ["AAPL", "MSFT", "GOOGL"]
quotes = api.stock.quotes.get_historical_quotes(
    symbols,
    start="2024-01-01",
    end="2024-01-31"
)

# Returns a dictionary mapping symbols to DataFrames
for symbol, df in quotes.items():
    print(f"{symbol}: {len(df)} quotes")
    print(f"Average spread: {df['spread'].mean():.4f}")
```

## Parameters

### get_historical_quotes()

- **symbols**: Single symbol string or list of symbols
- **start**: Start date/time in ISO 8601 format
- **end**: End date/time in ISO 8601 format
- **limit**: Maximum number of quotes per symbol (default: 10000)
- **asof**: As-of date for corporate actions adjustments
- **feed**: Data feed to use ("iex", "sip", or "otc")
- **page_token**: Pagination token from previous request
- **sort**: Sort order ("asc" or "desc")

## Features

### Spread Analysis

The module automatically calculates:
- **Spread**: The difference between ask and bid prices
- **Spread Percentage**: The spread as a percentage of the mid-price

```python
# Analyze spreads
quotes = api.stock.quotes.get_historical_quotes("AAPL", start="2024-01-01", end="2024-01-02")

print(f"Average spread: ${quotes['spread'].mean():.4f}")
print(f"Average spread %: {quotes['spread_pct'].mean():.4f}%")
print(f"Max spread: ${quotes['spread'].max():.4f}")
print(f"Min spread: ${quotes['spread'].min():.4f}")
```

### Pagination

The module handles pagination automatically for large datasets:

```python
# Automatically handles pagination for large requests
quotes = api.stock.quotes.get_historical_quotes(
    "AAPL",
    start="2024-01-01",
    end="2024-12-31",
    limit=50000  # Will paginate as needed
)
```

## Feed Selection

Choose between different data feeds based on your subscription:

```python
# Use SIP feed for consolidated data
quotes = api.stock.quotes.get_historical_quotes(
    "AAPL",
    start="2024-01-01",
    end="2024-01-02",
    feed="sip"
)

# Use IEX feed for IEX-only data
quotes = api.stock.quotes.get_historical_quotes(
    "AAPL",
    start="2024-01-01",
    end="2024-01-02",
    feed="iex"
)
```

## Error Handling

The module includes comprehensive error handling:

```python
from py_alpaca_api.exceptions import ValidationError

try:
    quotes = api.stock.quotes.get_historical_quotes(
        "INVALID",
        start="invalid-date",
        end="2024-01-01"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```
