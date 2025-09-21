py_alpaca_api.trading.orders
============================

.. py:module:: py_alpaca_api.trading.orders


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.orders.Orders


Module Contents
---------------

.. py:class:: Orders(base_url: str, headers: dict[str, str])

   .. py:attribute:: base_url


   .. py:attribute:: headers


   .. py:method:: get_all_orders(status: str = 'open', limit: int = 50, after: str | None = None, until: str | None = None, direction: str = 'desc', nested: bool = False, symbols: str | None = None) -> list[py_alpaca_api.models.order_model.OrderModel]

      Retrieves a list of orders for the account, filtered by the supplied parameters.

      :param status: Order status to be queried. Options are 'open', 'closed', or 'all'.
                     Defaults to 'open'.
      :param limit: Maximum number of orders to return. Max is 500. Defaults to 50.
      :param after: Filter for orders submitted after this timestamp (ISO 8601 format).
      :param until: Filter for orders submitted until this timestamp (ISO 8601 format).
      :param direction: Chronological order of response based on submission time.
                        Options are 'asc' or 'desc'. Defaults to 'desc'.
      :param nested: If True, multi-leg orders will be rolled up under the legs field
                     of primary order. Defaults to False.
      :param symbols: Comma-separated list of symbols to filter by (e.g., "AAPL,TSLA,MSFT").

      :returns: List of OrderModel objects matching the query parameters.

      :raises ValidationError: If invalid parameters are provided.
      :raises APIRequestError: If the API request fails.



   .. py:method:: get_by_id(order_id: str, nested: bool = False) -> py_alpaca_api.models.order_model.OrderModel

      Retrieves order information by its ID.

      :param order_id: The ID of the order to retrieve.
      :type order_id: str
      :param nested: Whether to include nested objects in the response.
                     Defaults to False.
      :type nested: bool, optional

      :returns: An object representing the order information.
      :rtype: OrderModel

      :raises ValueError: If the request to retrieve order information fails.



   .. py:method:: cancel_by_id(order_id: str) -> str

      Cancel an order by its ID.

      :param order_id: The ID of the order to be cancelled.
      :type order_id: str

      :returns: A message indicating the status of the cancellation.
      :rtype: str

      :raises Exception: If the cancellation request fails, an exception is raised with the
          error message.



   .. py:method:: cancel_all() -> str

      Cancels all open orders.

      :returns: A message indicating the number of orders that have been cancelled.
      :rtype: str

      :raises Exception: If the request to cancel orders is not successful, an exception is
          raised with the error message.



   .. py:method:: replace_order(order_id: str, qty: float | None = None, limit_price: float | None = None, stop_price: float | None = None, trail: float | None = None, time_in_force: str | None = None, client_order_id: str | None = None) -> py_alpaca_api.models.order_model.OrderModel

      Replace an existing order with updated parameters.

      :param order_id: The ID of the order to replace.
      :param qty: The new quantity for the order.
      :param limit_price: The new limit price for limit orders.
      :param stop_price: The new stop price for stop orders.
      :param trail: The new trail amount for trailing stop orders (percent or price).
      :param time_in_force: The new time in force for the order.
      :param client_order_id: Optional client-assigned ID for the replacement order.

      :returns: The replaced order.
      :rtype: OrderModel

      :raises ValidationError: If no parameters are provided to update.
      :raises APIRequestError: If the API request fails.



   .. py:method:: get_by_client_order_id(client_order_id: str) -> py_alpaca_api.models.order_model.OrderModel

      Retrieves order information by client order ID.

      Note: This queries all orders and filters by client_order_id.
      The Alpaca API doesn't have a direct endpoint for this.

      :param client_order_id: The client-assigned ID of the order to retrieve.

      :returns: An object representing the order information.
      :rtype: OrderModel

      :raises APIRequestError: If the request fails or order not found.
      :raises ValidationError: If no order with given client_order_id is found.



   .. py:method:: cancel_by_client_order_id(client_order_id: str) -> str

      Cancel an order by its client order ID.

      Note: This first retrieves the order by client_order_id, then cancels by ID.

      :param client_order_id: The client-assigned ID of the order to be cancelled.

      :returns: A message indicating the status of the cancellation.
      :rtype: str

      :raises APIRequestError: If the cancellation request fails.
      :raises ValidationError: If no order with given client_order_id is found.



   .. py:method:: check_for_order_errors(symbol: str, qty: float | None = None, notional: float | None = None, take_profit: float | None = None, stop_loss: float | None = None) -> None
      :staticmethod:


      Checks for order errors based on the given parameters.

      :param symbol: The symbol for trading.
      :type symbol: str
      :param qty: The quantity of the order. Defaults to None.
      :type qty: float, optional
      :param notional: The notional value of the order.
                       Defaults to None.
      :type notional: float, optional
      :param take_profit: The take profit value for the order.
                          Defaults to None.
      :type take_profit: float, optional
      :param stop_loss: The stop loss value for the order. Defaults to None.
      :type stop_loss: float, optional

      :raises ValueError: If symbol is not provided.
      :raises ValueError: If both qty and notional are provided or if neither is provided.
      :raises ValueError: If either take_profit or stop_loss is not provided.
      :raises ValueError: If both take_profit and stop_loss are not provided.
      :raises ValueError: If notional is provided or if qty is not an integer when both
          take_profit and
      :raises stop_loss are provided.:

      :returns: None



   .. py:method:: market(symbol: str, qty: float | None = None, notional: float | None = None, take_profit: float | None = None, stop_loss: float | None = None, side: str = 'buy', time_in_force: str = 'day', extended_hours: bool = False, client_order_id: str | None = None, order_class: str | None = None) -> py_alpaca_api.models.order_model.OrderModel

      Submits a market order for a specified symbol.

      :param symbol: The symbol of the asset to trade.
      :type symbol: str
      :param qty: The quantity of the asset to trade. Either qty or notional
                  must be provided, but not both. Defaults to None.
      :type qty: float, optional
      :param notional: The notional value of the asset to trade.
                       Either qty or notional must be provided, but not both. Defaults to None.
      :type notional: float, optional
      :param take_profit: The take profit price for the order. Defaults to None.
      :type take_profit: float, optional
      :param stop_loss: The stop loss price for the order. Defaults to None.
      :type stop_loss: float, optional
      :param side: The side of the order (buy/sell). Defaults to "buy".
      :type side: str, optional
      :param time_in_force: The time in force for the order
                            (day/gtc/opg/ioc/fok). Defaults to "day".
      :type time_in_force: str, optional
      :param extended_hours: Whether to trade during extended hours.
                             Defaults to False.
      :type extended_hours: bool, optional
      :param client_order_id: Client-assigned ID for the order. Defaults to None.
      :type client_order_id: str, optional
      :param order_class: Order class (simple/bracket/oco/oto). Defaults to None.
      :type order_class: str, optional

      :returns: An instance of the OrderModel representing the submitted order.
      :rtype: OrderModel



   .. py:method:: limit(symbol: str, limit_price: float, qty: float | None = None, notional: float | None = None, take_profit: float | None = None, stop_loss: float | None = None, side: str = 'buy', time_in_force: str = 'day', extended_hours: bool = False, client_order_id: str | None = None, order_class: str | None = None) -> py_alpaca_api.models.order_model.OrderModel

      Limit order function that submits an order to buy or sell a specified symbol
      at a specified limit price.

      :param symbol: The symbol of the asset to trade.
      :type symbol: str
      :param limit_price: The limit price at which to execute the order.
      :type limit_price: float
      :param qty: The quantity of the asset to trade. Default is None.
      :type qty: float, optional
      :param notional: The amount of money to spend on the asset.
                       Default is None.
      :type notional: float, optional
      :param take_profit: The price at which to set a take profit order.
                          Default is None.
      :type take_profit: float, optional
      :param stop_loss: The price at which to set a stop loss order.
                        Default is None.
      :type stop_loss: float, optional
      :param side: The side of the order. Must be either "buy" or "sell".
                   Default is "buy".
      :type side: str, optional
      :param time_in_force: The duration of the order. Must be either "day"
                            or "gtc" (good till canceled). Default is "day".
      :type time_in_force: str, optional
      :param extended_hours: Whether to allow trading during extended
                             hours. Default is False.
      :type extended_hours: bool, optional
      :param client_order_id: Client-assigned ID for the order. Defaults to None.
      :type client_order_id: str, optional
      :param order_class: Order class (simple/bracket/oco/oto). Defaults to None.
      :type order_class: str, optional

      :returns: The submitted order.
      :rtype: OrderModel



   .. py:method:: stop(symbol: str, stop_price: float, qty: float, side: str = 'buy', take_profit: float | None = None, stop_loss: float | None = None, time_in_force: str = 'day', extended_hours: bool = False, client_order_id: str | None = None, order_class: str | None = None) -> py_alpaca_api.models.order_model.OrderModel

      :param symbol: The symbol of the security to trade.
      :param stop_price: The stop price at which the trade should be triggered.
      :param qty: The quantity of shares to trade.
      :param side: The side of the trade. Defaults to 'buy'.
      :param take_profit: The price at which to take profit on the trade.
                          Defaults to None.
      :param stop_loss: The price at which to set the stop loss on the trade.
                        Defaults to None.
      :param time_in_force: The duration for which the order will be in effect.
                            Defaults to 'day'.
      :param extended_hours: A boolean value indicating whether to place the order during
                             extended hours. Defaults to False.
      :param client_order_id: Client-assigned ID for the order. Defaults to None.
      :param order_class: Order class (simple/bracket/oco/oto). Defaults to None.

      :returns: An instance of the OrderModel representing the submitted order.

      :raises OrderError: If there are any errors with the order parameters.



   .. py:method:: stop_limit(symbol: str, stop_price: float, limit_price: float, qty: float, side: str = 'buy', time_in_force: str = 'day', extended_hours: bool = False, client_order_id: str | None = None, order_class: str | None = None) -> py_alpaca_api.models.order_model.OrderModel

      Submits a stop-limit order for trading.

      :param symbol: The symbol of the security to trade.
      :type symbol: str
      :param stop_price: The stop price for the order.
      :type stop_price: float
      :param limit_price: The limit price for the order.
      :type limit_price: float
      :param qty: The quantity of shares to trade.
      :type qty: float
      :param side: The side of the order, either 'buy' or 'sell'.
                   Defaults to 'buy'.
      :type side: str, optional
      :param time_in_force: The time in force for the order.
                            Defaults to 'day'.
      :type time_in_force: str, optional
      :param extended_hours: Whether to allow trading during extended hours.
                             Defaults to False.
      :type extended_hours: bool, optional
      :param client_order_id: Client-assigned ID for the order. Defaults to None.
      :type client_order_id: str, optional
      :param order_class: Order class (simple/bracket/oco/oto). Defaults to None.
      :type order_class: str, optional

      :returns: The submitted stop-limit order.
      :rtype: OrderModel

      :raises ValueError: If symbol is not provided.
      :raises ValueError: If neither limit_price nor stop_price is provided.
      :raises ValueError: If qty is not provided.



   .. py:method:: trailing_stop(symbol: str, qty: float, trail_percent: float | None = None, trail_price: float | None = None, side: str = 'buy', time_in_force: str = 'day', extended_hours: bool = False, client_order_id: str | None = None, order_class: str | None = None) -> py_alpaca_api.models.order_model.OrderModel

      Submits a trailing stop order for the specified symbol.

      :param symbol: The symbol of the security to trade.
      :type symbol: str
      :param qty: The quantity of shares to trade.
      :type qty: float
      :param trail_percent: The trailing stop percentage. Either
                            `trail_percent` or `trail_price` must be provided, not both. Defaults to None.
      :type trail_percent: float, optional
      :param trail_price: The trailing stop price. Either
                          `trail_percent` or `trail_price` must be provided, not both. Defaults to None.
      :type trail_price: float, optional
      :param side: The side of the order, either 'buy' or 'sell'. Defaults to 'buy'.
      :type side: str, optional
      :param time_in_force: The time in force for the order. Defaults to 'day'.
      :type time_in_force: str, optional
      :param extended_hours: Whether to allow trading during extended hours.
                             Defaults to False.
      :type extended_hours: bool, optional
      :param client_order_id: Client-assigned ID for the order. Defaults to None.
      :type client_order_id: str, optional
      :param order_class: Order class (simple/bracket/oco/oto). Defaults to None.
      :type order_class: str, optional

      :returns: The submitted trailing stop order.
      :rtype: OrderModel

      :raises ValueError: If `symbol` is not provided.
      :raises ValueError: If `qty` is not provided.
      :raises ValueError: If both `trail_percent` and `trail_price` are provided, or if neither is provided.
      :raises ValueError: If `trail_percent` is less than 0.
