py_alpaca_api.stock.quotes
==========================

.. py:module:: py_alpaca_api.stock.quotes

.. autoapi-nested-parse::

   Historical quotes functionality for Alpaca Market Data API.



Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.quotes.Quotes


Module Contents
---------------

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
