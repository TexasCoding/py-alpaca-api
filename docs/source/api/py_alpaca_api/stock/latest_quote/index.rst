py_alpaca_api.stock.latest_quote
================================

.. py:module:: py_alpaca_api.stock.latest_quote


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.latest_quote.LatestQuote


Module Contents
---------------

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
