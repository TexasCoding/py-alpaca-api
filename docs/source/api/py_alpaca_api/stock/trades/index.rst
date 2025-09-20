py_alpaca_api.stock.trades
==========================

.. py:module:: py_alpaca_api.stock.trades


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.trades.Trades


Module Contents
---------------

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
