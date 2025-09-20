# Examples

This section contains practical examples of using PyAlpacaAPI.

## Trading Examples

### Basic Order Placement

```python
from py_alpaca_api import PyAlpacaAPI
import os

api = PyAlpacaAPI(
    api_key=os.environ.get("ALPACA_API_KEY"),
    api_secret=os.environ.get("ALPACA_SECRET_KEY"),
    api_paper=True
)

# Market order
order = api.trading.orders.market("AAPL", qty=10)
print(f"Order {order.id} placed")

# Limit order
order = api.trading.orders.limit(
    symbol="GOOGL",
    qty=5,
    limit_price=150.00
)
```

### Portfolio Management

```python
# Get account information
account = api.trading.account.get()
print(f"Buying Power: ${account.buying_power}")

# Get all positions
positions = api.trading.positions.get_all()
for pos in positions:
    pnl_pct = (pos.unrealized_pl / pos.cost_basis) * 100
    print(f"{pos.symbol}: {pos.qty} shares, P/L: {pnl_pct:.2f}%")

# Close a position
api.trading.positions.close("AAPL")
```

## Market Data Examples

### Real-time Quotes

```python
# Single symbol
quote = api.stock.latest_quote.get("AAPL")
print(f"AAPL Bid: ${quote.bid_price} Ask: ${quote.ask_price}")

# Multiple symbols
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]
quotes = api.stock.latest_quote.get_multiple(symbols)
for symbol, quote in quotes.items():
    spread = quote.ask_price - quote.bid_price
    print(f"{symbol}: Spread ${spread:.2f}")
```

### Historical Data Analysis

```python
import pendulum
import pandas as pd

# Get daily bars
bars = api.stock.history.get_bars(
    symbol="AAPL",
    start=pendulum.now().subtract(months=3),
    end=pendulum.now(),
    timeframe="1Day"
)

# Calculate returns
bars['returns'] = bars['close'].pct_change()
bars['cumulative_returns'] = (1 + bars['returns']).cumprod()

# Find support/resistance levels
bars['support'] = bars['low'].rolling(20).min()
bars['resistance'] = bars['high'].rolling(20).max()
```

## Analysis Examples

### Stock Screening

```python
# Find top gainers
gainers = api.stock.screener.get_gainers(top=20)
strong_gainers = [
    stock for stock in gainers
    if stock['change_percentage'] > 5.0
]

# Find top losers
losers = api.stock.screener.get_losers(top=20)
oversold = [
    stock for stock in losers
    if stock['change_percentage'] < -5.0
]
```

### ML Predictions

```python
# Predict future price
prediction = api.stock.predictor.predict(
    symbol="AAPL",
    days=30,
    include_history=True
)

print(f"Current price: ${prediction['current_price']}")
print(f"Predicted price: ${prediction['predicted_price']}")
print(f"Expected change: {prediction['change_percentage']:.2f}%")

# Get prediction with confidence intervals
prediction = api.stock.predictor.predict(
    symbol="TSLA",
    days=14,
    include_history=True
)
df = prediction['forecast']
print(df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
```

## Advanced Examples

### Automated Trading Strategy

```python
from py_alpaca_api import PyAlpacaAPI
import pendulum
import time

class SimpleStrategy:
    def __init__(self, api, symbol, qty=10):
        self.api = api
        self.symbol = symbol
        self.qty = qty

    def should_buy(self):
        # Get recent bars
        bars = self.api.stock.history.get_bars(
            symbol=self.symbol,
            start=pendulum.now().subtract(days=5),
            end=pendulum.now(),
            timeframe="15Min"
        )

        # Simple moving average crossover
        bars['sma_20'] = bars['close'].rolling(20).mean()
        bars['sma_50'] = bars['close'].rolling(50).mean()

        last_row = bars.iloc[-1]
        prev_row = bars.iloc[-2]

        # Buy signal: SMA20 crosses above SMA50
        return (last_row['sma_20'] > last_row['sma_50'] and
                prev_row['sma_20'] <= prev_row['sma_50'])

    def run(self):
        while True:
            try:
                # Check if market is open
                clock = self.api.trading.market.clock()
                if not clock.is_open:
                    print("Market is closed")
                    time.sleep(60)
                    continue

                # Check for buy signal
                if self.should_buy():
                    # Check if we have a position
                    positions = self.api.trading.positions.get_all()
                    symbols = [p.symbol for p in positions]

                    if self.symbol not in symbols:
                        # Place buy order
                        order = self.api.trading.orders.market(
                            self.symbol,
                            qty=self.qty
                        )
                        print(f"Buy order placed: {order.id}")

                time.sleep(60)  # Check every minute

            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)

# Run strategy
strategy = SimpleStrategy(api, "AAPL", qty=10)
# strategy.run()  # Uncomment to run
```

### Risk Management

```python
def calculate_position_size(api, symbol, risk_percentage=1.0):
    """Calculate position size based on risk"""
    account = api.trading.account.get()
    portfolio_value = float(account.portfolio_value)

    # Risk amount
    risk_amount = portfolio_value * (risk_percentage / 100)

    # Get current price
    quote = api.stock.latest_quote.get(symbol)
    current_price = quote.ask_price

    # Calculate stop loss (2% below current price)
    stop_loss = current_price * 0.98
    risk_per_share = current_price - stop_loss

    # Calculate position size
    position_size = int(risk_amount / risk_per_share)

    return position_size, stop_loss

# Example usage
qty, stop_loss = calculate_position_size(api, "AAPL", risk_percentage=1.0)
print(f"Position size: {qty} shares")
print(f"Stop loss: ${stop_loss:.2f}")
```

### Watchlist Management

```python
# Create sector watchlists
tech_stocks = ["AAPL", "GOOGL", "MSFT", "NVDA", "META"]
finance_stocks = ["JPM", "BAC", "GS", "MS", "WFC"]

tech_watchlist = api.trading.watchlists.create(
    name="Tech Leaders",
    symbols=tech_stocks
)

finance_watchlist = api.trading.watchlists.create(
    name="Financial Sector",
    symbols=finance_stocks
)

# Monitor watchlist performance
def check_watchlist_performance(api, watchlist_name):
    watchlist = api.trading.watchlists.get_by_name(watchlist_name)

    total_change = 0
    for symbol in watchlist.symbols:
        quote = api.stock.latest_quote.get(symbol)
        bars = api.stock.history.get_bars(
            symbol=symbol,
            start=pendulum.today(),
            end=pendulum.now(),
            timeframe="1Day"
        )
        if not bars.empty:
            daily_change = ((quote.ask_price - bars.iloc[0]['open']) /
                          bars.iloc[0]['open']) * 100
            total_change += daily_change
            print(f"{symbol}: {daily_change:.2f}%")

    avg_change = total_change / len(watchlist.symbols)
    print(f"Average change: {avg_change:.2f}%")

# Monitor performance
check_watchlist_performance(api, "Tech Leaders")
```
