import json
from typing import Dict

import requests

from .data_classes import OrderClass, order_class_from_dict


class Order:
    def __init__(self, trade_url: str, headers: Dict[str, str]) -> None:
        """
        Initializes a new instance of the Order class.

        Args:
            trade_url (str): The URL for trading.
            headers (Dict[str, str]): The headers for the API request.

        Returns:
            None
        """
        self.trade_url = trade_url
        self.headers = headers

    #########################################################
    # \\\\\\\\\/////////  Get Order BY id \\\\\\\///////////#
    #########################################################
    def get_by_id(self, order_id: str, nested: bool = False) -> OrderClass:
        """
        Retrieves order information by its ID.

        Args:
            order_id (str): The ID of the order to retrieve.
            nested (bool, optional): Whether to include nested objects in the response. Defaults to False.

        Returns:
            OrderClass: An object representing the order information.

        Raises:
            ValueError: If the request to retrieve order information fails.
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
    def cancel_by_id(self, order_id: str) -> str:
        """
        Cancel an order by its ID.

        Args:
            order_id (str): The ID of the order to be cancelled.

        Returns:
            str: A message indicating the status of the cancellation.

        Raises:
            Exception: If the cancellation request fails, an exception is raised with the error message.
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
    def cancel_all(self) -> str:
        """
        Cancels all open orders.

        Returns:
            str: A message indicating the number of orders that have been cancelled.

        Raises:
            Exception: If the request to cancel orders is not successful, an exception is raised with the error message.
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
    def market(
        self,
        symbol: str,
        qty: float = None,
        notional: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderClass:
        """
        Submits a market order for the specified symbol.

        Args:
            symbol (str): The symbol to trade.
            qty (float, optional): The quantity to trade. Either `qty` or `notional` must be provided, not both.
            Defaults to None.
            notional (float, optional): The notional value of the trade. Either `qty` or `notional` must be provided, not both.
            Defaults to None.
            side (str, optional): The side of the trade. Defaults to "buy".
            time_in_force (str, optional): The time in force for the order. Defaults to "day".
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderClass: The submitted market order.

        Raises:
            ValueError: If `symbol` is not provided.
            ValueError: If both `qty` and `notional` are not provided, or if both are provided.
        """

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not (qty or notional) or (qty and notional):
            raise ValueError("Qty or Notional are required, not both.")

        return self.__submit_order(
            symbol=symbol,
            side=side,
            qty=qty,
            notional=notional,
            entry_type="market",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
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
        """
        Submits a limit order for trading.

        Args:
            symbol (str): The symbol of the security to trade.
            limit_price (float): The limit price for the order.
            qty (float, optional): The quantity of shares to trade. Either `qty` or `notional` must be provided, not both.
            Defaults to None.
            notional (float, optional): The notional value of the trade. Either `qty` or `notional` must be provided, not both.
            Defaults to None.
            side (str, optional): The side of the order, either 'buy' or 'sell'. Defaults to 'buy'.
            time_in_force (str, optional): The time in force for the order. Defaults to 'day'.
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderClass: The submitted limit order.

        Raises:
            ValueError: If `symbol` or `limit_price` is not provided, or if both `qty` and `notional` are provided or not provided.

        """

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not limit_price:
            raise ValueError("Must provide limit price for trading.")

        if not (qty or notional) or (qty and notional):
            raise ValueError("Qty or Notional are required, not both.")

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
        """
        Submits a stop order for trading.

        Args:
            symbol (str): The symbol of the security to trade.
            stop_price (float): The stop price for the order.
            qty (float): The quantity of shares to trade.
            side (str, optional): The side of the order. Defaults to "buy".
            time_in_force (str, optional): The time in force for the order. Defaults to "day".
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderClass: The submitted stop order.

        Raises:
            ValueError: If symbol, stop_price, or qty is not provided.
        """

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not stop_price:
            raise ValueError("Must provide stop price for trading.")

        if not qty:
            raise ValueError("Qty is required.")

        return self.__submit_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            qty=qty,
            entry_type="stop",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
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
        """
        Submits a stop-limit order for trading.

        Args:
            symbol (str): The symbol of the security to trade.
            stop_price (float): The stop price for the order.
            limit_price (float): The limit price for the order.
            qty (float): The quantity of shares to trade.
            side (str, optional): The side of the order, either 'buy' or 'sell'. Defaults to 'buy'.
            time_in_force (str, optional): The time in force for the order. Defaults to 'day'.
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderClass: The submitted stop-limit order.

        Raises:
            ValueError: If symbol is not provided.
            ValueError: If neither limit_price nor stop_price is provided.
            ValueError: If qty is not provided.
        """

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not (limit_price or stop_price):
            raise ValueError("Must provide limit and stop price for trading.")

        if not qty:
            raise ValueError("Qty is required.")

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
        """
        Submits a trailing stop order for the specified symbol.

        Args:
            symbol (str): The symbol of the security to trade.
            qty (float): The quantity of shares to trade.
            trail_percent (float, optional): The trailing stop percentage. Either `trail_percent` or `trail_price`
            must be provided, not both. Defaults to None.
            trail_price (float, optional): The trailing stop price. Either `trail_percent` or `trail_price`
            must be provided, not both. Defaults to None.
            side (str, optional): The side of the order, either 'buy' or 'sell'. Defaults to 'buy'.
            time_in_force (str, optional): The time in force for the order. Defaults to 'day'.
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderClass: The submitted trailing stop order.

        Raises:
            ValueError: If `symbol` is not provided.
            ValueError: If `qty` is not provided.
            ValueError: If both `trail_percent` and `trail_price` are provided, or if neither is provided.
            ValueError: If `trail_percent` is less than 0.
        """

        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not qty:
            raise ValueError("Qty is required.")

        if trail_percent is None and trail_price is None or trail_percent and trail_price:
            raise ValueError("Either trail_percent or trail_price must be provided, not both.")

        if trail_percent:
            if trail_percent < 0:
                raise ValueError("Trail percent must be greater than 0.")

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
        """
        Submits an order to the Alpaca API.

        Args:
            symbol (str): The symbol of the security to trade.
            entry_type (str): The type of order to submit (e.g., 'market', 'limit', 'stop').
            qty (float, optional): The quantity of shares to trade. Defaults to None.
            notional (float, optional): The desired notional value of the trade. Defaults to None.
            stop_price (float, optional): The stop price for a stop order. Defaults to None.
            limit_price (float, optional): The limit price for a limit order. Defaults to None.
            trail_percent (float, optional): The trailing stop percentage for a trailing stop order. Defaults to None.
            trail_price (float, optional): The trailing stop price for a trailing stop order. Defaults to None.
            side (str, optional): The side of the trade ('buy' or 'sell'). Defaults to 'buy'.
            time_in_force (str, optional): The time in force for the order ('day', 'gtc', 'opg', 'ioc', 'fok'). Defaults to 'day'.
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderClass: An object representing the submitted order.

        Raises:
            Exception: If the order submission fails, an exception is raised with the error message.
        """

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

        url = f"{self.trade_url}/orders"

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            res = json.loads(response.text)
            return order_class_from_dict(res)
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to submit order. Code: {response.status_code}, Response: {res["message"]}')
