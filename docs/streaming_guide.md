# WebSocket Streaming Guide

## Overview

The py-alpaca-api v3.1.0 introduces WebSocket streaming support for real-time market data. This allows you to receive live quotes, trades, and bar data without polling.

## Features

- **Real-time Data**: Receive quotes, trades, and bars as they happen
- **Automatic Reconnection**: Built-in exponential backoff for connection stability
- **Multiple Subscriptions**: Subscribe to multiple symbols and data types simultaneously
- **Feed Selection**: Choose between IEX, SIP, and OTC feeds
- **Thread-Safe**: Handle messages in separate threads safely

## Quick Start

```python
from py_alpaca_api import PyAlpacaAPI

# Initialize API
alpaca = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    api_paper=True
)

# Create streaming client
stream = alpaca.create_stream_client(feed="iex")

# Define handlers
def on_quote(quote):
    print(f"Quote: {quote.symbol} - Bid: ${quote.bid_price} Ask: ${quote.ask_price}")

def on_trade(trade):
    print(f"Trade: {trade.symbol} - Price: ${trade.price} Size: {trade.size}")

def on_bar(bar):
    print(f"Bar: {bar.symbol} - OHLC: ${bar.open}/{bar.high}/{bar.low}/{bar.close}")

# Connect and subscribe
stream.connect()
stream.subscribe_quotes(["AAPL", "GOOGL"], on_quote)
stream.subscribe_trades(["MSFT"], on_trade)
stream.subscribe_bars(["SPY"], on_bar)

# Keep running (or do other work)
import time
time.sleep(60)

# Disconnect when done
stream.disconnect()
```

## Using Context Manager

```python
from py_alpaca_api import PyAlpacaAPI

alpaca = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    api_paper=True
)

# Automatically connects and disconnects
with alpaca.create_stream_client() as stream:
    def on_quote(quote):
        print(f"Quote received: {quote}")

    stream.subscribe_quotes(["AAPL"], on_quote)

    # Stream will run for 30 seconds
    import time
    time.sleep(30)
# Automatically disconnects here
```

## Advanced Usage

### Multiple Handlers

```python
# You can have multiple handlers for the same data type
def log_quote(quote):
    logger.info(f"Quote: {quote}")

def process_quote(quote):
    # Your processing logic
    if quote.bid_price > threshold:
        place_order(quote.symbol)

stream.subscribe_quotes(["AAPL"], log_quote)
stream.subscribe_quotes(["AAPL"], process_quote)
```

### Dynamic Subscriptions

```python
# Subscribe and unsubscribe dynamically
stream.connect()

# Start with some symbols
stream.subscribe_quotes(["AAPL", "GOOGL"], handler)

# Add more symbols later
stream.subscribe_quotes(["MSFT", "AMZN"], handler)

# Remove symbols
stream.unsubscribe_quotes(["AAPL"])

# Check active subscriptions
print(stream.subscriptions)
```

### Error Handling

```python
def safe_quote_handler(quote):
    try:
        # Your processing logic
        process_quote(quote)
    except Exception as e:
        logger.error(f"Error processing quote: {e}")
        # Handler errors won't crash the stream

stream.subscribe_quotes(["AAPL"], safe_quote_handler)
```

### Collecting Data

```python
from collections import deque
from threading import Lock

# Thread-safe data collection
quotes_buffer = deque(maxlen=1000)
buffer_lock = Lock()

def collect_quotes(quote):
    with buffer_lock:
        quotes_buffer.append({
            'symbol': quote.symbol,
            'bid': quote.bid_price,
            'ask': quote.ask_price,
            'timestamp': quote.timestamp
        })

stream.subscribe_quotes(["SPY"], collect_quotes)

# Process collected data periodically
def process_buffer():
    with buffer_lock:
        data = list(quotes_buffer)
        quotes_buffer.clear()

    # Process data
    df = pd.DataFrame(data)
    # ... analysis ...
```

## Data Models

### QuoteData
```python
@dataclass
class QuoteData:
    symbol: str
    timestamp: datetime
    bid_price: float
    bid_size: int
    ask_price: float
    ask_size: int
    bid_exchange: str
    ask_exchange: str
    conditions: list[str]
```

### TradeData
```python
@dataclass
class TradeData:
    symbol: str
    timestamp: datetime
    price: float
    size: int
    exchange: str
    trade_id: str
    conditions: list[str]
```

### BarData
```python
@dataclass
class BarData:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    trade_count: int
    vwap: float
```

## Feed Types

- **IEX**: Included with all market data subscriptions (free)
- **SIP**: Full exchange data, requires Unlimited or Business subscription
- **OTC**: Over-the-counter securities data

```python
# IEX feed (default, free)
stream_iex = alpaca.create_stream_client(feed="iex")

# SIP feed (requires subscription)
stream_sip = alpaca.create_stream_client(feed="sip")

# OTC feed
stream_otc = alpaca.create_stream_client(feed="otc")
```

## Best Practices

1. **Use Handlers Efficiently**: Keep handlers fast and non-blocking
2. **Error Handling**: Always wrap handler logic in try-except
3. **Resource Management**: Use context managers or ensure proper disconnect
4. **Buffering**: Collect data in thread-safe structures for batch processing
5. **Logging**: Log important events but avoid logging every message
6. **Reconnection**: The client auto-reconnects, but monitor connection status

## Connection Management

### Monitoring Connection Status

```python
# Check connection status
if stream.is_connected:
    print("Stream is connected")

if stream.is_authenticated:
    print("Stream is authenticated")

# Monitor reconnection attempts
print(f"Reconnect attempts: {stream.reconnect_attempts}")
```

### Custom Reconnection Settings

```python
stream = alpaca.create_stream_client()

# Customize reconnection behavior
stream.max_reconnect_attempts = 20
stream.reconnect_delay = 2  # Initial delay in seconds
stream.max_reconnect_delay = 60  # Max delay between attempts

stream.connect()
```

## Performance Considerations

- Each handler is called synchronously - keep them fast
- Use queues or buffers for heavy processing
- Consider using separate threads for data processing
- Monitor memory usage with large subscriptions
- Bars are aggregated and sent less frequently than quotes/trades

## Troubleshooting

### No Data Received

1. Check market hours - no data outside trading hours
2. Verify symbol is valid and tradable
3. Check your subscription level for feed access
4. Ensure handlers are properly defined

### Connection Issues

1. Verify API credentials are correct
2. Check network connectivity
3. Monitor logs for authentication errors
4. Review reconnection attempts in logs

### Handler Errors

1. Wrap handler logic in try-except blocks
2. Log errors for debugging
3. Handler errors won't disconnect stream
4. Test handlers with sample data first

## Example: Real-time VWAP Calculation

```python
from collections import defaultdict
import threading

class VWAPCalculator:
    def __init__(self):
        self.data = defaultdict(lambda: {'volume': 0, 'value': 0})
        self.lock = threading.Lock()

    def on_trade(self, trade):
        with self.lock:
            symbol_data = self.data[trade.symbol]
            symbol_data['volume'] += trade.size
            symbol_data['value'] += trade.price * trade.size

            vwap = symbol_data['value'] / symbol_data['volume']
            print(f"{trade.symbol} VWAP: ${vwap:.2f}")

# Use the calculator
calculator = VWAPCalculator()
stream = alpaca.create_stream_client()
stream.connect()
stream.subscribe_trades(["AAPL", "GOOGL"], calculator.on_trade)
```

## Migration from Polling

If you're currently polling for data, streaming provides several advantages:

```python
# Old way - Polling
while True:
    quote = alpaca.stock.latest_quote.get("AAPL")
    process_quote(quote)
    time.sleep(1)  # Delay, missing data

# New way - Streaming
stream = alpaca.create_stream_client()
stream.connect()
stream.subscribe_quotes(["AAPL"], process_quote)
# Receives all quotes in real-time, no missed data
```

## Related Documentation

- [Alpaca WebSocket API Docs](https://docs.alpaca.markets/docs/real-time-market-data)
- [Market Data Subscriptions](https://alpaca.markets/data)
- [API Rate Limits](https://docs.alpaca.markets/docs/api-rate-limit)
