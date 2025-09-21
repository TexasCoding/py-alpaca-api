import json

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.order_model import OrderModel, order_class_from_dict


class Orders:
    def __init__(self, base_url: str, headers: dict[str, str]) -> None:
        """Initializes a new instance of the Order class.

        Args:
            base_url (str): The URL for trading.
            headers (Dict[str, str]): The headers for the API request.

        Returns:
            None
        """
        self.base_url = base_url
        self.headers = headers

    #########################################################
    # \\\\\\\\\/////////  Get All Orders \\\\\\\\\///////////#
    #########################################################
    def get_all_orders(
        self,
        status: str = "open",
        limit: int = 50,
        after: str | None = None,
        until: str | None = None,
        direction: str = "desc",
        nested: bool = False,
        symbols: str | None = None,
    ) -> list[OrderModel]:
        """Retrieves a list of orders for the account, filtered by the supplied parameters.

        Args:
            status: Order status to be queried. Options are 'open', 'closed', or 'all'.
                Defaults to 'open'.
            limit: Maximum number of orders to return. Max is 500. Defaults to 50.
            after: Filter for orders submitted after this timestamp (ISO 8601 format).
            until: Filter for orders submitted until this timestamp (ISO 8601 format).
            direction: Chronological order of response based on submission time.
                Options are 'asc' or 'desc'. Defaults to 'desc'.
            nested: If True, multi-leg orders will be rolled up under the legs field
                of primary order. Defaults to False.
            symbols: Comma-separated list of symbols to filter by (e.g., "AAPL,TSLA,MSFT").

        Returns:
            List of OrderModel objects matching the query parameters.

        Raises:
            ValidationError: If invalid parameters are provided.
            APIRequestError: If the API request fails.
        """
        # Validate status parameter
        valid_statuses = ["open", "closed", "all"]
        if status not in valid_statuses:
            raise ValidationError(
                f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
            )

        # Validate direction parameter
        valid_directions = ["asc", "desc"]
        if direction not in valid_directions:
            raise ValidationError(
                f"Invalid direction '{direction}'. Must be one of: {', '.join(valid_directions)}"
            )

        # Validate limit parameter
        if limit < 1 or limit > 500:
            raise ValidationError("Limit must be between 1 and 500")

        # Build parameters
        params: dict[str, str | bool | float | int] = {
            "status": status,
            "limit": limit,
            "direction": direction,
            "nested": nested,
        }

        if after:
            params["after"] = after
        if until:
            params["until"] = until
        if symbols:
            params["symbols"] = symbols

        url = f"{self.base_url}/orders"

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        # Convert each order dict to OrderModel
        return [order_class_from_dict(order_data) for order_data in response]

    #########################################################
    # \\\\\\\\\/////////  Get Order BY id \\\\\\\///////////#
    #########################################################
    def get_by_id(self, order_id: str, nested: bool = False) -> OrderModel:
        """Retrieves order information by its ID.

        Args:
            order_id (str): The ID of the order to retrieve.
            nested (bool, optional): Whether to include nested objects in the response.
                Defaults to False.

        Returns:
            OrderModel: An object representing the order information.

        Raises:
            ValueError: If the request to retrieve order information fails.
        """
        params: dict[str, str | bool | float | int] = {"nested": nested}
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
        """Cancel an order by its ID.

        Args:
            order_id (str): The ID of the order to be cancelled.

        Returns:
            str: A message indicating the status of the cancellation.

        Raises:
            Exception: If the cancellation request fails, an exception is raised with the
                error message.
        """
        url = f"{self.base_url}/orders/{order_id}"

        Requests().request(method="DELETE", url=url, headers=self.headers)

        return f"Order {order_id} has been cancelled"

    ########################################################
    # \\\\\\\\\\\\\\\\  Cancel All Orders //////////////////#
    ########################################################
    def cancel_all(self) -> str:
        """Cancels all open orders.

        Returns:
            str: A message indicating the number of orders that have been cancelled.

        Raises:
            Exception: If the request to cancel orders is not successful, an exception is
                raised with the error message.
        """
        url = f"{self.base_url}/orders"

        response = json.loads(
            Requests().request(method="DELETE", url=url, headers=self.headers).text
        )
        return f"{len(response)} orders have been cancelled"

    ########################################################
    # \\\\\\\\\  Replace Order /////////////////////#
    ########################################################
    def replace_order(
        self,
        order_id: str,
        qty: float | None = None,
        limit_price: float | None = None,
        stop_price: float | None = None,
        trail: float | None = None,
        time_in_force: str | None = None,
        client_order_id: str | None = None,
    ) -> OrderModel:
        """Replace an existing order with updated parameters.

        Args:
            order_id: The ID of the order to replace.
            qty: The new quantity for the order.
            limit_price: The new limit price for limit orders.
            stop_price: The new stop price for stop orders.
            trail: The new trail amount for trailing stop orders (percent or price).
            time_in_force: The new time in force for the order.
            client_order_id: Optional client-assigned ID for the replacement order.

        Returns:
            OrderModel: The replaced order.

        Raises:
            ValidationError: If no parameters are provided to update.
            APIRequestError: If the API request fails.
        """
        # At least one parameter must be provided
        if not any([qty, limit_price, stop_price, trail, time_in_force]):
            raise ValidationError(
                "At least one parameter must be provided to replace the order"
            )

        body: dict[str, str | float | None] = {}
        if qty is not None:
            body["qty"] = qty
        if limit_price is not None:
            body["limit_price"] = limit_price
        if stop_price is not None:
            body["stop_price"] = stop_price
        if trail is not None:
            body["trail"] = trail
        if time_in_force is not None:
            body["time_in_force"] = time_in_force
        if client_order_id is not None:
            body["client_order_id"] = client_order_id

        url = f"{self.base_url}/orders/{order_id}"

        response = json.loads(
            Requests()
            .request(method="PATCH", url=url, headers=self.headers, json=body)
            .text
        )
        return order_class_from_dict(response)

    ########################################################
    # \\\\\\\  Get Order By Client ID ////////////////#
    ########################################################
    def get_by_client_order_id(self, client_order_id: str) -> OrderModel:
        """Retrieves order information by client order ID.

        Note: This queries all orders and filters by client_order_id.
        The Alpaca API doesn't have a direct endpoint for this.

        Args:
            client_order_id: The client-assigned ID of the order to retrieve.

        Returns:
            OrderModel: An object representing the order information.

        Raises:
            APIRequestError: If the request fails or order not found.
            ValidationError: If no order with given client_order_id is found.
        """
        # Get all orders and filter by client_order_id
        params: dict[str, str | bool | float | int] = {"status": "all", "limit": 500}
        url = f"{self.base_url}/orders"

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        # Find the order with matching client_order_id
        for order_data in response:
            if order_data.get("client_order_id") == client_order_id:
                return order_class_from_dict(order_data)

        raise ValidationError(f"No order found with client_order_id: {client_order_id}")

    ########################################################
    # \\\\\\  Cancel Order By Client ID ///////////////#
    ########################################################
    def cancel_by_client_order_id(self, client_order_id: str) -> str:
        """Cancel an order by its client order ID.

        Note: This first retrieves the order by client_order_id, then cancels by ID.

        Args:
            client_order_id: The client-assigned ID of the order to be cancelled.

        Returns:
            str: A message indicating the status of the cancellation.

        Raises:
            APIRequestError: If the cancellation request fails.
            ValidationError: If no order with given client_order_id is found.
        """
        # First get the order by client_order_id to get its ID
        order = self.get_by_client_order_id(client_order_id)

        # Then cancel by the actual order ID
        return self.cancel_by_id(order.id)

    @staticmethod
    def check_for_order_errors(
        symbol: str,
        qty: float | None = None,
        notional: float | None = None,
        take_profit: float | None = None,
        stop_loss: float | None = None,
    ) -> None:
        """Checks for order errors based on the given parameters.

        Args:
            symbol (str): The symbol for trading.
            qty (float, optional): The quantity of the order. Defaults to None.
            notional (float, optional): The notional value of the order.
                Defaults to None.
            take_profit (float, optional): The take profit value for the order.
                Defaults to None.
            stop_loss (float, optional): The stop loss value for the order. Defaults to None.

        Raises:
            ValueError: If symbol is not provided.
            ValueError: If both qty and notional are provided or if neither is provided.
            ValueError: If either take_profit or stop_loss is not provided.
            ValueError: If both take_profit and stop_loss are not provided.
            ValueError: If notional is provided or if qty is not an integer when both
                take_profit and
            stop_loss are provided.

        Returns:
            None
        """
        if not symbol:
            raise ValueError()

        if not (qty or notional) or (qty and notional):
            raise ValueError()

        # Note: This validation was removed because different order classes have different requirements:
        # - Bracket orders need both take_profit and stop_loss
        # - OTO orders need EITHER take_profit OR stop_loss
        # - OCO orders have other specific requirements
        # The API will validate based on order_class

        if (
            take_profit
            and stop_loss
            and (notional or (qty is not None and not qty.is_integer()))
        ):
            raise ValidationError()

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Market Order ////////////////#
    ########################################################
    def market(
        self,
        symbol: str,
        qty: float | None = None,
        notional: float | None = None,
        take_profit: float | None = None,
        stop_loss: float | None = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
        client_order_id: str | None = None,
        order_class: str | None = None,
    ) -> OrderModel:
        """Submits a market order for a specified symbol.

        Args:
            symbol (str): The symbol of the asset to trade.
            qty (float, optional): The quantity of the asset to trade. Either qty or notional
                must be provided, but not both. Defaults to None.
            notional (float, optional): The notional value of the asset to trade.
                Either qty or notional must be provided, but not both. Defaults to None.
            take_profit (float, optional): The take profit price for the order. Defaults to None.
            stop_loss (float, optional): The stop loss price for the order. Defaults to None.
            side (str, optional): The side of the order (buy/sell). Defaults to "buy".
            time_in_force (str, optional): The time in force for the order
                (day/gtc/opg/ioc/fok). Defaults to "day".
            extended_hours (bool, optional): Whether to trade during extended hours.
                Defaults to False.
            client_order_id (str, optional): Client-assigned ID for the order. Defaults to None.
            order_class (str, optional): Order class (simple/bracket/oco/oto). Defaults to None.

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

        # Convert take_profit and stop_loss floats to dicts before passing to\n        # _submit_order
        take_profit_dict = {"limit_price": take_profit} if take_profit else None
        stop_loss_dict = {"stop_price": stop_loss} if stop_loss else None

        return self._submit_order(
            symbol=symbol,
            side=side,
            qty=qty,
            notional=notional,
            take_profit=take_profit_dict,
            stop_loss=stop_loss_dict,
            entry_type="market",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
            client_order_id=client_order_id,
            order_class=order_class,
        )

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Limit Order /////////////////#
    ########################################################
    def limit(
        self,
        symbol: str,
        limit_price: float,
        qty: float | None = None,
        notional: float | None = None,
        take_profit: float | None = None,
        stop_loss: float | None = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
        client_order_id: str | None = None,
        order_class: str | None = None,
    ) -> OrderModel:
        """Limit order function that submits an order to buy or sell a specified symbol
        at a specified limit price.

        Args:
            symbol (str): The symbol of the asset to trade.
            limit_price (float): The limit price at which to execute the order.
            qty (float, optional): The quantity of the asset to trade. Default is None.
            notional (float, optional): The amount of money to spend on the asset.
                Default is None.
            take_profit (float, optional): The price at which to set a take profit order.
                Default is None.
            stop_loss (float, optional): The price at which to set a stop loss order.
                Default is None.
            side (str, optional): The side of the order. Must be either "buy" or "sell".
                Default is "buy".
            time_in_force (str, optional): The duration of the order. Must be either "day"
                or "gtc" (good till canceled). Default is "day".
            extended_hours (bool, optional): Whether to allow trading during extended
                hours. Default is False.
            client_order_id (str, optional): Client-assigned ID for the order. Defaults to None.
            order_class (str, optional): Order class (simple/bracket/oco/oto). Defaults to None.

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

        # Convert take_profit and stop_loss floats to dicts before passing to\n        # _submit_order
        take_profit_dict = {"limit_price": take_profit} if take_profit else None
        stop_loss_dict = {"stop_price": stop_loss} if stop_loss else None

        return self._submit_order(
            symbol=symbol,
            side=side,
            limit_price=limit_price,
            qty=qty,
            notional=notional,
            take_profit=take_profit_dict,
            stop_loss=stop_loss_dict,
            entry_type="limit",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
            client_order_id=client_order_id,
            order_class=order_class,
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
        take_profit: float | None = None,
        stop_loss: float | None = None,
        time_in_force: str = "day",
        extended_hours: bool = False,
        client_order_id: str | None = None,
        order_class: str | None = None,
    ) -> OrderModel:
        """Args:

            symbol: The symbol of the security to trade.
            stop_price: The stop price at which the trade should be triggered.
            qty: The quantity of shares to trade.
            side: The side of the trade. Defaults to 'buy'.
            take_profit: The price at which to take profit on the trade.
                Defaults to None.
            stop_loss: The price at which to set the stop loss on the trade.
                Defaults to None.
            time_in_force: The duration for which the order will be in effect.
                Defaults to 'day'.
            extended_hours: A boolean value indicating whether to place the order during
                extended hours. Defaults to False.
            client_order_id: Client-assigned ID for the order. Defaults to None.
            order_class: Order class (simple/bracket/oco/oto). Defaults to None.

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

        # Convert take_profit and stop_loss floats to dicts before passing to\n        # _submit_order
        take_profit_dict = {"limit_price": take_profit} if take_profit else None
        stop_loss_dict = {"stop_price": stop_loss} if stop_loss else None

        return self._submit_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            qty=qty,
            take_profit=take_profit_dict,
            stop_loss=stop_loss_dict,
            entry_type="stop",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
            client_order_id=client_order_id,
            order_class=order_class,
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
        client_order_id: str | None = None,
        order_class: str | None = None,
    ) -> OrderModel:
        """Submits a stop-limit order for trading.

        Args:
            symbol (str): The symbol of the security to trade.
            stop_price (float): The stop price for the order.
            limit_price (float): The limit price for the order.
            qty (float): The quantity of shares to trade.
            side (str, optional): The side of the order, either 'buy' or 'sell'.
                Defaults to 'buy'.
            time_in_force (str, optional): The time in force for the order.
                Defaults to 'day'.
            extended_hours (bool, optional): Whether to allow trading during extended hours.
                Defaults to False.
            client_order_id (str, optional): Client-assigned ID for the order. Defaults to None.
            order_class (str, optional): Order class (simple/bracket/oco/oto). Defaults to None.

        Returns:
            OrderModel: The submitted stop-limit order.

        Raises:
            ValueError: If symbol is not provided.
            ValueError: If neither limit_price nor stop_price is provided.
            ValueError: If qty is not provided.
        """
        if not symbol:
            raise ValidationError()

        if not (limit_price or stop_price):
            raise ValidationError()

        if not qty:
            raise ValidationError()

        return self._submit_order(
            symbol=symbol,
            side=side,
            stop_price=stop_price,
            limit_price=limit_price,
            qty=qty,
            entry_type="stop_limit",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
            client_order_id=client_order_id,
            order_class=order_class,
        )

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Stop Order /////////////////#
    ########################################################
    def trailing_stop(
        self,
        symbol: str,
        qty: float,
        trail_percent: float | None = None,
        trail_price: float | None = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
        client_order_id: str | None = None,
        order_class: str | None = None,
    ) -> OrderModel:
        """Submits a trailing stop order for the specified symbol.

        Args:
            symbol (str): The symbol of the security to trade.
            qty (float): The quantity of shares to trade.
            trail_percent (float, optional): The trailing stop percentage. Either
                `trail_percent` or `trail_price` must be provided, not both. Defaults to None.
            trail_price (float, optional): The trailing stop price. Either
                `trail_percent` or `trail_price` must be provided, not both. Defaults to None.
            side (str, optional): The side of the order, either 'buy' or 'sell'. Defaults to 'buy'.
            time_in_force (str, optional): The time in force for the order. Defaults to 'day'.
            extended_hours (bool, optional): Whether to allow trading during extended hours.
                Defaults to False.
            client_order_id (str, optional): Client-assigned ID for the order. Defaults to None.
            order_class (str, optional): Order class (simple/bracket/oco/oto). Defaults to None.

        Returns:
            OrderModel: The submitted trailing stop order.

        Raises:
            ValueError: If `symbol` is not provided.
            ValueError: If `qty` is not provided.
            ValueError: If both `trail_percent` and `trail_price` are provided, or if neither is provided.
            ValueError: If `trail_percent` is less than 0.
        """
        if not symbol:
            raise ValidationError()

        if not qty:
            raise ValidationError()

        if (trail_percent is None and trail_price is None) or (
            trail_percent and trail_price
        ):
            raise ValidationError()

        if trail_percent and trail_percent < 0:
            raise ValidationError()

        return self._submit_order(
            symbol=symbol,
            side=side,
            trail_price=trail_price,
            trail_percent=trail_percent,
            qty=qty,
            entry_type="trailing_stop",
            time_in_force=time_in_force,
            extended_hours=extended_hours,
            client_order_id=client_order_id,
            order_class=order_class,
        )

    ########################################################
    # \\\\\\\\\\\\\\\\  Submit Order //////////////////////#
    ########################################################
    def _submit_order(
        self,
        symbol: str,
        entry_type: str,
        qty: float | None = None,
        notional: float | None = None,
        stop_price: float | None = None,
        limit_price: float | None = None,
        trail_percent: float | None = None,
        trail_price: float | None = None,
        take_profit: dict[str, float] | None = None,
        stop_loss: dict[str, float] | None = None,
        side: str = "buy",
        time_in_force: str = "day",
        extended_hours: bool = False,
        client_order_id: str | None = None,
        order_class: str | None = None,
    ) -> OrderModel:
        """Submits an order to the Alpaca API.

        Args:
            symbol (str): The symbol of the security to trade.
            entry_type (str): The type of order to submit.
            qty (float, optional): The quantity of shares to trade.
                Defaults to None.
            notional (float, optional): The notional value of the trade.
                Defaults to None.
            stop_price (float, optional): The stop price for a stop order.
                Defaults to None.
            limit_price (float, optional): The limit price for a limit order. Defaults to None.
            trail_percent (float, optional): The trailing stop percentage for a trailing
                stop order. Defaults to None.
            trail_price (float, optional): The trailing stop price for a trailing stop
                order. Defaults to None.
            take_profit (Dict[str, float], optional): The take profit parameters for the
                order. Defaults to None.
            stop_loss (Dict[str, float], optional): The stop loss parameters for the order.
                Defaults to None.
            side (str, optional): The side of the trade (buy or sell). Defaults to "buy".
            time_in_force (str, optional): The time in force for the order.
                Defaults to "day".
            extended_hours (bool, optional): Whether to allow trading during extended hours.
                Defaults to False.
            client_order_id (str, optional): Client-assigned ID for the order. Defaults to None.
            order_class (str, optional): Order class (simple/bracket/oco/oto). Defaults to None.

        Returns:
            OrderModel: The submitted order.

        Raises:
            Exception: If the order submission fails.
        """
        # Determine order class
        if order_class:
            # Use explicitly provided order class
            final_order_class = order_class
        elif take_profit or stop_loss:
            # Bracket order if take profit or stop loss is specified
            final_order_class = "bracket"
        else:
            # Default to simple
            final_order_class = "simple"

        payload = {
            "symbol": symbol,
            "qty": qty if qty else None,
            "notional": round(notional, 2) if notional else None,
            "stop_price": stop_price if stop_price else None,
            "limit_price": limit_price if limit_price else None,
            "trail_percent": trail_percent if trail_percent else None,
            "trail_price": trail_price if trail_price else None,
            "order_class": final_order_class,
            "take_profit": take_profit,
            "stop_loss": stop_loss,
            "side": side if side == "buy" else "sell",
            "type": entry_type,
            "time_in_force": time_in_force,
            "extended_hours": extended_hours,
            "client_order_id": client_order_id if client_order_id else None,
        }

        url = f"{self.base_url}/orders"

        response = json.loads(
            Requests()
            .request(method="POST", url=url, headers=self.headers, json=payload)
            .text
        )
        return order_class_from_dict(response)
