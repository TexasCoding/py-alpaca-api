# 🚀 py-alpaca-api

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/py-alpaca-api)](https://pypi.org/project/py-alpaca-api/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://github.com/TexasCoding/py-alpaca-api/workflows/CI/badge.svg)](https://github.com/TexasCoding/py-alpaca-api/actions)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checked](https://img.shields.io/badge/type_checked-mypy-blue)](http://mypy-lang.org/)

A modern Python wrapper for the Alpaca Trading API, providing easy access to trading, market data, and account management functionality with full type safety and comprehensive testing.

## ✨ Features

- **🔐 Complete Alpaca API Coverage**: Trading, market data, account management, and more
- **📊 Stock Market Analysis**: Built-in screeners for gainers/losers, historical data analysis
- **🤖 ML-Powered Predictions**: Stock price predictions using Facebook Prophet
- **📰 Financial News Integration**: Real-time news from Yahoo Finance and Benzinga
- **📈 Technical Analysis**: Stock recommendations and sentiment analysis
- **🎯 Type Safety**: Full type annotations with mypy strict mode
- **🧪 Battle-Tested**: 100+ tests with comprehensive coverage
- **⚡ Modern Python**: Async-ready, Python 3.10+ with latest best practices

## 📦 Installation

### Using pip

```bash
pip install py-alpaca-api
```

### Using uv (recommended)

```bash
uv add py-alpaca-api
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/TexasCoding/py-alpaca-api.git
cd py-alpaca-api

# Install with development dependencies using uv
uv sync --all-extras --dev

# Or using pip
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Basic Setup

```python
from py_alpaca_api import PyAlpacaAPI

# Initialize with your API credentials
api = PyAlpacaAPI(
    api_key="YOUR_API_KEY",
    api_secret="YOUR_SECRET_KEY",
    api_paper=True  # Use paper trading for testing
)

# Get account information
account = api.trading.account.get()
print(f"Account Balance: ${account.cash}")
print(f"Buying Power: ${account.buying_power}")
```

### Trading Operations

```python
# Place a market order
order = api.trading.orders.market(
    symbol="AAPL",
    qty=1,
    side="buy"
)
print(f"Order placed: {order.id}")

# Place a limit order
limit_order = api.trading.orders.limit(
    symbol="GOOGL",
    qty=1,
    side="buy",
    limit_price=150.00
)

# Get all positions
positions = api.trading.positions.get_all()
for position in positions:
    print(f"{position.symbol}: {position.qty} shares @ ${position.avg_entry_price}")

# Cancel all open orders
api.trading.orders.cancel_all()
```

### Market Data & Analysis

```python
# Get historical stock data
history = api.stock.history.get(
    symbol="TSLA",
    start="2024-01-01",
    end="2024-12-31"
)

# Get real-time quote
quote = api.stock.latest_quote.get("MSFT")
print(f"MSFT Price: ${quote.ask_price}")

# Screen for top gainers
gainers = api.stock.screener.gainers(
    price_greater_than=10.0,
    change_greater_than=5.0,
    volume_greater_than=1000000
)
print("Top Gainers:")
for stock in gainers.head(10).itertuples():
    print(f"{stock.symbol}: +{stock.change}%")

# Screen for top losers
losers = api.stock.screener.losers(
    price_greater_than=10.0,
    change_less_than=-5.0,
    volume_greater_than=1000000
)
```

### Stock Predictions with ML

```python
# Predict future stock prices using Prophet
predictions = api.stock.predictor.predict(
    symbol="AAPL",
    days_to_predict=30,
    forecast_days_back=365
)

# Get prediction for specific date
future_price = predictions[predictions['ds'] == '2024-12-31']['yhat'].values[0]
print(f"Predicted AAPL price on 2024-12-31: ${future_price:.2f}")
```

### Financial News & Sentiment

```python
# Get latest financial news
news = api.trading.news.get(symbol="NVDA")
for article in news[:5]:
    print(f"- {article['headline']}")
    print(f"  Sentiment: {article.get('sentiment', 'N/A')}")

# Get stock recommendations
recommendations = api.trading.recommendations.get_recommendations("META")
sentiment = api.trading.recommendations.get_sentiment("META")
print(f"META Sentiment: {sentiment}")
```

### Portfolio Analysis

```python
# Get portfolio history
portfolio_history = api.trading.account.portfolio_history(
    period="1M",
    timeframe="1D"
)

# Calculate returns
returns = (
    (portfolio_history['equity'].iloc[-1] - portfolio_history['equity'].iloc[0]) /
    portfolio_history['equity'].iloc[0] * 100
)
print(f"Monthly Return: {returns:.2f}%")

# Get account activities
activities = api.trading.account.get_activities()
for activity in activities:
    print(f"{activity.created_at}: {activity.activity_type} - {activity.symbol}")
```

## 📊 Advanced Features

### Watchlist Management

```python
# Create a watchlist
watchlist = api.trading.watchlists.create_watchlist(
    name="Tech Stocks",
    symbols=["AAPL", "GOOGL", "MSFT", "NVDA"]
)

# Add symbols to existing watchlist
api.trading.watchlists.add_assets_to_watchlist(
    watchlist_id=watchlist.id,
    symbols=["META", "AMZN"]
)

# Get all watchlists
watchlists = api.trading.watchlists.get_all_watchlists()
```

### Corporate Actions

```python
# Get dividend announcements
dividends = api.trading.corporate_actions.get_announcements(
    since="2024-01-01",
    until="2024-03-31",
    ca_types=["dividend"],
    symbol="AAPL"  # Optional: filter by symbol
)

for dividend in dividends:
    print(f"{dividend.initiating_symbol}: ${dividend.cash_amount} on {dividend.payable_date}")

# Get stock splits
splits = api.trading.corporate_actions.get_announcements(
    since="2024-01-01",
    until="2024-03-31",
    ca_types=["split"]
)

for split in splits:
    print(f"{split.initiating_symbol}: {split.split_from}:{split.split_to} split")

# Get mergers and acquisitions
mergers = api.trading.corporate_actions.get_announcements(
    since="2024-01-01",
    until="2024-03-31",
    ca_types=["merger"]
)

# Get specific announcement by ID
announcement = api.trading.corporate_actions.get_announcement_by_id("123456")
print(f"Corporate Action: {announcement.ca_type} for {announcement.initiating_symbol}")

# Get all types of corporate actions
all_actions = api.trading.corporate_actions.get_announcements(
    since="2024-01-01",
    until="2024-03-31",
    ca_types=["dividend", "split", "merger", "spinoff"],
    date_type="ex_dividend"  # Filter by specific date type
)
```

### Trade Data

```python
# Get historical trades for a symbol
trades_response = api.stock.trades.get_trades(
    symbol="AAPL",
    start="2024-01-15T09:30:00Z",
    end="2024-01-15T10:00:00Z",
    limit=100
)

for trade in trades_response.trades:
    print(f"Trade: {trade.size} shares @ ${trade.price} on {trade.exchange}")

# Get latest trade for a symbol
latest_trade = api.stock.trades.get_latest_trade("MSFT")
print(f"Latest MSFT trade: ${latest_trade.price} x {latest_trade.size}")

# Get trades for multiple symbols
multi_trades = api.stock.trades.get_trades_multi(
    symbols=["AAPL", "MSFT", "GOOGL"],
    start="2024-01-15T09:30:00Z",
    end="2024-01-15T10:00:00Z",
    limit=10
)

for symbol, trades_data in multi_trades.items():
    print(f"{symbol}: {len(trades_data.trades)} trades")

# Get all trades with automatic pagination
all_trades = api.stock.trades.get_all_trades(
    symbol="SPY",
    start="2024-01-15T09:30:00Z",
    end="2024-01-15T09:35:00Z"
)
print(f"Total SPY trades: {len(all_trades)}")

# Use different data feeds (requires subscription)
sip_trades = api.stock.trades.get_trades(
    symbol="AAPL",
    start="2024-01-15T09:30:00Z",
    end="2024-01-15T10:00:00Z",
    feed="sip"  # or "iex", "otc"
)
```

### Advanced Order Types

```python
# Stop-loss order
stop_loss = api.trading.orders.stop(
    symbol="TSLA",
    qty=1,
    side="sell",
    stop_price=180.00
)

# Trailing stop order
trailing_stop = api.trading.orders.trailing_stop(
    symbol="NVDA",
    qty=1,
    side="sell",
    trail_percent=5.0  # 5% trailing stop
)

# One-Cancels-Other (OCO) order
oco_order = api.trading.orders.market(
    symbol="AAPL",
    qty=1,
    side="buy",
    take_profit=200.00,
    stop_loss=150.00
)
```

### Market Hours & Calendar

```python
# Check if market is open
clock = api.trading.market.clock()
print(f"Market is {'open' if clock.is_open else 'closed'}")
print(f"Next open: {clock.next_open}")
print(f"Next close: {clock.next_close}")

# Get market calendar
calendar = api.trading.market.calendar(
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

## 🧪 Testing

The project includes comprehensive test coverage. Run tests using:

```bash
# Run all tests
./test.sh

# Run specific test file
./test.sh tests/test_trading/test_orders.py

# Run with coverage
uv run pytest --cov=py_alpaca_api --cov-report=html

# Run with markers
uv run pytest -m "not slow"  # Skip slow tests
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --all-extras --dev

# Install pre-commit hooks
pre-commit install

# Run code quality checks
make check

# Format code
make format

# Run type checking
make type-check

# Run linting
make lint
```

### Code Quality Tools

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checker with strict mode
- **Pre-commit**: Git hooks for code quality
- **Pytest**: Testing framework with coverage

### Project Structure

```
py-alpaca-api/
├── src/py_alpaca_api/
│   ├── __init__.py           # Main API client
│   ├── exceptions.py         # Custom exceptions
│   ├── trading/              # Trading operations
│   │   ├── account.py        # Account management
│   │   ├── orders.py         # Order management
│   │   ├── positions.py      # Position tracking
│   │   ├── watchlists.py     # Watchlist operations
│   │   ├── market.py         # Market data
│   │   ├── news.py           # Financial news
│   │   └── recommendations.py # Stock analysis
│   ├── stock/                # Stock market data
│   │   ├── assets.py         # Asset information
│   │   ├── history.py        # Historical data
│   │   ├── screener.py       # Stock screening
│   │   ├── predictor.py      # ML predictions
│   │   └── latest_quote.py   # Real-time quotes
│   ├── models/               # Data models
│   └── http/                 # HTTP client
├── tests/                    # Test suite
├── docs/                     # Documentation
└── pyproject.toml           # Project configuration
```

## 📖 Documentation

Full documentation is available at [Read the Docs](https://py-alpaca-api.readthedocs.io)

### API Reference

- [Trading API](https://py-alpaca-api.readthedocs.io/en/latest/trading/) - Orders, positions, and account management
- [Market Data API](https://py-alpaca-api.readthedocs.io/en/latest/market_data/) - Historical and real-time data
- [Stock Analysis](https://py-alpaca-api.readthedocs.io/en/latest/analysis/) - Screeners, predictions, and sentiment
- [Models](https://py-alpaca-api.readthedocs.io/en/latest/models/) - Data models and type definitions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow the existing code style (enforced by ruff)
- Add type hints to all functions
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Alpaca Markets](https://alpaca.markets/) for providing the trading API
- [Prophet](https://facebook.github.io/prophet/) for time series forecasting
- [yfinance](https://github.com/ranaroussi/yfinance) for market data
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for web scraping
- All contributors who have helped improve this project

## 📞 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/TexasCoding/py-alpaca-api/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/TexasCoding/py-alpaca-api/discussions)
- 📖 **Wiki**: [GitHub Wiki](https://github.com/TexasCoding/py-alpaca-api/wiki)

## 🚦 Project Status

![Tests](https://github.com/TexasCoding/py-alpaca-api/workflows/CI/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Last Commit](https://img.shields.io/github/last-commit/TexasCoding/py-alpaca-api)
![Issues](https://img.shields.io/github/issues/TexasCoding/py-alpaca-api)

## 🗺️ Roadmap

- [ ] WebSocket support for real-time data streaming
- [ ] Options trading support
- [ ] Crypto trading integration
- [ ] Advanced portfolio analytics
- [ ] Backtesting framework
- [ ] Strategy automation tools
- [ ] Mobile app integration

## ⚠️ Disclaimer

This software is for educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

Always start with paper trading to test your strategies before using real money.

---

<p align="center">Made with ❤️ by the py-alpaca-api team</p>
<p align="center">
  <a href="https://github.com/TexasCoding/py-alpaca-api">
    <img src="https://img.shields.io/github/stars/TexasCoding/py-alpaca-api?style=social" alt="GitHub Stars">
  </a>
</p>
