# GEMINI.md

This file provides guidance to Gemini (gemini.google.com) when working with code in this repository.

## Development Commands

### Package Management
This project uses `uv` for dependency management (migrated from Poetry).

```bash
# Install dependencies
uv sync --all-extras --dev

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

### Testing
```bash
# Run all tests
uv run pytest tests

# Run tests quietly
uv run pytest -q tests

# Run specific test file
uv run pytest tests/test_trading/test_orders.py

# Run with test script (includes API keys)
./test.sh

# Run specific tests with test script
./test.sh tests/test_trading/test_orders.py
```

### Code Quality
```bash
# Run linter
uv run ruff check

# Run linter with auto-fix
uv run ruff check --fix

# Format code
uv run ruff format
```

## Architecture Overview

### Core API Structure
The repository implements a Python wrapper for the Alpaca Trading API with the following architecture:

1. **Main Entry Point**: `PyAlpacaAPI` class in `src/py_alpaca_api/__init__.py`
   - Initializes with API key, secret, and paper trading flag
   - Provides access to `trading` and `stock` modules

2. **Trading Module** (`src/py_alpaca_api/trading/`)
   - `account.py`: Account information, activities, and portfolio history
   - `orders.py`: Order management and execution
   - `positions.py`: Position tracking and management
   - `watchlists.py`: Watchlist CRUD operations
   - `market.py`: Market clock and calendar data
   - `news.py`: Financial news from Yahoo Finance and Benzinga
   - `recommendations.py`: Stock recommendations and sentiment analysis

3. **Stock Module** (`src/py_alpaca_api/stock/`)
   - `assets.py`: Asset information retrieval
   - `history.py`: Historical stock data
   - `screener.py`: Stock screening for gainers/losers
   - `predictor.py`: Prophet-based stock prediction
   - `latest_quote.py`: Real-time quote data

4. **Models** (`src/py_alpaca_api/models/`)
   - Dataclass models for all API entities
   - `model_utils.py`: Utility functions for data transformation
   - Consistent pattern: each model has a `from_dict()` function

5. **HTTP Layer** (`src/py_alpaca_api/http/`)
   - `requests.py`: Centralized HTTP request handling with retry logic
   - Configurable retry strategies for resilient API communication

### Key Design Patterns

1. **Modular Architecture**: Each domain (trading, stock, models) is self-contained
2. **Dataclass Models**: All API responses are converted to typed dataclasses
3. **Centralized HTTP**: Single point for API communication with built-in resilience
4. **Factory Pattern**: `from_dict()` methods for model instantiation

### API Authentication
- Requires `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` environment variables
- Supports both paper and live trading environments
- Test script includes default paper trading credentials

### External Dependencies
- **Data Processing**: pandas, numpy
- **Time Handling**: pendulum
- **Stock Prediction**: prophet
- **Web Scraping**: beautifulsoup4
- **Market Data**: yfinance
- **HTTP**: requests with caching and rate limiting

## Testing Approach

Tests are organized by module:
- `test_http/`: HTTP request handling tests
- `test_models/`: Model creation and transformation tests
- `test_stock/`: Stock module functionality tests
- `test_trading/`: Trading operations tests

All tests require API credentials (can use paper trading credentials).
