py_alpaca_api.stock.snapshots
=============================

.. py:module:: py_alpaca_api.stock.snapshots


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.snapshots.Snapshots


Module Contents
---------------

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
