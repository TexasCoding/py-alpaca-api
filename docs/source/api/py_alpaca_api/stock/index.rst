py_alpaca_api.stock
===================

.. py:module:: py_alpaca_api.stock


Submodules
----------

.. toctree::
   :maxdepth: 1

   /api/py_alpaca_api/stock/assets/index
   /api/py_alpaca_api/stock/auctions/index
   /api/py_alpaca_api/stock/history/index
   /api/py_alpaca_api/stock/latest_quote/index
   /api/py_alpaca_api/stock/logos/index
   /api/py_alpaca_api/stock/metadata/index
   /api/py_alpaca_api/stock/predictor/index
   /api/py_alpaca_api/stock/quotes/index
   /api/py_alpaca_api/stock/screener/index
   /api/py_alpaca_api/stock/snapshots/index
   /api/py_alpaca_api/stock/trades/index


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.Assets
   py_alpaca_api.stock.Auctions
   py_alpaca_api.stock.History
   py_alpaca_api.stock.LatestQuote
   py_alpaca_api.stock.Logos
   py_alpaca_api.stock.Metadata
   py_alpaca_api.stock.Predictor
   py_alpaca_api.stock.Quotes
   py_alpaca_api.stock.Screener
   py_alpaca_api.stock.Snapshots
   py_alpaca_api.stock.Trades
   py_alpaca_api.stock.Market
   py_alpaca_api.stock.Stock


Package Contents
----------------

.. py:class:: Assets(base_url: str, headers: dict[str, str])

   .. py:attribute:: base_url


   .. py:attribute:: headers


   .. py:method:: get(symbol: str) -> py_alpaca_api.models.asset_model.AssetModel

      Retrieves an AssetModel for the specified symbol.

      :param symbol: The symbol of the asset to retrieve.
      :type symbol: str

      :returns: The AssetModel for the specified asset.
      :rtype: AssetModel

      :raises Exception: If the asset is not a US Equity (stock).



   .. py:method:: get_all(status: str = 'active', exchange: str = '', excluded_exchanges: list[str] | None = None) -> pandas.DataFrame

      Retrieves a DataFrame of all active, fractionable, and tradable assets.

      Excluding those from the OTC exchange.

      :param status: The status of the assets to retrieve.
                     Defaults to "active".
      :type status: str, optional
      :param exchange: The exchange to filter the assets by.
                       Defaults to an empty string, which retrieves assets from
                       all exchanges.
      :type exchange: str, optional
      :param excluded_exchanges: A list of exchanges to
                                 exclude from the results. Defaults to ["OTC"].
      :type excluded_exchanges: List[str], optional

      :returns: A DataFrame containing the retrieved assets.
      :rtype: pd.DataFrame



.. py:class:: Auctions(headers: dict[str, str])

   Handles historical auction data retrieval from Alpaca API.


   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v2/stocks'



   .. py:method:: get_auctions(symbols: str | list[str], start: str, end: str, limit: int = 10000, asof: str | None = None, feed: str = 'iex', page_token: str | None = None, sort: str = 'asc') -> pandas.DataFrame | dict[str, pandas.DataFrame]

      Get historical auction data for one or more symbols.

      Retrieves auction prices (opening and closing auctions) between specified dates.

      :param symbols: Symbol(s) to get auction data for. Can be a string for single symbol
                      or list of strings for multiple symbols.
      :param start: Start date/time in ISO 8601 format (e.g., "2021-01-01" or "2021-01-01T00:00:00Z").
      :param end: End date/time in ISO 8601 format.
      :param limit: Maximum number of auctions to return per symbol. Defaults to 10000.
      :param asof: As-of date for corporate actions adjustments in YYYY-MM-DD format.
      :param feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".
      :param page_token: Pagination token from previous request.
      :param sort: Sort order for results ("asc" or "desc"). Defaults to "asc".

      :returns: pd.DataFrame with auction data.
                For multiple symbols: dict mapping symbols to DataFrames with auction data.
      :rtype: For single symbol

      :raises ValidationError: If parameters are invalid.
      :raises Exception: If the API request fails or returns no data.



   .. py:method:: get_daily_auctions(symbols: str | list[str], start: str, end: str, feed: str = 'iex') -> pandas.DataFrame | dict[str, pandas.DataFrame]

      Get daily auction summary for one or more symbols.

      Retrieves opening and closing auction prices aggregated by day.

      :param symbols: Symbol(s) to get auction data for.
      :param start: Start date in YYYY-MM-DD format.
      :param end: End date in YYYY-MM-DD format.
      :param feed: The data feed to use. Defaults to "iex".

      :returns: DataFrame or dict of DataFrames with daily auction summaries.



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



.. py:class:: LatestQuote(headers: dict[str, str])

   .. py:attribute:: BATCH_SIZE
      :value: 200



   .. py:attribute:: headers


   .. py:method:: get(symbol: list[str] | str | None, feed: str = 'iex', currency: str = 'USD') -> list[py_alpaca_api.models.quote_model.QuoteModel] | py_alpaca_api.models.quote_model.QuoteModel

      Get latest quotes for one or more symbols.

      :param symbol: A string or list of strings representing the stock symbol(s).
      :param feed: The data feed source. Default is "iex".
      :param currency: The currency for the quotes. Default is "USD".

      :returns: A single QuoteModel or list of QuoteModel objects.

      :raises ValueError: If symbol is None/empty or if feed is invalid.



.. py:class:: Logos(headers: dict[str, str])

   Handles company logo retrieval from Alpaca API.


   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v1beta1/logos'



   .. py:method:: get_logo(symbol: str, placeholder: bool = False) -> bytes

      Get the logo for a specific symbol.

      Retrieves the company logo as binary image data.

      :param symbol: The stock symbol to get the logo for.
      :param placeholder: If True, returns a placeholder image when logo is not available.
                          Defaults to False.

      :returns: The logo image as binary data.
      :rtype: bytes

      :raises ValidationError: If the symbol is invalid.
      :raises Exception: If the API request fails.



   .. py:method:: get_logo_url(symbol: str, placeholder: bool = False) -> str

      Get the URL for a symbol's logo.

      This method returns the direct URL to fetch the logo, which can be used
      in HTML img tags or for direct browser access.

      :param symbol: The stock symbol to get the logo URL for.
      :param placeholder: If True, includes placeholder parameter in URL.
                          Defaults to False.

      :returns: The URL to the logo image.
      :rtype: str

      :raises ValidationError: If the symbol is invalid.



   .. py:method:: save_logo(symbol: str, filepath: str, placeholder: bool = False) -> None

      Save a symbol's logo to a file.

      Downloads the logo and saves it to the specified file path.

      :param symbol: The stock symbol to get the logo for.
      :param filepath: The path where the logo should be saved.
      :param placeholder: If True, saves a placeholder image when logo is not available.
                          Defaults to False.

      :raises ValidationError: If the symbol or filepath is invalid.
      :raises Exception: If the API request fails or file cannot be written.



   .. py:method:: get_logo_base64(symbol: str, placeholder: bool = False) -> str

      Get the logo as a base64 encoded string.

      Useful for embedding logos directly in HTML or JSON responses.

      :param symbol: The stock symbol to get the logo for.
      :param placeholder: If True, returns a placeholder image when logo is not available.
                          Defaults to False.

      :returns: The logo image as a base64 encoded string.
      :rtype: str

      :raises ValidationError: If the symbol is invalid.
      :raises Exception: If the API request fails.



   .. py:method:: get_multiple_logos(symbols: list[str], placeholder: bool = False) -> dict[str, bytes | None]

      Get logos for multiple symbols.

      Retrieves logos for multiple symbols in a single batch operation.

      :param symbols: List of stock symbols to get logos for.
      :param placeholder: If True, returns placeholder images when logos are not available.
                          Defaults to False.

      :returns:

                Dictionary mapping symbols to their logo binary data.
                    Symbols without logos will have None as value unless placeholder is True.
      :rtype: dict

      :raises ValidationError: If symbols list is invalid.



.. py:class:: Metadata(headers: dict[str, str])

   Market metadata API for condition codes and exchange codes.


   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v2/stocks/meta'



   .. py:method:: get_exchange_codes(use_cache: bool = True) -> dict[str, str]

      Get the mapping between exchange codes and exchange names.

      :param use_cache: Whether to use cached data if available. Defaults to True.

      :returns: Dictionary mapping exchange codes to exchange names.

      :raises APIRequestError: If the API request fails.



   .. py:method:: get_condition_codes(ticktype: str = 'trade', tape: str = 'A', use_cache: bool = True) -> dict[str, str]

      Get the mapping between condition codes and condition names.

      :param ticktype: Type of conditions to retrieve ("trade" or "quote"). Defaults to "trade".
      :param tape: Market tape ("A" for NYSE, "B" for NASDAQ, "C" for other). Defaults to "A".
      :param use_cache: Whether to use cached data if available. Defaults to True.

      :returns: Dictionary mapping condition codes to condition descriptions.

      :raises ValidationError: If invalid parameters are provided.
      :raises APIRequestError: If the API request fails.



   .. py:method:: get_all_condition_codes(use_cache: bool = True) -> dict[str, dict[str, dict[str, str]]]

      Get all condition codes for all tick types and tapes.

      :param use_cache: Whether to use cached data if available. Defaults to True.

      :returns:

                {
                    "trade": {
                        "A": {condition_code: description, ...},
                        "B": {condition_code: description, ...},
                        "C": {condition_code: description, ...}
                    },
                    "quote": {
                        "A": {condition_code: description, ...},
                        "B": {condition_code: description, ...},
                        "C": {condition_code: description, ...}
                    }
                }
      :rtype: Nested dictionary with structure

      :raises APIRequestError: If any API request fails.



   .. py:method:: clear_cache() -> None

      Clear all cached metadata.

      This forces the next request to fetch fresh data from the API.



   .. py:method:: lookup_exchange(code: str) -> str | None

      Look up an exchange name by its code.

      :param code: The exchange code to look up.

      :returns: The exchange name if found, None otherwise.



   .. py:method:: lookup_condition(code: str, ticktype: str = 'trade', tape: str = 'A') -> str | None

      Look up a condition description by its code.

      :param code: The condition code to look up.
      :param ticktype: Type of condition ("trade" or "quote"). Defaults to "trade".
      :param tape: Market tape ("A", "B", or "C"). Defaults to "A".

      :returns: The condition description if found, None otherwise.



.. py:class:: Predictor(history: py_alpaca_api.stock.history.History, screener: py_alpaca_api.stock.screener.Screener)

   .. py:attribute:: history


   .. py:attribute:: screener


   .. py:method:: get_stock_data(symbol: str, timeframe: str = '1d', start: str = four_years_ago, end: str = yesterday) -> pandas.DataFrame

      Retrieves historical stock data for a given symbol within a specified timeframe.

      :param symbol: The stock symbol to retrieve data for.
      :type symbol: str
      :param timeframe: The timeframe for the data. Defaults to "1d".
      :type timeframe: str, optional
      :param start: The start date for the data. Defaults to four_years_ago.
      :type start: str, optional
      :param end: The end date for the data. Defaults to yesterday.
      :type end: str, optional

      :returns: A DataFrame containing the historical stock data with columns "ds" (date) and "y" (vwap).
      :rtype: pd.DataFrame



   .. py:method:: train_prophet_model(data)
      :staticmethod:


      Trains a Prophet model using the provided data.

      :param data: The input data used for training the model.

      :returns: The trained Prophet model.



   .. py:method:: generate_forecast(model, future_periods=14)
      :staticmethod:


      Generates a forecast using the specified model for a given number of future periods.

      :param model: The model used for forecasting.
      :param future_periods: The number of future periods to forecast.

      :returns: The forecasted value for the next two weeks.



   .. py:method:: get_losers_to_gainers(gain_ratio: float = 10.0, losers_to_scan: int = 200, future_periods: int = 5) -> list


.. py:class:: Quotes(headers: dict[str, str])

   Handles historical quote data retrieval from Alpaca API.


   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v2/stocks'



   .. py:method:: get_historical_quotes(symbols: str | list[str], start: str, end: str, limit: int = 10000, asof: str | None = None, feed: str = 'iex', page_token: str | None = None, sort: str = 'asc') -> pandas.DataFrame | dict[str, pandas.DataFrame]

      Get historical quote data for one or more symbols.

      Retrieves historical quote (bid/ask) data between specified dates.

      :param symbols: Symbol(s) to get quote data for. Can be a string for single symbol
                      or list of strings for multiple symbols.
      :param start: Start date/time in ISO 8601 format (e.g., "2021-01-01" or "2021-01-01T00:00:00Z").
      :param end: End date/time in ISO 8601 format.
      :param limit: Maximum number of quotes to return per symbol. Defaults to 10000.
      :param asof: As-of date for corporate actions adjustments in YYYY-MM-DD format.
      :param feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".
      :param page_token: Pagination token from previous request.
      :param sort: Sort order for results ("asc" or "desc"). Defaults to "asc".

      :returns: pd.DataFrame with quote data.
                For multiple symbols: dict mapping symbols to DataFrames with quote data.
      :rtype: For single symbol

      :raises ValidationError: If parameters are invalid.
      :raises Exception: If the API request fails or returns no data.



.. py:class:: Screener(data_url: str, headers: dict[str, str], asset: py_alpaca_api.stock.assets.Assets, market: py_alpaca_api.trading.market.Market)

   .. py:attribute:: data_url


   .. py:attribute:: headers


   .. py:attribute:: asset


   .. py:attribute:: market


   .. py:attribute:: yesterday
      :value: ''



   .. py:attribute:: day_before_yesterday
      :value: ''



   .. py:method:: filter_stocks(price_greater_than: float, change_condition: collections.abc.Callable[[pandas.DataFrame], pandas.Series], volume_greater_than: int, trade_count_greater_than: int, total_returned: int, ascending_order: bool) -> pandas.DataFrame

      Filter stocks based on given parameters.

      :param price_greater_than: The minimum price threshold for the stocks.
      :param change_condition: A callable function that takes in a DataFrame and returns a boolean Series.
                               This function is used to filter the stocks based on a specific change condition.
      :param volume_greater_than: The minimum volume threshold for the stocks.
      :param trade_count_greater_than: The minimum trade count threshold for the stocks.
      :param total_returned: The number of stocks to return.
      :param ascending_order: A boolean value indicating whether to sort the stocks in ascending order by change value.

      :returns: A pandas DataFrame containing the filtered stocks.



   .. py:method:: losers(price_greater_than: float = 5.0, change_less_than: float = -2.0, volume_greater_than: int = 20000, trade_count_greater_than: int = 2000, total_losers_returned: int = 100) -> pandas.DataFrame

      Returns a filtered DataFrame of stocks that meet the specified conditions for losers.

      :param price_greater_than: The minimum price threshold for stocks to be considered losers. Default is 5.0.
      :type price_greater_than: float
      :param change_less_than: The maximum change threshold for stocks to be considered losers. Default is -2.0.
      :type change_less_than: float
      :param volume_greater_than: The minimum volume threshold for stocks to be considered losers. Default is
      :type volume_greater_than: int
      :param 20000.:
      :param trade_count_greater_than: The minimum trade count threshold for stocks to be considered losers.
                                       Default is 2000.
      :type trade_count_greater_than: int
      :param total_losers_returned: The maximum number of losers to be returned. Default is 100.
      :type total_losers_returned: int

      :returns: A filtered DataFrame containing stocks that meet the specified conditions for losers.
      :rtype: pd.DataFrame



   .. py:method:: gainers(price_greater_than: float = 5.0, change_greater_than: float = 2.0, volume_greater_than: int = 20000, trade_count_greater_than: int = 2000, total_gainers_returned: int = 100) -> pandas.DataFrame

      :param price_greater_than: The minimum price threshold for the stocks to be included in the gainers list.
      :type price_greater_than: float
      :param Default is 5.0.:
      :param change_greater_than: The minimum change (in percentage) threshold for the stocks to be included in
      :type change_greater_than: float
      :param the gainers list.:
      :param Default is 2.0.:
      :param volume_greater_than: The minimum volume threshold for the stocks to be included in the gainers list.
                                  Default is 20000.
      :type volume_greater_than: int
      :param trade_count_greater_than: The minimum trade count threshold for the stocks to be included in the
      :type trade_count_greater_than: int
      :param gainers list. Default is 2000.:
      :param total_gainers_returned: The maximum number of gainers to be returned. Default is 100.
      :type total_gainers_returned: int

      :returns: A Pandas DataFrame containing the stocks that satisfy the criteria for being gainers.
      :rtype: pd.DataFrame



   .. py:method:: set_dates()

      Sets the dates for the screener.

      This method retrieves the last two trading dates from the market calendar
      and assigns them to the `yesterday` and `day_before_yesterday` attributes.

      :returns: None



.. py:class:: Snapshots(headers: dict[str, str])

   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v2/stocks'



   .. py:method:: get_snapshot(symbol: str, feed: str = 'iex') -> py_alpaca_api.models.snapshot_model.SnapshotModel

      Get a snapshot of a single stock symbol.

      The snapshot includes the latest trade, latest quote, minute bar,
      daily bar, and previous daily bar data.

      :param symbol: The stock symbol to get snapshot for.
      :param feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".

      :returns: A SnapshotModel containing the snapshot data.

      :raises ValidationError: If symbol is invalid or feed is invalid.
      :raises APIRequestError: If the API request fails.



   .. py:method:: get_snapshots(symbols: list[str] | str, feed: str = 'iex') -> list[py_alpaca_api.models.snapshot_model.SnapshotModel] | dict[str, py_alpaca_api.models.snapshot_model.SnapshotModel]

      Get snapshots for multiple stock symbols.

      The snapshot includes the latest trade, latest quote, minute bar,
      daily bar, and previous daily bar data for each symbol.

      :param symbols: A list of stock symbols or comma-separated string of symbols.
      :param feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".

      :returns: A dictionary mapping symbols to their SnapshotModel objects, or a list
                of SnapshotModel objects if only one symbol is provided.

      :raises ValidationError: If symbols are invalid or feed is invalid.
      :raises APIRequestError: If the API request fails.



.. py:class:: Trades(headers: dict[str, str])

   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v2'



   .. py:method:: get_trades(symbol: str, start: str, end: str, limit: int = 1000, feed: Literal['iex', 'sip', 'otc'] | None = None, page_token: str | None = None, asof: str | None = None) -> py_alpaca_api.models.trade_model.TradesResponse

      Retrieve historical trades for a symbol.

      :param symbol: The stock symbol to retrieve trades for
      :param start: Start time in RFC-3339 format (YYYY-MM-DDTHH:MM:SSZ)
      :param end: End time in RFC-3339 format (YYYY-MM-DDTHH:MM:SSZ)
      :param limit: Number of trades to return (1-10000, default 1000)
      :param feed: Data feed to use (iex, sip, otc)
      :param page_token: Token for pagination
      :param asof: As-of time for historical data in RFC-3339 format

      :returns: TradesResponse with list of trades and pagination token

      :raises ValidationError: If parameters are invalid
      :raises APIRequestError: If the API request fails



   .. py:method:: get_latest_trade(symbol: str, feed: Literal['iex', 'sip', 'otc'] | None = None, asof: str | None = None) -> py_alpaca_api.models.trade_model.TradeModel

      Get the latest trade for a symbol.

      :param symbol: The stock symbol to retrieve latest trade for
      :param feed: Data feed to use (iex, sip, otc)
      :param asof: As-of time for historical data in RFC-3339 format

      :returns: TradeModel with the latest trade data

      :raises ValidationError: If symbol is invalid
      :raises APIRequestError: If the API request fails



   .. py:method:: get_trades_multi(symbols: list[str], start: str, end: str, limit: int = 1000, feed: Literal['iex', 'sip', 'otc'] | None = None, page_token: str | None = None, asof: str | None = None) -> dict[str, py_alpaca_api.models.trade_model.TradesResponse]

      Retrieve historical trades for multiple symbols.

      :param symbols: List of stock symbols (max 100)
      :param start: Start time in RFC-3339 format
      :param end: End time in RFC-3339 format
      :param limit: Number of trades per symbol (1-10000, default 1000)
      :param feed: Data feed to use
      :param page_token: Token for pagination
      :param asof: As-of time for historical data

      :returns: Dictionary mapping symbols to TradesResponse objects

      :raises ValidationError: If parameters are invalid
      :raises APIRequestError: If the API request fails



   .. py:method:: get_latest_trades_multi(symbols: list[str], feed: Literal['iex', 'sip', 'otc'] | None = None, asof: str | None = None) -> dict[str, py_alpaca_api.models.trade_model.TradeModel]

      Get latest trades for multiple symbols.

      :param symbols: List of stock symbols (max 100)
      :param feed: Data feed to use
      :param asof: As-of time for historical data

      :returns: Dictionary mapping symbols to their latest TradeModel

      :raises ValidationError: If parameters are invalid
      :raises APIRequestError: If the API request fails



   .. py:method:: get_all_trades(symbol: str, start: str, end: str, feed: Literal['iex', 'sip', 'otc'] | None = None, asof: str | None = None) -> list[py_alpaca_api.models.trade_model.TradeModel]

      Retrieve all trades for a symbol with automatic pagination.

      :param symbol: The stock symbol
      :param start: Start time in RFC-3339 format
      :param end: End time in RFC-3339 format
      :param feed: Data feed to use
      :param asof: As-of time for historical data

      :returns: List of all TradeModel objects across all pages

      :raises ValidationError: If parameters are invalid
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



.. py:class:: Stock(api_key: str, api_secret: str, api_paper: bool, market: py_alpaca_api.trading.market.Market)
