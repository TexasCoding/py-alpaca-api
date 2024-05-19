import json

import requests

from .data_classes import OrderClass, order_class_from_dict


class Order:
    def __init__(self, trade_url: str, headers: object) -> None:
        """Initialize Order class

        Parameters:
        ___________
        trade_url: str
                Alpaca Trade API URL required

        headers: object
                API request headers required

        Raises:
        _______
        ValueError: If trade URL is not provided

        ValueError: If headers are not provided
        """  # noqa

        self.trade_url = trade_url
        self.headers = headers

    #########################################################
    # \\\\\\\\\/////////  Get Order BY id \\\\\\\///////////#
    #########################################################
    def get_by_id(self, order_id: str, nested: bool = False) -> OrderClass:
        """Get order information by order ID

        Parameters:
        -----------
        order_id:   Order ID to get information
                    A valid order ID string required

        nested:     Include nested objects (default: False)
                    Include nested objects (optional) bool

        Returns:
        --------
        OrderClass: Order information as an OrderClass object

        Raises:
        -------
        ValueError: If failed to get order information

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.get_by_id(order_id="ORDER_ID")
            print(order)

        OrderClass(
            id="ORDER_ID",
            client_order_id="CLIENT_ORDER_ID",
            created_at="2021-10-01T00:00:00Z",
            submitted_at="2021-10-01 00:00:00",
            asset_id="ASSET_ID",
            symbol="AAPL",
            asset_class="us_equity",
            notional=1000.0,
            qty=10.0,
            filled_qty=10.0,
            filled_avg_price=100.0,
            order_class="simple",
            order_type="market",
            limit_price=None,
            stop_price=None,
            status="new",
            side="buy",
            time_in_force="day",
            extended_hours=False
        )
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
    def cancel_by_id(self, order_id: str) -> str:
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
        Exception:  If failed to cancel order

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.cancel_by_id(order_id="ORDER_ID")
            print(order)

        Order ORDER_ID has been cancelled
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
    def cancel_all(self) -> str:
        """Cancel all orders

        Returns:
        --------
        str:        Order cancellation confirmation message

        Raises:
        -------
        Exception:  If failed to cancel all orders

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.cancel_all()
            print(order)

        10 orders have been cancelled
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
    def market(
        self,
        symbol: str,
        qty: float = None,
        notional: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:
        """Submit a Market Order

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
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.market(symbol="AAPL", qty=10)
            print(order)

        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='market', \
                limit_price=None, stop_price=None, status='new', side='buy', time_in_force='day', extended_hours=False)
        """  # noqa

        # Payload for market order
        payload = {
            "symbol": symbol,
            "qty": qty if qty else None,
            "notional": round(notional, 2) if notional else None,
            "side": side if side == "buy" else "sell",
            "type": "market",
            "time_in_force": time_in_force,
            "extended_hours": extended_hours,
        }
        # Return market order using submit order method
        return self.__submit_order(payload)

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Limit Order /////////////////#
    ########################################################
    def limit(
        self,
        symbol: str,
        limit_price: float,
        qty: float = None,
        notional: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:
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
                            values: id, client_order_id, created_at, submitted_at, asset_id, symbol, asset_class, 
                            notional, qty, filled_qty, filled_avg_price, order_class, order_type , limit_price, 
                            stop_price, filled_qty, filled_avg_price, status, type, side, time_in_force, extended_hours

        Raises:
        -------
        Exception: 
            Exception if failed to submit limit order

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.limit(symbol="AAPL", limit_price=100, qty=10)
            print(order)

        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='limit', \
                limit_price=100.0, stop_price=None, status='new', side='buy', time_in_force='day', extended_hours=False)

        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.limit(symbol="AAPL", limit_price=100, notional=1000)
            print(order)

        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='limit', \
                limit_price=100.0, stop_price=None, status='new', side='buy', time_in_force='day', extended_hours=False)

        """  # noqa

        # Payload for limit order
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
        # Return limit order using submit order method
        return self.__submit_order(payload)

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Stop Order /////////////////#
    ########################################################
    def stop(
        self,
        symbol: str,
        stop_price: float,
        qty: float,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:
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
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            order = api.order.stop(symbol="AAPL", stop_price=100, qty=10)
            print(order)

        MarketOrderClass(id='ORDER_ID', client_order_id='CLIENT_ORDER_ID', created_at='2021-10-01T00:00:00Z', \
                submitted_at='2021-10-01 00:00:00', asset_id='ASSET_ID', symbol='AAPL', asset_class='us_equity', \
                notional=1000.0, qty=10.0, filled_qty=10.0, filled_avg_price=100.0, order_class='simple', order_type='stop', \
                limit_price=None, stop_price=100.0, status='new', side='buy', time_in_force='day', extended_hours=False)

        """  # noqa

        # Payload for stop order
        payload = {
            "symbol": symbol,  # Asset symbol to buy/sell
            "stop_price": stop_price,  # Stop price for the order
            "qty": qty,  # Quantity of asset to buy/sell
            "side": (side if side == "buy" else "sell"),  # Check if side is buy or sell
            "type": "stop",  # Order type is stop
            "time_in_force": time_in_force,  # Time in force options, default: day
            "extended_hours": extended_hours,  # Extended hours trading, default: False
        }
        # Return stop order using submit order method
        return self.__submit_order(payload)

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Stop Order /////////////////#
    ########################################################
    def stop_limit(
        self,
        symbol: str,
        stop_price: float,
        limit_price: float,
        qty: float,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:
        """Submit a Stop Limit Order

        Parameters:
        -----------
        symbol:         Asset symbol to buy/sell
                        A valid asset symbol string required

        stop_price:     Stop price for the order
                        Stop price for the order float required

        limit_price:    Limit price for the order
                        Limit price for the order float required

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
        """  # noqa

        # Payload for stop order
        payload = {
            "symbol": symbol,  # Asset symbol to buy/sell
            "stop_price": stop_price,  # Stop price for the order
            "limit_price": limit_price,  # Limit price for the order
            "qty": qty,  # Quantity of asset to buy/sell
            "side": (side if side == "buy" else "sell"),  # Check if side is buy or sell
            "type": "stop_limit",  # Order type is stop
            "time_in_force": time_in_force,  # Time in force options, default: day
            "extended_hours": extended_hours,  # Extended hours trading, default: False
        }
        # Return stop order using submit order method
        return self.__submit_order(payload)

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Stop Order /////////////////#
    ########################################################
    def trailing_stop(
        self,
        symbol: str,
        qty: float,
        trail_percent: float = None,
        trail_price: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:
        """Submit a Trailing Stop Order

        Parameters:
        -----------
        symbol:         Asset symbol to buy/sell
                        A valid asset symbol string required

        qty:            Quantity of asset to buy/sell
                        Quantity of asset to buy/sell float required

        trail_percent:  Trailing stop percent
                        Trailing stop percent float optional

        trail_price:    Trailing stop price
                        Trailing stop price float optional

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
        """  # noqa

        if trail_percent is None and trail_price is None or trail_percent and trail_price:
            raise ValueError("Either trail_percent or trail_price must be provided, not both.")
        if trail_percent:
            if trail_percent < 0:
                raise ValueError("Trail percent must be greater than 0.")
        # Payload for stop order
        payload = {
            "symbol": symbol,  # Asset symbol to buy/sell
            "trail_percent": trail_percent,  # Stop price for the order
            "trail_price": trail_price,  # Limit price for the order
            "qty": qty,  # Quantity of asset to buy/sell
            "side": (side if side == "buy" else "sell"),  # Check if side is buy or sell
            "type": "trailing_stop",  # Order type is stop
            "time_in_force": time_in_force,  # Time in force options, default: day
            "extended_hours": extended_hours,  # Extended hours trading, default: False
        }
        # Return stop order using submit order method
        return self.__submit_order(payload)

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Order //////////////////////#
    ########################################################
    def __submit_order(self, payload: dict) -> OrderClass:
        """Submit an order

        Parameters:
        -----------
        payload:    Order payload dictionary
                    Order payload dictionary required

        Returns:
        --------
        OrderClass: Order information as an OrderClass object

        Raises:
        -------
        Exception:  If failed to submit order
        """  # noqa

        # Alpaca API URL for submitting an order
        url = f"{self.trade_url}/orders"
        # Post request to Alpaca API for submitting an order
        response = requests.post(url, headers=self.headers, json=payload)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return order information as an OrderClass object
            return order_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to submit order. Code: {response.status_code}, Response: {res["message"]}')
