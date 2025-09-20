# Installation

## Requirements

- Python 3.10 or higher
- Alpaca API credentials (paper trading credentials for testing)
- Optional: Redis server for advanced caching

## Install from PyPI

```bash
pip install py-alpaca-api
```

## Install from Source

```bash
# Clone the repository
git clone https://github.com/TexasCoding/py-alpaca-api.git
cd py-alpaca-api

# Install with pip
pip install -e .

# Or install with uv (recommended for development)
uv sync --all-extras --dev
```

## Verify Installation

```python
from py_alpaca_api import PyAlpacaAPI

# Create an instance with your credentials
api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    api_paper=True  # Use paper trading
)

# Test the connection
account = api.trading.account.get()
print(f"Account status: {account.status}")
```

## Optional Dependencies

### Redis Cache

For production environments, Redis caching is recommended:

```bash
pip install py-alpaca-api[redis]
```

### Development Dependencies

For contributing to the project:

```bash
pip install py-alpaca-api[dev]
```

## Environment Variables

Create a `.env` file in your project root:

```bash
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
ALPACA_API_PAPER=true  # Set to false for live trading
```

## Next Steps

- Read the [Quickstart Guide](quickstart.md) to start using PyAlpacaAPI
- Explore the [API Reference](api/modules.rst) for detailed documentation
- Check out [Examples](examples/index.md) for common use cases
