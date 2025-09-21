py_alpaca_api.stock.history
===========================

.. py:module:: py_alpaca_api.stock.history


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.history.History


Module Contents
---------------

.. py:class:: History(data_url: str, headers: dict[str, str], asset: py_alpaca_api.stock.assets.Assets)

   .. py:attribute:: BATCH_SIZE
      :value: 200



   .. py:attribute:: data_url


   .. py:attribute:: headers


   .. py:attribute:: asset


   .. py:method:: check_if_stock(symbol: str) -> py_alpaca_api.models.asset_model.AssetModel

      Check if the asset corresponding to the symbol is a stock.

      :param symbol: The symbol of the asset to be checked.
      :type symbol: str

      :returns: The asset information for the given symbol.
      :rtype: AssetModel

      :raises ValueError: If there is an error getting the asset information or if the asset is not a stock.



   .. py:method:: get_stock_data(symbol: str | list[str], start: str, end: str, timeframe: str = '1d', feed: str = 'sip', currency: str = 'USD', limit: int = 1000, sort: str = 'asc', adjustment: str = 'raw') -> pandas.DataFrame

      Retrieves historical stock data for one or more symbols within a specified date range and timeframe.

      :param symbol: The stock symbol(s) to fetch data for. Can be a single symbol string or list of symbols.
      :param start: The start date for historical data in the format "YYYY-MM-DD".
      :param end: The end date for historical data in the format "YYYY-MM-DD".
      :param timeframe: The timeframe for the historical data. Default is "1d".
      :param feed: The data feed source. Default is "sip".
      :param currency: The currency for historical data. Default is "USD".
      :param limit: The number of data points to fetch per symbol. Default is 1000.
      :param sort: The sort order for the data. Default is "asc".
      :param adjustment: The adjustment for historical data. Default is "raw".

      :returns: A pandas DataFrame containing the historical stock data for the given symbol(s) and time range.

      :raises ValueError: If the given timeframe is not one of the allowed values.



   .. py:method:: preprocess_multi_data(symbols_data: dict[str, list[collections.defaultdict]]) -> pandas.DataFrame
      :staticmethod:


      Preprocess data for multiple symbols.

      :param symbols_data: A dictionary mapping symbols to their bar data.

      :returns: A pandas DataFrame containing the preprocessed historical stock data for all symbols.



   .. py:method:: preprocess_data(symbol_data: list[collections.defaultdict], symbol: str) -> pandas.DataFrame
      :staticmethod:


      Prepross data
      Preprocesses the given symbol data by converting it to a pandas DataFrame and performing various
      data transformations.

      :param symbol_data: A list of defaultdict objects representing the JSON response data.
      :param symbol: A string representing the symbol or ticker for the stock data.

      :returns: A pandas DataFrame containing the preprocessed historical stock data.



   .. py:method:: get_historical_data(symbols: list[str], url: str, params: dict, is_single: bool) -> dict[str, list[collections.defaultdict]]

      Retrieves historical data for given symbol(s).

      :param symbols: List of symbols for which to retrieve historical data.
      :param url: The URL to send the request to.
      :param params: Additional parameters to include in the request.
      :param is_single: Whether this is a single-symbol request.

      :returns: A dictionary mapping symbols to their historical data.
      :rtype: dict[str, list[defaultdict]]



   .. py:method:: get_latest_bars(symbols: str | list[str], feed: str = 'iex', currency: str = 'USD') -> pandas.DataFrame | dict[str, pandas.DataFrame]

      Get the latest bars for one or more symbols.

      The latest bars endpoint returns the most recent minute bar for each requested symbol.

      :param symbols: Symbol(s) to get latest bars for. Can be a string for single symbol
                      or list of strings for multiple symbols.
      :param feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".
      :param currency: The currency for the returned prices. Defaults to "USD".

      :returns: pd.DataFrame with the latest bar data.
                For multiple symbols: dict mapping symbols to DataFrames with latest bar data.
      :rtype: For single symbol

      :raises ValueError: If feed is invalid or symbols is empty.
      :raises Exception: If the API request fails or returns no data.
