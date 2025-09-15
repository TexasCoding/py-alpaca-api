# CLAUDE.md

This file provides comprehensive guidance to Claude Code (claude.ai/code) and other AI assistants when working with the py-alpaca-api codebase.

## 🎯 Project Overview

**py-alpaca-api** is a modern Python wrapper for the Alpaca Trading API that provides:
- Complete trading operations (orders, positions, account management)
- Market data access (historical, real-time quotes, news)
- Stock analysis tools (screeners, ML predictions, sentiment)
- Full type safety with mypy strict mode
- Comprehensive test coverage (109+ tests)

**Current Version**: 2.2.0
**Python Support**: 3.10+
**License**: MIT

## 🛠️ Development Setup

### Prerequisites
- Python 3.10 or higher
- uv package manager (recommended) or pip
- Alpaca API credentials (paper trading credentials for testing)

### Initial Setup
```bash
# Clone and enter the repository
git clone https://github.com/TexasCoding/py-alpaca-api.git
cd py-alpaca-api

# Install dependencies with uv (recommended)
uv sync --all-extras --dev

# Or with pip
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Set up environment variables (create .env file)
echo "ALPACA_API_KEY=your_api_key" >> .env
echo "ALPACA_SECRET_KEY=your_secret_key" >> .env
```

## 📝 Development Commands

### Package Management
```bash
# Install all dependencies
uv sync --all-extras --dev

# Add a runtime dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Update dependencies
uv lock --upgrade

# Show dependency tree
uv tree
```

### Testing
```bash
# Run all tests with API credentials
./test.sh

# Run specific test file
./test.sh tests/test_trading/test_orders.py

# Run tests with pytest directly
uv run pytest tests

# Run with coverage report
uv run pytest --cov=py_alpaca_api --cov-report=html

# Run tests quietly
uv run pytest -q tests

# Run tests with markers
uv run pytest -m "not slow"
```

### Code Quality
```bash
# Run all quality checks (recommended before committing)
make check

# Format code
make format
uv run ruff format src tests

# Lint code
make lint
uv run ruff check --fix

# Type checking
make type-check
uv run mypy src

# Run pre-commit hooks manually
pre-commit run --all-files
```

### Development Workflow
```bash
# Common development workflow
make format          # Format code
make check           # Run all checks
./test.sh           # Run tests
git add .           # Stage changes
git commit          # Commit (triggers pre-commit hooks)
```

## 🏗️ Architecture

### Project Structure
```
py-alpaca-api/
├── src/py_alpaca_api/
│   ├── __init__.py              # Main PyAlpacaAPI class
│   ├── exceptions.py            # Custom exception hierarchy
│   ├── trading/                 # Trading operations
│   │   ├── __init__.py         # Trading module exports
│   │   ├── account.py          # Account management
│   │   ├── orders.py           # Order execution & management
│   │   ├── positions.py        # Position tracking
│   │   ├── watchlists.py       # Watchlist CRUD
│   │   ├── market.py           # Market hours & calendar
│   │   ├── news.py             # Financial news aggregation
│   │   └── recommendations.py  # Stock sentiment analysis
│   ├── stock/                   # Market data & analysis
│   │   ├── __init__.py         # Stock module exports
│   │   ├── assets.py           # Asset information
│   │   ├── history.py          # Historical data retrieval
│   │   ├── screener.py         # Gainers/losers screening
│   │   ├── predictor.py        # ML predictions (Prophet)
│   │   └── latest_quote.py     # Real-time quotes
│   ├── models/                  # Data models
│   │   ├── account_model.py    # Account dataclass
│   │   ├── order_model.py      # Order dataclass
│   │   ├── position_model.py   # Position dataclass
│   │   ├── asset_model.py      # Asset dataclass
│   │   ├── watchlist_model.py  # Watchlist dataclass
│   │   ├── quote_model.py      # Quote dataclass
│   │   ├── clock_model.py      # Market clock dataclass
│   │   └── model_utils.py      # Conversion utilities
│   └── http/                    # HTTP layer
│       └── requests.py          # Request handling with retries
├── tests/                       # Test suite
│   ├── test_trading/           # Trading tests
│   ├── test_stock/             # Stock tests
│   ├── test_models/            # Model tests
│   └── test_http/              # HTTP tests
├── docs/                        # Documentation
├── .github/                     # GitHub Actions CI/CD
├── pyproject.toml              # Project configuration
├── Makefile                    # Development tasks
├── test.sh                     # Test runner script
└── README.md                   # User documentation
```

### Key Design Patterns

1. **Factory Pattern**: All models use `from_dict()` methods for instantiation
   ```python
   order = order_class_from_dict(api_response_dict)
   ```

2. **Module Organization**: Clear separation of concerns
   - `trading/`: All trading-related operations
   - `stock/`: Market data and analysis
   - `models/`: Data structures only
   - `http/`: Network communication

3. **Exception Hierarchy**: Custom exceptions for better error handling
   ```python
   PyAlpacaAPIError (base)
   ├── AuthenticationError
   ├── APIRequestError
   └── ValidationError
   ```

4. **Type Safety**: Full type annotations throughout
   ```python
   def market(
       self,
       symbol: str,
       qty: float | None = None,
       notional: float | None = None,
       side: str = "buy",
       take_profit: float | None = None,
       stop_loss: float | None = None,
   ) -> OrderModel:
   ```

## 🔑 API Authentication

### Environment Variables
```bash
# Required for all API operations
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here

# Optional - defaults to paper trading
ALPACA_API_PAPER=true  # Set to false for live trading
```

### Authentication Flow
1. API credentials are passed to `PyAlpacaAPI` constructor
2. Headers are set with authentication tokens
3. All requests include authentication headers
4. 401 errors raise `AuthenticationError`

## 📊 Data Flow

### Request Flow
```
User Code → PyAlpacaAPI → Trading/Stock Module → HTTP Layer → Alpaca API
                                                       ↓
User Code ← Model Object ← from_dict() ← JSON Response
```

### Model Conversion
1. API returns JSON response
2. `extract_class_data()` processes raw data
3. `from_dict()` creates typed model instance
4. Model returned to user with full type safety

## 🧪 Testing Guidelines

### Test Organization
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test API interactions
- **Mock Tests**: Use when API calls should be avoided

### Writing Tests
```python
# Use fixtures for common setup
@pytest.fixture
def alpaca():
    return PyAlpacaAPI(
        api_key=os.environ.get("ALPACA_API_KEY"),
        api_secret=os.environ.get("ALPACA_SECRET_KEY"),
        api_paper=True
    )

# Test naming convention
def test_feature_scenario_expected_result(alpaca):
    # Arrange
    symbol = "AAPL"

    # Act
    result = alpaca.stock.assets.get(symbol)

    # Assert
    assert result.symbol == symbol
```

### Test Data
- Use paper trading account for all tests
- Clean up test data after each test (cancel orders, etc.)
- Use small quantities/notional values to avoid account limits

## 🐛 Common Issues & Solutions

### Issue: ValidationError instead of ValueError
**Solution**: Use `ValidationError` from `exceptions.py` for input validation

### Issue: DataFrame type issues with pandas
**Solution**: Use explicit type assertions and `.copy()` to maintain DataFrame type
```python
df = df.loc[filter].copy()
assert isinstance(df, pd.DataFrame)
```

### Issue: Prophet seasonality parameters
**Solution**: Use "auto" string instead of boolean values
```python
yearly_seasonality="auto"  # Not True/False
```

### Issue: API returns different column counts
**Solution**: Handle dynamic columns gracefully
```python
if len(df.columns) >= expected_cols:
    df = df[expected_columns]
```

## 🚀 Best Practices

### Code Style
1. **Imports**: Use absolute imports from `py_alpaca_api`
2. **Type Hints**: Always include type annotations
3. **Docstrings**: Use Google style docstrings
4. **Line Length**: Maximum 88 characters (ruff default)
5. **Naming**: Use descriptive names, avoid abbreviations

### Error Handling
```python
# Good
try:
    result = api_call()
except APIRequestError as e:
    logger.error(f"API request failed: {e}")
    raise

# Bad
try:
    result = api_call()
except Exception:
    pass  # Never silent fail
```

### DataFrame Operations
```python
# Good - Preserve DataFrame type
df = df.loc[df["column"] > value].copy()

# Bad - May return Series
df = df[df["column"] > value]
```

### API Calls
1. Always handle rate limiting
2. Use paper trading for development
3. Validate inputs before API calls
4. Log API errors for debugging

## 📦 Dependencies

### Core Dependencies
- **pandas**: DataFrame operations, data analysis
- **numpy**: Numerical computations
- **requests**: HTTP client
- **pendulum**: Timezone-aware datetime handling
- **prophet**: Time series forecasting
- **yfinance**: Additional market data
- **beautifulsoup4**: HTML parsing for news

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking support
- **ruff**: Linting and formatting
- **mypy**: Static type checking
- **pre-commit**: Git hooks
- **hypothesis**: Property-based testing

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
1. **Triggered by**: Push to any branch, PRs to main
2. **Steps**:
   - Checkout code
   - Set up Python 3.10+
   - Install dependencies
   - Run linting (ruff)
   - Run type checking (mypy)
   - Run tests with coverage
   - Upload coverage reports

### Pre-commit Hooks
- `trailing-whitespace`: Remove trailing whitespace
- `end-of-file-fixer`: Ensure files end with newline
- `check-yaml`: Validate YAML files
- `check-json`: Validate JSON files
- `check-toml`: Validate TOML files
- `ruff`: Lint Python code
- `ruff-format`: Format Python code
- `mypy`: Type check Python code

## 📈 Performance Considerations

1. **Rate Limiting**: Alpaca API has rate limits, use caching when possible
2. **Batch Operations**: Combine multiple requests when feasible
3. **DataFrame Operations**: Use vectorized operations over loops
4. **Prophet Models**: Cache trained models for repeated predictions
5. **News Fetching**: Implement caching to avoid repeated scraping

## 🔒 Security

1. **Never commit credentials**: Use environment variables
2. **Validate user input**: Prevent injection attacks
3. **Use paper trading**: For development and testing
4. **Secure storage**: Use proper secret management in production
5. **API key rotation**: Regularly rotate API keys

## 📚 Additional Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/api-references/)
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

## 🎓 Learning Path

For new contributors:
1. Read the README.md for user perspective
2. Set up development environment
3. Run existing tests to understand functionality
4. Make small changes and run quality checks
5. Review existing code for patterns
6. Start with bug fixes before features

## 💡 Tips for AI Assistants

1. **Always run tests** after making changes
2. **Use type hints** in all new code
3. **Follow existing patterns** in the codebase
4. **Check pre-commit hooks** before committing
5. **Update tests** when changing functionality
6. **Document breaking changes** clearly
7. **Preserve backward compatibility** when possible
8. **Use descriptive commit messages**

---

*Last Updated: Version 2.2.0*
*Maintained by: py-alpaca-api team*
