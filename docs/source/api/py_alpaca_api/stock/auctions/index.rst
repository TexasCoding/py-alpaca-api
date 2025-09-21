py_alpaca_api.stock.auctions
============================

.. py:module:: py_alpaca_api.stock.auctions

.. autoapi-nested-parse::

   Historical auctions functionality for Alpaca Market Data API.



Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.auctions.Auctions


Module Contents
---------------

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
