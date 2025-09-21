py_alpaca_api.trading
=====================

.. py:module:: py_alpaca_api.trading


Submodules
----------

.. toctree::
   :maxdepth: 1

   /api/py_alpaca_api/trading/account/index
   /api/py_alpaca_api/trading/corporate_actions/index
   /api/py_alpaca_api/trading/market/index
   /api/py_alpaca_api/trading/news/index
   /api/py_alpaca_api/trading/orders/index
   /api/py_alpaca_api/trading/positions/index
   /api/py_alpaca_api/trading/recommendations/index
   /api/py_alpaca_api/trading/watchlists/index


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.Account
   py_alpaca_api.trading.CorporateActions
   py_alpaca_api.trading.Market
   py_alpaca_api.trading.News
   py_alpaca_api.trading.Orders
   py_alpaca_api.trading.Positions
   py_alpaca_api.trading.Recommendations
   py_alpaca_api.trading.Watchlist
   py_alpaca_api.trading.Trading


Package Contents
----------------

.. py:class:: Account(headers: dict[str, str], base_url: str)

   .. py:attribute:: headers


   .. py:attribute:: base_url


   .. py:method:: get() -> py_alpaca_api.models.account_model.AccountModel

      Retrieves the user's account information.

      :returns: The user's account model.
      :rtype: AccountModel



   .. py:method:: activities(activity_type: str, date: str | None = None, until_date: str | None = None) -> list[py_alpaca_api.models.account_activity_model.AccountActivityModel]

      Retrieves the account activities for the specified activity type.

      Optionally filtered by date or until date.

      :param activity_type: The type of account activity to retrieve.
      :type activity_type: str
      :param date: The date to filter the activities by.
                   If provided, only activities on this date will be returned.
      :type date: str, optional
      :param until_date: The date to filter the activities up to.
                         If provided, only activities up to and including this date
                         will be returned.
      :type until_date: str, optional

      :returns:

                A list of account activity models
                    representing the retrieved activities.
      :rtype: List[AccountActivityModel]

      :raises ValueError: If the activity type is not provided, or if both
          date and until_date are provided.



   .. py:method:: portfolio_history(period: str = '1W', timeframe: str = '1D', intraday_reporting: str = 'market_hours') -> pandas.DataFrame

      Retrieves portfolio history data.

      :param period: The period of time for which the portfolio history
                     is requested. Defaults to "1W" (1 week).
      :type period: str
      :param timeframe: The timeframe for the intervals of the portfolio
                        history. Defaults to "1D" (1 day).
      :type timeframe: str
      :param intraday_reporting: The type of intraday reporting to be used.
                                 Defaults to "market_hours".
      :type intraday_reporting: str

      :returns: A pandas DataFrame containing the portfolio history data.
      :rtype: pd.DataFrame

      :raises Exception: If the request to the Alpaca API fails.



   .. py:method:: get_configuration() -> py_alpaca_api.models.account_config_model.AccountConfigModel

      Retrieves the current account configuration settings.

      :returns: The current account configuration.
      :rtype: AccountConfigModel

      :raises APIRequestError: If the request to retrieve configuration fails.



   .. py:method:: update_configuration(dtbp_check: str | None = None, fractional_trading: bool | None = None, max_margin_multiplier: str | None = None, no_shorting: bool | None = None, pdt_check: str | None = None, ptp_no_exception_entry: bool | None = None, suspend_trade: bool | None = None, trade_confirm_email: str | None = None) -> py_alpaca_api.models.account_config_model.AccountConfigModel

      Updates the account configuration settings.

      :param dtbp_check: Day trade buying power check ("entry", "exit", "both")
      :param fractional_trading: Whether to enable fractional trading
      :param max_margin_multiplier: Maximum margin multiplier ("1", "2", "4")
      :param no_shorting: Whether to disable short selling
      :param pdt_check: Pattern day trader check ("entry", "exit", "both")
      :param ptp_no_exception_entry: Whether to enable PTP no exception entry
      :param suspend_trade: Whether to suspend trading
      :param trade_confirm_email: Trade confirmation emails ("all", "none")

      :returns: The updated account configuration.
      :rtype: AccountConfigModel

      :raises APIRequestError: If the request to update configuration fails.
      :raises ValueError: If invalid parameter values are provided.



.. py:class:: CorporateActions(headers: dict[str, str], base_url: str)

   .. py:attribute:: headers


   .. py:attribute:: base_url


   .. py:method:: get_announcements(since: str, until: str, ca_types: list[str], symbol: str | None = None, cusip: str | None = None, date_type: Literal['declaration_date', 'ex_date', 'record_date', 'payable_date'] | None = None, page_limit: int = 100, page_token: str | None = None) -> list[py_alpaca_api.models.corporate_action_model.CorporateActionModel]

      Retrieve corporate action announcements.

      :param since: The start (inclusive) of the date range in YYYY-MM-DD format.
                    Date range is limited to 90 days.
      :param until: The end (inclusive) of the date range in YYYY-MM-DD format.
                    Date range is limited to 90 days.
      :param ca_types: List of corporate action types to return.
                       Valid types: dividend, merger, spinoff, split
      :param symbol: Optional filter by symbol
      :param cusip: Optional filter by CUSIP
      :param date_type: Optional date type for filtering (declaration_date, ex_date, record_date, payable_date)
      :param page_limit: Number of results per page (Note: API may return all results regardless)
      :param page_token: Token for pagination (currently not used by API)

      :returns: List of CorporateActionModel objects

      :raises ValidationError: If date range exceeds 90 days or invalid parameters
      :raises APIRequestError: If the API request fails



   .. py:method:: get_announcement_by_id(announcement_id: str) -> py_alpaca_api.models.corporate_action_model.CorporateActionModel

      Retrieve a specific corporate action announcement by ID.

      :param announcement_id: The unique ID of the announcement

      :returns: CorporateActionModel object

      :raises APIRequestError: If the API request fails or announcement not found



   .. py:method:: get_all_announcements(since: str, until: str, ca_types: list[str], symbol: str | None = None, cusip: str | None = None, date_type: Literal['declaration_date', 'ex_date', 'record_date', 'payable_date'] | None = None) -> list[py_alpaca_api.models.corporate_action_model.CorporateActionModel]

      Retrieve all corporate action announcements.

      Note: The API currently returns all results within the date range
      without pagination, so this method simply calls get_announcements.

      :param since: The start (inclusive) of the date range in YYYY-MM-DD format.
      :param until: The end (inclusive) of the date range in YYYY-MM-DD format.
      :param ca_types: List of corporate action types to return.
      :param symbol: Optional filter by symbol
      :param cusip: Optional filter by CUSIP
      :param date_type: Optional date type for filtering

      :returns: List of all CorporateActionModel objects

      :raises ValidationError: If date range exceeds 90 days or invalid parameters
      :raises APIRequestError: If the API request fails



.. py:class:: Market(base_url: str, headers: dict[str, str])

   .. py:attribute:: base_url


   .. py:attribute:: headers


   .. py:method:: clock() -> py_alpaca_api.models.clock_model.ClockModel

      Retrieves the current market clock.

      :returns: A model containing the current market clock data.
      :rtype: ClockModel



   .. py:method:: calendar(start_date: str, end_date: str) -> pandas.DataFrame

      Retrieves the market calendar for the specified date range.

      :param start_date: The start date of the calendar range in the format "YYYY-MM-DD".
      :type start_date: str
      :param end_date: The end date of the calendar range in the format "YYYY-MM-DD".
      :type end_date: str

      :returns: A DataFrame containing the market calendar data, with columns for the date, settlement date, open time, and close time.
      :rtype: pd.DataFrame



.. py:class:: News(headers: dict[str, str])

   .. py:attribute:: news_url
      :value: 'https://data.alpaca.markets/v1beta1/news'



   .. py:attribute:: headers


   .. py:method:: strip_html(content: str)
      :staticmethod:


      Removes HTML tags and returns the stripped content.

      :param content: The HTML content to be stripped.
      :type content: str

      :returns: The stripped content without HTML tags.
      :rtype: str



   .. py:method:: scrape_article(url: str) -> str | None
      :staticmethod:


      Scrapes the article text from the given URL.

      :param url: The URL of the article.
      :type url: str

      :returns: The text content of the article, or None if the article body is not found.
      :rtype: str | None



   .. py:method:: truncate(text: str, length: int) -> str
      :staticmethod:


      Truncates a given text to a specified length.

      :param text: The text to be truncated.
      :type text: str
      :param length: The maximum length of the truncated text.
      :type length: int

      :returns: The truncated text.
      :rtype: str



   .. py:method:: get_news(symbol: str, limit: int = 6) -> list[dict[str, str]]

      Retrieves news articles related to a given symbol from Benzinga and Yahoo Finance.

      Note: Yahoo Finance has implemented anti-scraping measures that prevent fetching
      full article content. Yahoo news will include title, URL, publish date, and
      summary/description when available, but not full article text.

      :param symbol: The symbol for which to retrieve news articles.
      :type symbol: str
      :param limit: The maximum number of news articles to retrieve. Defaults to 6.
      :type limit: int, optional

      :returns: A list of news articles, sorted by publish date in descending order.
      :rtype: list



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



.. py:class:: Positions(base_url: str, headers: dict[str, str], account: py_alpaca_api.trading.account.Account)

   .. py:attribute:: base_url


   .. py:attribute:: headers


   .. py:attribute:: account


   .. py:method:: close_all(cancel_orders: bool = False) -> str

      Close all positions.

      :param cancel_orders: Whether to cancel open orders associated with the positions.
                            Defaults to False.
      :type cancel_orders: bool, optional

      :returns: A message indicating the number of positions that have been closed.
      :rtype: str

      :raises Exception: If the request to close positions is not successful, an exception is raised with
          the error message from the API response.



   .. py:method:: close(symbol_or_id: str, qty: float | None = None, percentage: int | None = None) -> str

      Closes a position for a given symbol or asset ID.

      :param symbol_or_id: The symbol or asset ID of the position to be closed.
      :type symbol_or_id: str
      :param qty: The quantity of the position to be closed. Defaults to None.
      :type qty: float, optional
      :param percentage: The percentage of the position to be closed. Defaults to None.
      :type percentage: int, optional

      :returns: A message indicating the success or failure of closing the position.
      :rtype: str

      :raises ValueError: If neither quantity nor percentage is provided.
      :raises ValueError: If both quantity and percentage are provided.
      :raises ValueError: If the percentage is not between 0 and 100.
      :raises ValueError: If symbol_or_id is not provided.
      :raises Exception: If the request to close the position fails.



   .. py:method:: get(symbol: str) -> py_alpaca_api.models.position_model.PositionModel

      Retrieves the position for the specified symbol.

      :param symbol: The symbol of the asset for which to retrieve the position.
      :type symbol: str

      :returns: The position for the specified symbol.
      :rtype: PositionModel

      :raises ValueError: If the symbol is not provided or if a position for the specified symbol is not found.



   .. py:method:: get_all(order_by: str = 'profit_pct', order_asc: bool = False) -> pandas.DataFrame

      Retrieves all positions for the user's Alpaca account, including cash positions.

      The positions are returned as a pandas DataFrame, with the following columns:
      - asset_id: The unique identifier for the asset
      - symbol: The symbol for the asset
      - exchange: The exchange the asset is traded on
      - asset_class: The class of the asset (e.g. 'stock', 'crypto')
      - avg_entry_price: The average price at which the position was entered
      - qty: The quantity of the asset held in the position
      - qty_available: The quantity of the asset that is available to trade
      - side: The side of the position (either 'long' or 'short')
      - market_value: The current market value of the position
      - cost_basis: The total cost basis of the position
      - profit_dol: The unrealized profit/loss in dollars
      - profit_pct: The unrealized profit/loss as a percentage
      - intraday_profit_dol: The unrealized intraday profit/loss in dollars
      - intraday_profit_pct: The unrealized intraday profit/loss as a percentage
      - portfolio_pct: The percentage of the total portfolio value that this position represents
      - current_price: The current price of the asset
      - lastday_price: The price of the asset at the end of the previous trading day
      - change_today: The percent change in the asset's price from the previous trading day
      - asset_marginable: Whether the asset is marginable or not

      The positions are sorted based on the provided `order_by` parameter, in ascending or descending order based on the `order_asc` parameter.



   .. py:method:: modify_position_df(positions_df: pandas.DataFrame) -> pandas.DataFrame
      :staticmethod:


      Modifies the given positions DataFrame by renaming columns, converting data types,
      and rounding values.

      :param positions_df: The positions DataFrame to be modified.
      :type positions_df: pd.DataFrame

      :returns: The modified positions DataFrame.
      :rtype: pd.DataFrame



   .. py:method:: cash_position_df()

      Retrieves the user's cash position data as a DataFrame.

      :returns: A DataFrame containing the user's cash position data.
      :rtype: pd.DataFrame



   .. py:method:: exercise(symbol_or_contract_id: str) -> dict

      Exercise a held option contract.

      All available held shares of this option contract will be exercised.
      By default, Alpaca will automatically exercise in-the-money (ITM)
      contracts at expiry.

      :param symbol_or_contract_id: The symbol or contract ID of the option
                                    position to exercise.

      :returns: Response from the API confirming the exercise request.
      :rtype: dict

      :raises APIRequestError: If the exercise request fails.
      :raises ValueError: If symbol_or_contract_id is not provided.

      .. note::

         - Exercise requests will be processed immediately once received.
         - Exercise requests submitted between market close and midnight
           will be rejected.
         - To cancel an exercise request or submit a Do-not-exercise (DNE)
           instruction, contact Alpaca support.



.. py:class:: Recommendations

   .. py:method:: get_recommendations(symbol: str) -> dict[Any, Any] | pandas.DataFrame
      :staticmethod:


      Retrieves the latest recommendations for a given stock symbol.

      :param symbol: The stock symbol for which to retrieve recommendations.
      :type symbol: str

      :returns: A dictionary or DataFrame containing the latest recommendations for the stock symbol.
      :rtype: Union[dict, pd.DataFrame]



   .. py:method:: get_sentiment(symbol: str) -> str

      Retrieves the sentiment for a given stock symbol based on the latest recommendations.

      :param symbol: The stock symbol for which to retrieve the sentiment.
      :type symbol: str

      :returns: The sentiment for the stock symbol, either "BULLISH", "BEARISH", or "NEUTRAL".
      :rtype: str



.. py:class:: Watchlist(base_url: str, headers: dict[str, str])

   .. py:attribute:: base_url


   .. py:attribute:: headers


   .. py:method:: get(watchlist_id: str | None = None, watchlist_name: str | None = None) -> py_alpaca_api.models.watchlist_model.WatchlistModel | str

      Retrieves a watchlist based on the provided watchlist ID or name.

      :param watchlist_id: The ID of the watchlist to retrieve.
      :type watchlist_id: str, optional
      :param watchlist_name: The name of the watchlist to retrieve.
      :type watchlist_name: str, optional

      :returns: The retrieved watchlist.
      :rtype: WatchlistModel

      :raises ValueError: If both watchlist_id and watchlist_name are provided, or if neither is provided.



   .. py:method:: get_all() -> list[py_alpaca_api.models.watchlist_model.WatchlistModel | str]

      Retrieves all watchlists.

      :returns: A list of WatchlistModel objects representing all the watchlists.

      :raises Exception: If the API request fails.



   .. py:method:: create(name: str, symbols: list | str | None = None) -> py_alpaca_api.models.watchlist_model.WatchlistModel | str

      Creates a new watchlist with the given name and symbols.

      :param name: The name of the watchlist.
      :type name: str
      :param symbols: A comma-separated string of symbols to add to the watchlist. Defaults to "".
      :type symbols: str, optional

      :returns: The created watchlist.
      :rtype: WatchlistModel

      :raises SomeException: An exception that may occur during the request.



   .. py:method:: update(watchlist_id: str | None = None, watchlist_name: str | None = None, name: str = '', symbols: list | str | None = None) -> py_alpaca_api.models.watchlist_model.WatchlistModel | str

      Update a watchlist with the specified parameters.

      :param watchlist_id: The ID of the watchlist to update. Either `watchlist_id` or `watchlist_name`
      :type watchlist_id: str, optional
      :param must be provided.:
      :param watchlist_name: The name of the watchlist to update. Either `watchlist_id` or
      :type watchlist_name: str, optional
      :param `watchlist_name` must be provided.:
      :param name: The new name for the watchlist. If not provided, the existing name will be used.
      :type name: str, optional
      :param symbols: A comma-separated string of symbols to update the watchlist with. If not provided,
                      the existing symbols
      :type symbols: str, optional
      :param will be used.:

      :returns: The updated watchlist.
      :rtype: WatchlistModel

      :raises ValueError: If both `watchlist_id` and `watchlist_name` are provided, or if neither `watchlist_id` nor
      :raises watchlist_name:



   .. py:method:: delete(watchlist_id: str | None = None, watchlist_name: str | None = None) -> str

      Deletes a watchlist.

      :param watchlist_id: The ID of the watchlist to delete.
      :type watchlist_id: str, optional
      :param watchlist_name: The name of the watchlist to delete.
      :type watchlist_name: str, optional

      :returns: A message indicating the successful deletion of the watchlist.
      :rtype: str

      :raises ValueError: If both watchlist_id and watchlist_name are provided or if neither is provided.



   .. py:method:: add_asset(watchlist_id: str | None = None, watchlist_name: str | None = None, symbol: str = '') -> py_alpaca_api.models.watchlist_model.WatchlistModel | str

      Adds an asset to a watchlist.

      :param watchlist_id: The ID of the watchlist to add the asset to. If `watchlist_id` is provided,
      :type watchlist_id: str
      :param `watchlist_name` should be None.:
      :param watchlist_name: The name of the watchlist to add the asset to. If `watchlist_name` is provided,
      :type watchlist_name: str
      :param `watchlist_id` should be None.:
      :param symbol: The symbol of the asset to add to the watchlist.
      :type symbol: str

      :returns: The updated watchlist after adding the asset.
      :rtype: WatchlistModel

      :raises ValueError: If both `watchlist_id` and `watchlist_name` are provided or neither is provided.
      :raises ValueError: If `symbol` is not provided.



   .. py:method:: remove_asset(watchlist_id: str | None = None, watchlist_name: str | None = None, symbol: str = '') -> py_alpaca_api.models.watchlist_model.WatchlistModel | str

      Removes an asset from a watchlist.

      :param watchlist_id: The ID of the watchlist. If not provided, the watchlist_name parameter
      :type watchlist_id: str, optional
      :param will be used to:
      :param retrieve the ID. Defaults to None.:
      :param watchlist_name: The name of the watchlist. If not provided, thewatchlist_id parameter
                             will be used to
      :type watchlist_name: str, optional
      :param retrieve the ID. Defaults to None.:
      :param symbol: The symbol of the asset to be removed from the watchlist.
      :type symbol: str

      :returns: The updated watchlist object.
      :rtype: WatchlistModel

      :raises ValueError: If both watchlist_id and watchlist_name are provided, or if symbol is not provided.



   .. py:method:: get_assets(watchlist_id: str | None = None, watchlist_name: str | None = None) -> list

      Retrieves the symbols of assets in a watchlist.

      :param watchlist_id: The ID of the watchlist. Either `watchlist_id` or `watchlist_name`
                           should be provided,
      :type watchlist_id: str, optional
      :param not both. Defaults to None.:
      :param watchlist_name: The name of the watchlist. Either `watchlist_id` or `watchlist_name`
                             should be
      :type watchlist_name: str, optional
      :param provided:
      :param not both. Defaults to None.:

      :returns: A list of symbols of assets in the watchlist.
      :rtype: list

      :raises ValueError: If both `watchlist_id` and `watchlist_name` are provided, or if neither `watchlist_id` nor
      :raises watchlist_name:



.. py:class:: Trading(api_key: str, api_secret: str, api_paper: bool)
