py_alpaca_api.trading.watchlists
================================

.. py:module:: py_alpaca_api.trading.watchlists


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.watchlists.Watchlist


Module Contents
---------------

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
