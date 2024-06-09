import json
from typing import Dict

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.order_model import OrderModel, order_class_from_dict


class Orders:
    def __init__(self, base_url: str, headers: Dict[str, str]) -> None:
        """
        Initializes a new instance of the Order class.

        Args:
            base_url (str): The URL for trading.
            headers (Dict[str, str]): The headers for the API request.

        Returns:
            None
        """
        self.base_url = base_url
        self.headers = headers

    #########################################################
    # \\\\\\\\\/////////  Get Order BY id \\\\\\\///////////#
    #########################################################
    def get_by_id(self, order_id: str, nested: bool = False) -> OrderModel:
        """
        Retrieves order information by its ID.

        Args:
            order_id (str): The ID of the order to retrieve.
            nested (bool, optional): Whether to include nested objects in the response. Defaults to False.

        Returns:
            OrderModel: An object representing the order information.

        Raises:
            ValueError: If the request to retrieve order information fails.
        """
        params = {"nested": nested}
        url = f"{self.base_url}/orders/{order_id}"

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )
        return order_class_from_dict(response)

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
        url = f"{self.base_url}/orders/{order_id}"

        Requests().request(method="DELETE", url=url, headers=self.headers)

        return f"Order {order_id} has been cancelled"

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
        url = f"{self.base_url}/orders"

        response = json.loads(
            Requests().request(method="DELETE", url=url, headers=self.headers).text
        )
        return f"{len(response)} orders have been cancelled"

    @staticmethod
    def check_for_order_errors(
        symbol: str,
        qty: float = None,
        notional: float = None,
        take_profit: float = None,
        stop_loss: float = None,
    ) -> None:
        """
        Checks for order errors based on the given parameters.

        Args:
            symbol (str): The symbol for trading.
            qty (float, optional): The quantity of the order. Defaults to None.
            notional (float, optional): The notional value of the order. Defaults to None.
            take_profit (float, optional): The take profit value for the order. Defaults to None.
            stop_loss (float, optional): The stop loss value for the order. Defaults to None.

        Raises:
            ValueError: If symbol is not provided.
            ValueError: If both qty and notional are provided or if neither is provided.
            ValueError: If either take_profit or stop_loss is not provided.
            ValueError: If both take_profit and stop_loss are not provided.
            ValueError: If notional is provided or if qty is not an integer when both take_profit and
            stop_loss are provided.

        Returns:
            None
        """
        if not symbol:
            raise ValueError("Must provide symbol for trading.")

        if not (qty or notional) or (qty and notional):
            raise ValueError("Qty or Notional are required, not both.")

        if take_profit and not stop_loss or stop_loss and not take_profit:
            raise ValueError(
                "Both take profit and stop loss are required for bracket orders."
            )

        if take_profit and stop_loss:
            if notional or not qty.is_integer():
                raise ValueError("Bracket orders can not be fractionable.")

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Market Order ////////////////#
    ########################################################
    def market(
        self,
        symbol: str,
        qty: float = None,
        notional: float = None,
        take_profit: float = None,
        stop_loss: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderModel:
        """
        Submits a market order for a specified symbol.

        Args:
            symbol (str): The symbol of the asset to trade.
            qty (float, optional): The quantity of the asset to trade. Either qty or notional must be provided,
            but not both. Defaults to None.
            notional (float, optional): The notional value of the asset to trade. Either qty or notional must be
            provided, but not both. Defaults to None.
            take_profit (float, optional): The take profit price for the order. Defaults to None.
            stop_loss (float, optional): The stop loss price for the order. Defaults to None.
            side (str, optional): The side of the order (buy/sell). Defaults to "buy".
            time_in_force (str, optional): The time in force for the order (day/gtc/opg/ioc/fok). Defaults to "day".
            extended_hours (bool, optional): Whether to trade during extended hours. Defaults to False.

        Returns:
            OrderModel: An instance of the OrderModel representing the submitted order.
        """
        self.check_for_order_errors(
            symbol=symbol,
            qty=qty,
            notional=notional,
            take_profit=take_profit,
            stop_loss=stop_loss,
        )

        return self._submit_order(
            symbol=symbol,
            side=side,
            qty=qty,
            notional=notional,
            take_profit=take_profit,
            stop_loss=stop_loss,
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
        take_profit: float = None,
        stop_loss: float = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderModel:
        """
        Limit order function that submits an order to buy or sell a specified symbol at a specified limit price.

        Args:
            symbol (str): The symbol of the asset to trade.
            limit_price (float): The limit price at which to execute the order.
            qty (float, optional): The quantity of the asset to trade. Default is None.
            notional (float, optional): The amount of money to spend on the asset. Default is None.
            take_profit (float, optional): The price at which to set a take profit order. Default is None.
            stop_loss (float, optional): The price at which to set a stop loss order. Default is None.
            side (str, optional): The side of the order. Must be either "buy" or "sell". Default is "buy".
            time_in_force (str, optional): The duration of the order. Must be either "day" or "gtc"
            (good till canceled). Default is "day".
            extended_hours (bool, optional): Whether to allow trading during extended hours. Default is False.

        Returns:
            OrderModel: The submitted order.
        """
        self.check_for_order_errors(
            symbol=symbol,
            qty=qty,
            notional=notional,
            take_profit=take_profit,
            stop_loss=stop_loss,
        )

        return self._submit_order(
            symbol=symbol,
            side=side,
            limit_price=limit_price,
            qty=qty,
            notional=notional,
            take_profit=take_profit,
            stop_loss=stop_loss,
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
        take_profit: float = None,
        stop_loss: float = None,
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderModel:
        """
        Args:
            symbol: The symbol of the security to trade.
            stop_price: The stop price at which the trade should be triggered.
            qty: The quantity of shares to trade.
            side: The side of the trade. Defaults to 'buy'.
            take_profit: The price at which to take profit on the trade. Defaults to None.
            stop_loss: The price at which to set the stop loss on the trade. Defaults to None.
            time_in_force: The duration for which the order will be in effect. Defaults to 'day'.
            extended_hours: A boolean value indicating whether to place the order during extended hours.
            Defaults to False.

        Returns:
            An instance of the OrderModel representing the submitted order.

        Raises:
            OrderError: If there are any errors with the order parameters.
        """
        self.check_for_order_errors(
            symbol=symbol,
            qty=qty,
            take_profit=take_profit,
            stop_loss=stop_loss,
        )

        return self._submit_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            qty=qty,
            take_profit=take_profit,
            stop_loss=stop_loss,
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
    ) -> OrderModel:
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
            OrderModel: The submitted stop-limit order.

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

        return self._submit_order(
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
    ) -> OrderModel:
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
            OrderModel: The submitted trailing stop order.

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

        if (
            trail_percent is None
            and trail_price is None
            or trail_percent
            and trail_price
        ):
            raise ValueError(
                "Either trail_percent or trail_price must be provided, not both."
            )

        if trail_percent:
            if trail_percent < 0:
                raise ValueError("Trail percent must be greater than 0.")

        return self._submit_order(
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
    def _submit_order(
        self,
        symbol: str,
        entry_type: str,
        qty: float = None,
        notional: float = None,
        stop_price: float = None,
        limit_price: float = None,
        trail_percent: float = None,
        trail_price: float = None,
        take_profit: Dict[str, float] = None,
        stop_loss: Dict[str, float] = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
    ) -> OrderModel:
        """
        Submits an order to the Alpaca API.

        Args:
            symbol (str): The symbol of the security to trade.
            entry_type (str): The type of order to submit.
            qty (float, optional): The quantity of shares to trade. Defaults to None.
            notional (float, optional): The notional value of the trade. Defaults to None.
            stop_price (float, optional): The stop price for a stop order. Defaults to None.
            limit_price (float, optional): The limit price for a limit order. Defaults to None.
            trail_percent (float, optional): The trailing stop percentage for a trailing stop order. Defaults to None.
            trail_price (float, optional): The trailing stop price for a trailing stop order. Defaults to None.
            take_profit (Dict[str, float], optional): The take profit parameters for the order. Defaults to None.
            stop_loss (Dict[str, float], optional): The stop loss parameters for the order. Defaults to None.
            side (str, optional): The side of the trade (buy or sell). Defaults to "buy".
            time_in_force (str, optional): The time in force for the order. Defaults to "day".
            extended_hours (bool, optional): Whether to allow trading during extended hours. Defaults to False.

        Returns:
            OrderModel: The submitted order.

        Raises:
            Exception: If the order submission fails.
        """
        payload = {
            "symbol": symbol,
            "qty": qty if qty else None,
            "notional": round(notional, 2) if notional else None,
            "stop_price": stop_price if stop_price else None,
            "limit_price": limit_price if limit_price else None,
            "trail_percent": trail_percent if trail_percent else None,
            "trail_price": trail_price if trail_price else None,
            "order_class": "bracket" if take_profit or stop_loss else "simple",
            "take_profit": ({"limit_price": take_profit} if take_profit else None),
            "stop_loss": {"stop_price": stop_loss} if stop_loss else None,
            "side": side if side == "buy" else "sell",
            "type": entry_type,
            "time_in_force": time_in_force,
            "extended_hours": extended_hours,
        }

        url = f"{self.base_url}/orders"

        response = json.loads(
            Requests()
            .request(method="POST", url=url, headers=self.headers, json=payload)
            .text
        )
        return order_class_from_dict(response)
