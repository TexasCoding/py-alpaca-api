# Historical Data

The history module provides access to historical price data, bars, and latest market data.

## Overview

The history module allows you to:
- Retrieve historical price bars (OHLCV data)
- Get the latest bars for symbols
- Access multi-timeframe data (1Min, 5Min, 15Min, 1Hour, 1Day, etc.)
- Batch retrieve data for multiple symbols

## Usage

### Historical Bars

```python
from py_alpaca_api import PyAlpacaAPI
import pendulum

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key"
)

# Get daily bars for the last 30 days
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.now().subtract(days=30),
    end=pendulum.now(),
    timeframe="1Day"
)

# Returns a DataFrame with columns:
# - open: Opening price
# - high: High price
# - low: Low price
# - close: Closing price
# - volume: Trading volume
# - trade_count: Number of trades
# - vwap: Volume-weighted average price
```

### Latest Bars

```python
# Get the latest bar for a single symbol
latest = api.stock.history.get_latest_bars("AAPL")

print(f"Latest close: ${latest.iloc[0]['close']}")
print(f"Volume: {latest.iloc[0]['volume']:,}")

# Get latest bars for multiple symbols
symbols = ["AAPL", "MSFT", "GOOGL"]
latest_bars = api.stock.history.get_latest_bars(symbols)

# Returns a dictionary mapping symbols to DataFrames
for symbol, df in latest_bars.items():
    print(f"{symbol}: ${df.iloc[0]['close']}")
```

### Intraday Bars

```python
# Get 5-minute bars for today
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.today("America/New_York").add(hours=9, minutes=30),
    end=pendulum.now("America/New_York"),
    timeframe="5Min"
)

# Analyze price movements
print(f"Bars retrieved: {len(bars)}")
print(f"Day's range: ${bars['low'].min():.2f} - ${bars['high'].max():.2f}")
print(f"Total volume: {bars['volume'].sum():,}")
```

## Methods

### get_bars() / get_stock_data()

Retrieve historical bar data for a symbol.

**Parameters:**
- **symbol**: Stock symbol
- **start**: Start date/time (pendulum datetime)
- **end**: End date/time (pendulum datetime)
- **timeframe**: Bar timeframe ("1Min", "5Min", "15Min", "30Min", "1Hour", "1Day", "1Week", "1Month")
- **adjustment**: Price adjustment for splits ("raw", "split", "dividend", "all")
- **feed**: Data feed to use ("iex", "sip", "otc")
- **limit**: Maximum number of bars to return
- **page_limit**: Number of bars per page
- **asof**: As-of date for corporate actions

### get_latest_bars()

Get the most recent bar for one or more symbols.

**Parameters:**
- **symbols**: Single symbol string or list of symbols
- **feed**: Data feed to use ("iex", "sip", "otc")
- **currency**: Currency for the bars (default: "USD")

### get_bars_multi()

Get bars for multiple symbols in a single request.

**Parameters:**
- **symbols**: List of stock symbols
- **start**: Start date/time
- **end**: End date/time
- **timeframe**: Bar timeframe
- **adjustment**: Price adjustment
- **feed**: Data feed

## Timeframes

Available timeframes for bar data:

| Timeframe | Description |
|-----------|-------------|
| 1Min | One minute bars |
| 5Min | Five minute bars |
| 15Min | Fifteen minute bars |
| 30Min | Thirty minute bars |
| 1Hour | Hourly bars |
| 1Day | Daily bars |
| 1Week | Weekly bars |
| 1Month | Monthly bars |

## Price Adjustments

Control how historical prices are adjusted:

```python
# Raw prices (no adjustments)
bars_raw = api.stock.history.get_bars(
    symbol="AAPL",
    start=start_date,
    end=end_date,
    timeframe="1Day",
    adjustment="raw"
)

# Split-adjusted only
bars_split = api.stock.history.get_bars(
    symbol="AAPL",
    start=start_date,
    end=end_date,
    timeframe="1Day",
    adjustment="split"
)

# All adjustments (splits and dividends)
bars_adjusted = api.stock.history.get_bars(
    symbol="AAPL",
    start=start_date,
    end=end_date,
    timeframe="1Day",
    adjustment="all"
)
```

## Technical Analysis

```python
# Calculate moving averages
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.now().subtract(days=100),
    end=pendulum.now(),
    timeframe="1Day"
)

# Simple moving averages
bars['SMA_20'] = bars['close'].rolling(window=20).mean()
bars['SMA_50'] = bars['close'].rolling(window=50).mean()

# Bollinger Bands
bars['BB_middle'] = bars['close'].rolling(window=20).mean()
bars['BB_std'] = bars['close'].rolling(window=20).std()
bars['BB_upper'] = bars['BB_middle'] + (bars['BB_std'] * 2)
bars['BB_lower'] = bars['BB_middle'] - (bars['BB_std'] * 2)

# RSI calculation
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

bars['RSI'] = calculate_rsi(bars['close'])
```

## Volume Analysis

```python
# Analyze volume patterns
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.now().subtract(days=30),
    end=pendulum.now(),
    timeframe="1Day"
)

# Volume indicators
bars['Volume_MA'] = bars['volume'].rolling(window=20).mean()
bars['Volume_Ratio'] = bars['volume'] / bars['Volume_MA']

# Find high volume days
high_volume_days = bars[bars['Volume_Ratio'] > 1.5]
print(f"Days with 50% above average volume: {len(high_volume_days)}")

# VWAP analysis
bars['VWAP_Diff'] = bars['close'] - bars['vwap']
bars['VWAP_Pct'] = (bars['VWAP_Diff'] / bars['vwap']) * 100
```

## Batch Operations

```python
# Get data for multiple symbols efficiently
symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

# Latest bars for all symbols
latest = api.stock.history.get_latest_bars(symbols)

# Historical data for multiple symbols
all_data = {}
for symbol in symbols:
    all_data[symbol] = api.stock.history.get_bars(
        symbol=symbol,
        start=pendulum.now().subtract(days=7),
        end=pendulum.now(),
        timeframe="1Hour"
    )

# Analyze correlations
closes = pd.DataFrame({
    symbol: data['close']
    for symbol, data in all_data.items()
})
correlation_matrix = closes.corr()
```

## Error Handling

```python
from py_alpaca_api.exceptions import APIRequestError

try:
    bars = api.stock.history.get_bars(
        symbol="INVALID",
        start=pendulum.now().subtract(days=30),
        end=pendulum.now(),
        timeframe="1Day"
    )
except APIRequestError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Error retrieving data: {e}")
```

## Performance Tips

1. **Use appropriate timeframes**: Don't request minute bars for multi-year periods
2. **Implement caching**: The library includes built-in caching support
3. **Batch requests**: Use get_latest_bars() with multiple symbols instead of looping
4. **Limit data range**: Request only the data you need
5. **Use pagination**: For large datasets, the library handles pagination automatically
