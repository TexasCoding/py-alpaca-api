py_alpaca_api.trading.positions
===============================

.. py:module:: py_alpaca_api.trading.positions


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.positions.Positions


Module Contents
---------------

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
