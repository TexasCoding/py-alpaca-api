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
        """Initialize PyAlpacaApi class

        Parameters:
        -----------
        api_key:    Alpaca API Key
                    A valid Alpaca API Key string required

        api_secret: Alpaca API Secret
                    A valid Alpaca API Secret string required

        api_paper:  Alpaca Paper Trading
                    Alpaca Paper Trading (default: True) bool

        Raises:
        -------
        ValueError:
            ValueError if API Key is not provided

        ValueError:
            ValueError if API Secret is not provided

        Example:
        --------
        >>> PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
        PyAlpacaApi()
        """  # noqa
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
        """Get historical stock data for a given symbol

        Parameters:
        -----------
        symbol:     Stock symbol
                    A valid stock symbol (e.g., AAPL) string required

        start:      Start date for historical data
                    A valid start date string in the format "YYYY-MM-DD" required

        end:        End date for historical data
                    A valid end date string in the format "YYYY-MM-DD" required

        timeframe:  Timeframe for historical data
                    (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1m) (default: 1d) (optional)

        feed:       Data feed source
                    (iex, sip, tops, last, hist) (default: iex) (optional)

        currency:   Currency for historical data (default: USD)
                    Supported currencies: USD, CAD, EUR, GBP, JPY, AUD, CNY, HKD

        limit:      Limit number of data points (default: 1000)
                    Maximum number of data points to return (optional) int

        sort:       Sort order (asc, desc) (default: asc)

        adjustment: Adjustment for historical data (raw, split, dividends) (default: raw)

        Returns:
        --------
        DataFrame:  Historical stock data as a DataFrame with columns:
                    symbol, date, open, high, low, close, volume, trade_count, vwap

        Raises:
        -------
        Exception:
            Exception if failed to get historical stock data

        ValueError:
            ValueError if symbol is not a stock

        ValueError:
            ValueError if invalid timeframe

        ValueError:
            ValueError if no data available for symbol

        Example:
        --------
        >>> get_stock_historical_data(symbol="AAPL", start="2021-01-01", end="2021-12-31", timeframe="1d")
            symbol  close   high    low     trade_count open    date        volume      vwap
        0   AAPL    132.69  133.61  132.16  1           133.52  2021-01-04  100620780   132.69

        >>> get_stock_historical_data(symbol="FAKESYMBOL", start="2021-01-01", end="2021-12-31", timeframe="1d")
        ValueError: Failed to get asset information. Response: {"code":40410001,"message":"symbol not found: FAKESYMBOL"}
        """  # noqa
        # Get asset information for the symbol
        try:
            asset = self.get_asset(symbol)
        # Raise exception if failed to get asset information
        except Exception as e:
            raise ValueError(e)
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
        """Get order information by order ID

        Parameters:
        -----------
        order_id:   Order ID to get information
                    A valid order ID string required

        nested:     Include nested information (default: False)
                    Include nested information in the response (optional) bool

        Returns:
        --------
        OrderClass: Order information as an OrderClass object with values:
                    id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, notional, qty, filled_qty, filled_avg_price,
                    order_class, order_type

        Raises:
        -------
        ValueError: 
            ValueError if failed to get order information
        
        Example:
        --------
        >>> get_order_by_id(order_id="ORDER_ID")
        OrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='market')
        """  # noqa
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
        """Cancel order by order ID

        Parameters:
        -----------
        order_id:   Order ID to cancel
                    A valid order ID string required

        Returns:
        --------
        str:        Order cancellation confirmation message

        Raises:
        -------
        Exception:
            Exception if failed to cancel order

        Example:
        --------
        >>> cancel_order_by_id(order_id="ORDER_ID")
        'Order ORDER_ID has been cancelled'
        """  # noqa
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
        """Cancel all orders

        Returns:
        --------
        str:        Order cancellation confirmation message

        Raises:
        -------
        Exception:
            Exception if failed to cancel all orders
        """  # noqa
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
        """Submit a market order

        Parameters:
        -----------
        symbol:         Asset symbol to buy/sell
                        A valid asset symbol string required
        
        qty:            Quantity of asset to buy/sell (default: None)
                        Quantity of asset to buy/sell (optional) float

        notional:       Notional value of asset to buy/sell (default: None)
                        Notional value of asset to buy/sell (optional) float
                    
        side:           Order side (buy/sell) (default: buy)
                        Order side (buy/sell) (optional) str
                    
        time_in_force:  Time in force options (day, gtc, opg, cls, ioc, fok) (default: day)
                        Time in force options (optional) str

        extended_hours: Extended hours trading (default: False)
                        Extended hours trading (optional) bool

        Returns:
        --------
        MarketOrderClass: Market order information as a MarketOrderClass object with
                            values: id, client_order_id, created_at, submitted_at, asset_id, symbol, \
                            asset_class, notional, qty, filled_qty, filled_avg_price, order_class, \
                            order_type , limit_price, stop_price, filled_qty, filled_avg_price, \
                            status, type, side, time_in_force, extended_hours

        Raises:
        -------
        Exception: 
            Exception if failed to submit market order

        Example:
        --------
        >>> market_order(symbol="AAPL", qty=10)
        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='market')

        >>> market_order(symbol="AAPL", notional=1000)
        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='market')
        """  # noqa
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
        """Submit a Limit Order

        Parameters:
        -----------
        symbol:         Asset symbol to buy/sell
                        A valid asset symbol string required

        limit_price:    Limit price for the order
                        Limit price for the order float required
                
        qty:            Quantity of asset to buy/sell (default: None)
                        Quantity of asset to buy/sell (optional) float

        notional:       Notional value of asset to buy/sell (default: None)
                        Notional value of asset to buy/sell (optional) float

        side:           Order side (buy/sell) (default: buy)
                        Order side (buy/sell) (optional) str

        time_in_force:  Time in force options (day, gtc, opg, cls, ioc, fok) (default: day)
                        Time in force options (optional) str

        extended_hours: Extended hours trading (default: False)
                        Extended hours trading (optional) bool

        Returns:
        --------
        MarketOrderClass: Market order information as a MarketOrderClass object with
                            values: id, client_order_id, created_at, submitted_at, asset_id, symbol, \
                            asset_class, notional, qty, filled_qty, filled_avg_price, order_class, \
                            order_type , limit_price, stop_price, filled_qty, filled_avg_price, \
                            status, type, side, time_in_force, extended_hours
        
        Raises:
        -------
        Exception: 
            Exception if failed to submit limit order
        
        Example:
        --------
        >>> limit_order(symbol="AAPL", limit_price=100, qty=10)
        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='limit', \
                limit_price=100.0, stop_price=None, status='new', side='buy', time_in_force='day', extended_hours=False)

        >>> limit_order(symbol="AAPL", limit_price=100, notional=1000)
        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='limit', \
                limit_price=100.0, stop_price=None, status='new', side='buy', time_in_force='day', extended_hours=False)
        """  # noqa
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
        """Submit a Stop Order

        Parameters:
        -----------
        symbol:         Asset symbol to buy/sell
                        A valid asset symbol string required

        stop_price:     Stop price for the order
                        Stop price for the order float required

        qty:            Quantity of asset to buy/sell
                        Quantity of asset to buy/sell float required

        side:           Order side (buy/sell) (default: buy)
                        Order side (buy/sell) (optional) str

        time_in_force:  Time in force options (day, gtc, opg, cls, ioc, fok) (default: day) 
                        Time in force options (optional) str

        extended_hours: Extended hours trading (default: False) 
                        Extended hours trading (optional) bool

        Returns:
        --------
        MarketOrderClass: Market order information as a MarketOrderClass object with
                            values: id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, 
                            notional, qty, filled_qty, filled_avg_price, order_class, order_type , limit_price, 
                            stop_price, filled_qty, filled_avg_price, status, type, side, time_in_force, extended_hours

        Raises: 
        -------
        Exception: 
            Exception if failed to submit stop order

        Example:    
        --------
        >>> stop_order(symbol="AAPL", stop_price=100, qty=10)
        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='stop', \
                limit_price=None, stop_price=100.0, status='new', side='buy', time_in_force='day', extended_hours=False)

        >>> stop_order(symbol="AAPL", stop_price=100, qty=10, side="sell")
        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='stop', \
                limit_price=None, stop_price=100.0, status='new', side='sell', time_in_force='day', extended_hours=False)
        """  # noqa
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
        """Get asset information by symbol

        Parameters:
        -----------
        symbol:     Asset symbol to get information
                    A valid asset symbol string required

        Returns:
        --------
        AssetClass: Asset information as an AssetClass object with values:
                    id, class, exchange, symbol, status, tradable, marginable, shortable, easy_to_borrow
                
        Raises:
        -------
        ValueError: 
            ValueError if failed to get asset information

        Example:
        --------
        >>> get_asset(symbol="AAPL")
        AssetClass(id='ASSET_ID', class='us_equity', exchange='NASDAQ', symbol='AAPL', status='active', \
                    tradable=True, marginable=True, shortable=True, easy_to_borrow=True)

        """  # noqa
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
