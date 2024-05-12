import json

import pandas as pd
import requests

from .src.data_classes import (
    account_class_from_dict,
    asset_class_from_dict,
    order_class_from_dict,
)


# PyAlpacaApi class
class PyAlpacaApi:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True):
        """
        PyAlpacaApi class constructor
        api_key: Alpaca API Key, required
        api_secret: Alpaca API Secret, required
        api_paper: Use Alpaca Paper Trading API (default: True)
        """
        # Check if API Key and Secret are provided
        if not api_key:
            raise ValueError("API Key is required")
        if not api_secret:
            raise ValueError("API Secret is required")
        # Set the API Key and Secret
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
        }
        # Set the API URL's
        if api_paper:
            self.trade_url = "https://paper-api.alpaca.markets/v2"
        else:
            self.trade_url = "https://api.alpaca.markets/v2"

        self.data_url = "https://data.alpaca.markets/v2"

    #################################################
    ########## Alpaca API Data Functions  ###########
    #################################################

    ############################
    # Get Stock Historical Data
    ############################
    def get_stock_historical_data(
        self,
        symbol,
        start,
        end,
        timeframe="1d",
        feed="iex",
        currency="USD",
        limit=1000,
        sort="asc",
        adjustment="raw",
    ):
        """
        Get historical stock data for a given symbol
        symbol: Stock symbol to get historical data
        start: Start date for historical data (YYYY-MM-DD)
        end: End date for historical data (YYYY-MM-DD)
        timeframe: Timeframe for historical data (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1m)
        feed: Data feed source (iex, sip, tops, last, hist) (default: iex)
        currency: Currency for historical data (default: USD)
        limit: Limit number of data points (default: 1000)
        sort: Sort order (asc, desc) (default: asc)
        adjustment: Adjustment for historical data (raw, split, dividends) (default: raw)
        return: Historical stock data as a DataFrame
        Exception: ValueError if failed to get asset information
        ValueError: ValueError if symbol is not a stock
        ValueError: ValueError if invalid timeframe
        ValueError: ValueError if no data available for symbol
        """
        # Get asset information for the symbol
        try:
            asset = self.get_asset(symbol)
        # Raise exception if failed to get asset information
        except Exception as e:
            raise ValueError(f"Error getting asset: {e}")
        else:
            # Check if asset is a stock
            if asset.asset_class != "us_equity":
                # Raise exception if asset is not a stock
                raise ValueError(f"{symbol} is not a stock.")
        # URL for historical stock data request
        url = f"{self.data_url}/stocks/{symbol}/bars"
        # Set timeframe
        match timeframe:
            case "1m":
                timeframe = "1Min"
            case "5m":
                timeframe = "5Min"
            case "15m":
                timeframe = "15Min"
            case "30m":
                timeframe = "30Min"
            case "1h":
                timeframe = "1Hour"
            case "4h":
                timeframe = "4Hour"
            case "1d":
                timeframe = "1Day"
            case "1w":
                timeframe = "1Week"
            case "1m":
                timeframe = "1Month"
            case _:
                # Raise exception if invalid timeframe is provided
                raise ValueError('Invalid timeframe. Must be "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", or "1m"')
        # Parameters for historical stock data request
        params = {
            "timeframe": timeframe,  # Timeframe for historical data, default: 1d
            "start": start,  # Start date for historical data
            "end": end,  # End date for historical data
            "currency": currency,  # Currency for historical data, default: USD
            "limit": limit,  # Limit number of data points, default: 1000
            "adjustment": adjustment,  # Adjustment for historical data, default: raw
            "feed": feed,  # Data feed source, default: iex
            "sort": sort,  # Sort order, default: asc
        }
        # Get historical stock data from Alpaca API
        response = requests.get(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code != 200:
            # Raise exception if response is not successful
            raise Exception(json.loads(response.text)["message"])
        # Convert JSON response to dictionary
        res_json = json.loads(response.text)["bars"]
        # Check if data is available
        if not res_json:
            raise ValueError(f"No data available for {symbol}.")
        # Normalize JSON response and convert to DataFrame
        bar_data_df = pd.json_normalize(res_json)
        # Add symbol column to DataFrame
        bar_data_df.insert(0, "symbol", symbol)
        # Reformat date column
        bar_data_df["t"] = pd.to_datetime(bar_data_df["t"].replace("[A-Za-z]", " ", regex=True))
        # Rename columns for consistency
        bar_data_df.rename(
            columns={
                "t": "date",
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "v": "volume",
                "n": "trade_count",
                "vw": "vwap",
            },
            inplace=True,
        )
        # Convert columns to appropriate data types
        bar_data_df = bar_data_df.astype(
            {
                "open": "float",
                "high": "float",
                "low": "float",
                "close": "float",
                "symbol": "str",
                "date": "datetime64[ns]",
                "vwap": "float",
                "trade_count": "int",
                "volume": "int",
            }
        )
        # Return historical stock data as a DataFrame
        return bar_data_df

    ########################################################
    ######### Alpaca API Order Functions  ##################
    ########################################################
    #########################################################
    # \\\\\\\\\/////////  Get Order BY id \\\\\\\///////////#
    #########################################################
    def get_order_by_id(self, order_id: str, nested: bool = False):
        """
        Get order information by order ID
        order_id: Order ID to get information
        nested: Include nested objects (default: False)
        return: OrderClass object with order information
        Exception: Exception if failed to get order information
        """
        # Parameters for the request
        params = {"nested": nested}
        # Alpaca API URL for order information
        url = f"{self.trade_url}/orders/{order_id}"
        # Get request to Alpaca API for order information
        response = requests.get(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return order information as an OrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise ValueError(f'Failed to get order information. Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\\ Cancel Order By ID /////////////////#
    ########################################################
    def cancel_order_by_id(self, order_id: str):
        """
        Cancel order by order ID
        order_id: Order ID to cancel
        return: Order cancellation message
        Exception: Exception if failed to cancel order
        """
        # Alpaca API URL for canceling an order
        url = f"{self.trade_url}/orders/{order_id}"
        # Delete request to Alpaca API for canceling an order
        response = requests.delete(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 204:
            # Convert JSON response to dictionary
            return f"Order {order_id} has been cancelled"
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to cancel order {order_id}, Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\  Cancel All Orders //////////////////#
    ########################################################
    def cancel_all_orders(self):
        """
        Cancel all orders
        return: Number of orders cancelled
        Exception: Exception if failed to cancel orders
        """
        # Alpaca API URL for canceling all orders
        url = f"{self.trade_url}/orders"
        # Delete request to Alpaca API for canceling all orders
        response = requests.delete(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 207:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            return f"{len(res)} orders have been cancelled"
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to cancel orders. Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Market Order ////////////////#
    ########################################################
    def market_order(
        self,
        symbol: str,
        qty: float = None,
        notional: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ):
        """
        Submit a market order
        symbol: Asset symbol to buy/sell
        qty: Quantity of asset to buy/sell (default: None)
        notional: Notional value of asset to buy/sell (default: None)
        side: Order side (buy/sell) (default: buy)
        time_in_force: Time in force options (day, gtc, opg, cls, ioc, fok) (default: day)
        extended_hours: Extended hours trading (default: False)
        return: MarketOrderClass object with
        values: id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, notional, qty, filled_qty, filled_avg_price,
                order_class, order_type
        Exception: Exception if failed to submit market order
        """
        # Alpaca API URL for submitting market order
        url = f"{self.trade_url}/orders"
        # Market order payload
        payload = {
            "symbol": symbol,
            "qty": qty if qty else None,
            "notional": round(notional, 2) if notional else None,
            "side": side if side == "buy" else "sell",
            "type": "market",
            "time_in_force": time_in_force,
            "extended_hours": extended_hours,
        }
        # Post request to Alpaca API for submitting market order
        response = requests.post(url, headers=self.headers, json=payload)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return market order information as a MarketOrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to submit market order. Code: {response.status_code}, Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Limit Order /////////////////#
    ########################################################
    def limit_order(
        self,
        symbol: str,
        limit_price: float,
        qty: float = None,
        notional: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ):
        """
        Submit a limit order
        symbol: Asset symbol to buy/sell
        limit_price: Limit price for the order
        qty: Quantity of asset to buy/sell (default: None)
        notional: Notional value of asset to buy/sell (default: None)
        side: Order side (buy/sell) (default: buy)
        time_in_force: Time in force options (day, gtc, opg, cls, ioc, fok) (default: day)
        extended_hours: Extended hours trading (default: False)
        return: MarketOrderClass object with
        values: id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, notional, qty, filled_qty, filled_avg_price,
                order_class, order_type, limit_price, stop_price, filled_qty, filled_avg_price, status, type, side, time_in_force, extended_hours
        Exception: Exception if failed to submit limit order
        """
        # Alpaca API URL for submitting market order
        url = f"{self.trade_url}/orders"
        # Market order payload
        payload = {
            "symbol": symbol,  # Asset symbol to buy/sell
            "limit_price": limit_price,  # Limit price for the order
            "qty": (qty if qty else None),  # Check if qty is provided, if not, set to None
            "notional": (round(notional, 2) if notional else None),  # Round notional to 2 decimal places, if notional is provided
            "side": (side if side == "buy" else "sell"),  # Check if side is buy or sell
            "type": "limit",  # Order type is limit
            "time_in_force": time_in_force,  # Time in force options, default: day
            "extended_hours": extended_hours,  # Extended hours trading, default: False
        }
        # Post request to Alpaca API for submitting market order
        response = requests.post(url, headers=self.headers, json=payload)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return market order information as a MarketOrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to submit limit order. Code: {response.status_code}, Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Stop Order /////////////////#
    ########################################################
    def stop_order(
        self,
        symbol: str,
        stop_price: float,
        qty: float,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ):
        """
        Submit a Stop Order
        symbol: Asset symbol to buy/sell
        stop_price: Stop price for the order
        qty: Quantity of asset to buy/sell
        side: Order side (buy/sell) (default: buy)
        time_in_force: Time in force options (day, gtc, opg, cls, ioc, fok) (default: day)
        extended_hours: Extended hours trading (default: False)
        return: MarketOrderClass object with
        values: id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, notional, qty, filled_qty, filled_avg_price,
                order_class, order_type, limit_price, stop_price, filled_qty, filled_avg_price, status, type, side, time_in_force, extended_hours
        Exception: Exception if failed to submit stop order
        """
        # Alpaca API URL for submitting market order
        url = f"{self.trade_url}/orders"
        # Market order payload
        payload = {
            "symbol": symbol,  # Asset symbol to buy/sell
            "stop_price": stop_price,  # Stop price for the order
            "qty": qty,  # Quantity of asset to buy/sell
            "side": (side if side == "buy" else "sell"),  # Check if side is buy or sell
            "type": "stop",  # Order type is stop
            "time_in_force": time_in_force,  # Time in force options, default: day
            "extended_hours": extended_hours,  # Extended hours trading, default: False
        }
        # Post request to Alpaca API for submitting market order
        response = requests.post(url, headers=self.headers, json=payload)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return market order information as a MarketOrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to submit limit order. Code: {response.status_code}, Response: {res["message"]}')

    #####################################################
    # \\\\\\\\\\\\\\\\\\\  Get Asset ////////////////////#
    #####################################################
    def get_asset(self, symbol: str):
        """
        Get asset information
        symbol: Asset symbol
        return: AssetClass object with
        values: id, class, exchange, symbol, status, tradable, marginable, shortable, easy_to_borrow, fractionable
        Execption: ValueError if failed to get asset information
        """
        # Alpaca API URL for asset information
        url = f"{self.trade_url}/assets/{symbol}"
        # Get request to Alpaca API for asset information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return asset information as an AssetClass object
            return asset_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise ValueError(f"Failed to get asset information. Response: {response.text}")

    ########################################################
    # \\\\\\\\\\\\\  Get Account Information ///////////////#
    ########################################################
    def get_account(self):
        """
        Get account information
        return: AccountClass object with account information
        values: id, admin_configurations, user_configurations, account_number, status, crypto_status, options_approved_level,
                options_trading_level, currency, buying_power, regt_buying_power, daytrading_buying_power, effective_buying_power,
                non_marginable_buying_power, options_buying_power, bod_dtbp, cash, accrued_fees, pending_transfer_in, portfolio_value,
                pattern_day_trader, trading_blocked, transfers_blocked, account_blocked, created_at, trade_suspended_by_user, multiplier,
                shorting_enabled, equity, last_equity, long_market_value, short_market_value, position_market_value, initial_margin,
                maintenance_margin, last_maintenance_margin, sma, daytrade_count, balance_asof, crypto_tier, intraday_adjustments,
                pending_reg_taf_fees
        Exception: Exception if failed to get account information
        """
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
