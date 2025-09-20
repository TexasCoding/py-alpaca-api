# Trading Module

The trading module provides comprehensive access to all trading-related operations in the Alpaca API.

```{toctree}
:maxdepth: 2

account
orders
positions
watchlists
market
news
recommendations
corporate_actions
```

## Overview

The trading module is organized into the following components:

- **Account**: Account management and configuration
- **Orders**: Order execution and management
- **Positions**: Position tracking and management
- **Watchlists**: Create and manage watchlists
- **Market**: Market hours and calendar information
- **News**: Financial news aggregation
- **Recommendations**: Analyst recommendations and sentiment
- **Corporate Actions**: Dividends, splits, and mergers

## Quick Example

```python
from py_alpaca_api import PyAlpacaAPI

api = PyAlpacaAPI(
    api_key="your_api_key",
    api_secret="your_secret_key",
    api_paper=True
)

# Access trading functionality
account = api.trading.account.get()
orders = api.trading.orders.get_all()
positions = api.trading.positions.get_all()
```
