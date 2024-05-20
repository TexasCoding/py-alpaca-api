import json
from typing import Dict

import requests

from .data_classes import OrderClass, order_class_from_dict


class Order:
    def __init__(self, trade_url: str, headers: Dict[str, str]) -> None:
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
        >>> from py_alpaca_api.alpaca import PyAlpacaApi
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
        >>> from py_alpaca_api.alpaca import PyAlpacaApi
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
        >>> from py_alpaca_api.alpaca import PyAlpacaApi
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

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not (qty or notional) or (qty and notional):
            raise ValueError("Qty or Notional are required, not both.")

        # Return market order using submit order method
        return self.__submit_order(
            symbol=symbol, side=side, qty=qty, notional=notional, entry_type="market", time_in_force=time_in_force, extended_hours=extended_hours
        )

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

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not limit_price:
            raise ValueError("Must provide limit price for trading.")

        if not (qty or notional) or (qty and notional):
            raise ValueError("Qty or Notional are required, not both.")
        # Return limit order
        return self.__submit_order(
            symbol=symbol,
            side=side,
            limit_price=limit_price,
            qty=qty,
            notional=notional,
            entry_type="limit",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
        )

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

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not stop_price:
            raise ValueError("Must provide stop price for trading.")

        if not qty:
            raise ValueError("Qty is required.")
        # Return stop order
        return self.__submit_order(
            symbol=symbol, side=side, stop_price=stop_price, qty=qty, entry_type="stop", time_in_force=time_in_force, extended_hours=extended_hours
        )

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

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not (limit_price or stop_price):
            raise ValueError("Must provide limit and stop price for trading.")

        if not qty:
            raise ValueError("Qty is required.")
        # Return stop_limit order
        return self.__submit_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            limit_price=limit_price,
            qty=qty,
            entry_type="stop_limit",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
        )

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

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not qty:
            raise ValueError("Qty is required.")

        if trail_percent is None and trail_price is None or trail_percent and trail_price:
            raise ValueError("Either trail_percent or trail_price must be provided, not both.")

        if trail_percent:
            if trail_percent < 0:
                raise ValueError("Trail percent must be greater than 0.")

        # Return trailing_stop
        return self.__submit_order(
            symbol=symbol,
            side=side,
            trail_price=trail_price,
            trail_percent=trail_percent,
            qty=qty,
            entry_type="trailing_stop",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
        )

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Order //////////////////////#
    ########################################################
    def __submit_order(
        self,
        symbol: str,
        entry_type: str,
        qty: float = None,
        notional: float = None,
        stop_price: float = None,
        limit_price: float = None,
        trail_percent: float = None,
        trail_price: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:

        payload = {
            "symbol": symbol,
            "qty": qty if qty else None,
            "notional": round(notional, 2) if notional else None,
            "stop_price": stop_price if stop_price else None,
            "limit_price": limit_price if limit_price else None,
            "trail_percent": trail_percent if trail_percent else None,
            "trail_price": trail_price if trail_price else None,
            "side": side if side == "buy" else "sell",
            "type": entry_type,
            "time_in_force": time_in_force,
            "extended_hours": extended_hours,
        }

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
