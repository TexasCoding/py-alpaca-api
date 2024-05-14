import json

import requests

from .data_classes import AccountClass, account_class_from_dict


class Account:
    def __init__(self, trade_url: str, headers: object) -> None:
        self.trade_url = trade_url
        self.headers = headers

    ########################################################
    # \\\\\\\\\\\\\  Get Account Information ///////////////#
    ########################################################
    def get(self) -> AccountClass:
        """Get account information

        Returns:
        --------
        AccountClass: Account information as an AccountClass object with values:
                    id, account_number, status, currency, cash, cash_withdrawable, buying_power, regt_buying_power, daytrading_buying_power,
                    portfolio_value, pattern_day_trader, trading_blocked, transfers_blocked, account_blocked, created_at, trade_suspended_by_user,
                    multiplier, shorting_enabled, equity, last_equity, long_market_value, short_market_value, equity_previous_close, \
                    long_portfolio_value, short_portfolio_value, initial_margin, maintenance_margin, last_maintenance_margin, sma, daytrade_count, \
                    last_maintenance_margin, sma_held_for_orders, sma_held_for_positions, sma_held_for_options, created_at, updated_at

        Raises:
        -------
        Exception: 
            Exception if failed to get account information

        Example:
        --------
        >>> get_account()
        AccountClass(id='ACCOUNT_ID', account_number='ACCOUNT_NUMBER', status='ACTIVE', currency='USD', cash=1000.0, \
                    cash_withdrawable=1000.0, buying_power=1000.0, regt_buying_power=1000.0, \
                    daytrading_buying_power=1000.0, portfolio_value=1000.0, pattern_day_trader=False, \
                    trading_blocked=False, transfers_blocked=False, account_blocked=False, \
                    created_at='2021-10-01T00:00:00Z', trade_suspended_by_user=False, multiplier=1.0, \
                    shorting_enabled=True, equity=1000.0, last_equity=1000.0, long_market_value=0.0, \
                    short_market_value=0.0, equity_previous_close=1000.0, long_portfolio_value=0.0, \
                    short_portfolio_value=0.0, initial_margin=0.0, maintenance_margin=0.0, last_maintenance_margin=0.0, \
                    sma=0.0, daytrade_count=0, last_maintenance_margin=0.0, sma_held_for_orders=0.0, \
                    sma_held_for_positions=0.0, sma_held_for_options=0.0, created_at='2021-10-01T00:00:00Z', \
                    updated_at='2021-10-01T00:00:00Z')
        """  # noqa
        # Alpaca API URL for account information
        url = f"{self.trade_url}/account"
        # Get request to Alpaca API for account information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return account information as an AccountClass object
            return account_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise Exception(f"Failed to get account information. Response: {response.text}")
