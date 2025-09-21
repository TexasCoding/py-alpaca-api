# Historical Auctions

The auctions module provides access to opening and closing auction data for stocks.

## Overview

The auctions module allows you to retrieve:
- Opening auction prices and volumes
- Closing auction prices and volumes
- Intraday returns between auctions
- Daily aggregated auction data

## Usage

### Historical Auctions

```python
from py_alpaca_api import PyAlpacaAPI

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key"
)

# Get auction data for a single symbol
auctions = api.stock.auctions.get_auctions(
    "AAPL",
    start="2024-01-01",
    end="2024-01-31"
)

# Returns a DataFrame with columns:
# - opening_price: Opening auction price
# - opening_volume: Opening auction volume
# - closing_price: Closing auction price
# - closing_volume: Closing auction volume
# - intraday_return: Return from opening to closing
```

### Multiple Symbol Auctions

```python
# Get auctions for multiple symbols
symbols = ["AAPL", "MSFT", "GOOGL"]
auctions = api.stock.auctions.get_auctions(
    symbols,
    start="2024-01-01",
    end="2024-01-31"
)

# Returns a dictionary mapping symbols to DataFrames
for symbol, df in auctions.items():
    print(f"{symbol}: {len(df)} auctions")
    print(f"Average intraday return: {df['intraday_return'].mean():.2f}%")
```

### Daily Aggregated Auctions

```python
# Get daily aggregated auction data
daily_auctions = api.stock.auctions.get_daily_auctions(
    "AAPL",
    start="2024-01-01",
    end="2024-01-31"
)

# Returns daily aggregated data with:
# - One row per trading day
# - Opening and closing prices for the day
# - Daily return calculation
```

## Parameters

### get_auctions()

- **symbols**: Single symbol string or list of symbols
- **start**: Start date in YYYY-MM-DD format
- **end**: End date in YYYY-MM-DD format
- **limit**: Maximum number of auctions per symbol (default: 10000)
- **asof**: As-of date for corporate actions adjustments
- **feed**: Data feed to use ("iex", "sip", or "otc")
- **page_token**: Pagination token from previous request
- **sort**: Sort order ("asc" or "desc")

### get_daily_auctions()

- **symbols**: Single symbol string or list of symbols
- **start**: Start date in YYYY-MM-DD format
- **end**: End date in YYYY-MM-DD format
- **feed**: Data feed to use ("iex", "sip", or "otc")

## Features

### Intraday Return Calculation

The module automatically calculates intraday returns:

```python
# Analyze intraday returns
auctions = api.stock.auctions.get_auctions("AAPL", start="2024-01-01", end="2024-01-31")

print(f"Average intraday return: {auctions['intraday_return'].mean():.2f}%")
print(f"Max intraday return: {auctions['intraday_return'].max():.2f}%")
print(f"Min intraday return: {auctions['intraday_return'].min():.2f}%")

# Find days with large movements
large_moves = auctions[abs(auctions['intraday_return']) > 2]
print(f"Days with >2% intraday move: {len(large_moves)}")
```

### Auction Volume Analysis

```python
# Analyze auction volumes
auctions = api.stock.auctions.get_auctions("AAPL", start="2024-01-01", end="2024-01-31")

# Compare opening vs closing volumes
avg_opening_vol = auctions['opening_volume'].mean()
avg_closing_vol = auctions['closing_volume'].mean()

print(f"Average opening volume: {avg_opening_vol:,.0f}")
print(f"Average closing volume: {avg_closing_vol:,.0f}")
print(f"Closing/Opening ratio: {avg_closing_vol/avg_opening_vol:.2f}")
```

### Daily Aggregation

```python
# Get daily summary
daily = api.stock.auctions.get_daily_auctions(
    "AAPL",
    start="2024-01-01",
    end="2024-01-31"
)

# Analyze daily patterns
print(f"Average daily return: {daily['daily_return'].mean():.2f}%")
print(f"Volatility (std): {daily['daily_return'].std():.2f}%")

# Find trending days
up_days = daily[daily['daily_return'] > 0]
down_days = daily[daily['daily_return'] < 0]
print(f"Up days: {len(up_days)} ({len(up_days)/len(daily)*100:.1f}%)")
print(f"Down days: {len(down_days)} ({len(down_days)/len(daily)*100:.1f}%)")
```

## Pagination

The module handles pagination automatically:

```python
# Automatically handles pagination for large requests
auctions = api.stock.auctions.get_auctions(
    "AAPL",
    start="2023-01-01",
    end="2024-12-31",
    limit=50000  # Will paginate as needed
)
```

## Error Handling

```python
from py_alpaca_api.exceptions import ValidationError

try:
    auctions = api.stock.auctions.get_auctions(
        "AAPL",
        start="invalid-date",
        end="2024-01-01"
    )
except ValidationError as e:
    print(f"Validation error: {e}")
```
