py_alpaca_api.models.watchlist_model
====================================

.. py:module:: py_alpaca_api.models.watchlist_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.watchlist_model.WatchlistModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.watchlist_model.process_assets
   py_alpaca_api.models.watchlist_model.watchlist_class_from_dict


Module Contents
---------------

.. py:class:: WatchlistModel

   .. py:attribute:: id
      :type:  str


   .. py:attribute:: account_id
      :type:  str


   .. py:attribute:: created_at
      :type:  datetime.datetime


   .. py:attribute:: updated_at
      :type:  datetime.datetime


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: assets
      :type:  list[py_alpaca_api.models.asset_model.AssetModel]


.. py:function:: process_assets(assets: list[dict]) -> list[py_alpaca_api.models.asset_model.AssetModel]

   Process a list of assets.

   This function takes a list of asset dictionaries and returns a list of AssetModel objects.
   Each asset dictionary should contain the necessary information to create an AssetModel object.

   :param assets: A list of asset dictionaries.
   :type assets: List[Dict]

   :returns: A list of AssetModel objects.
   :rtype: List[AssetModel]


.. py:function:: watchlist_class_from_dict(data_dict: dict) -> WatchlistModel

   :param data_dict: A dictionary containing the data needed to create a WatchlistModel object.

   :returns: A new instance of the WatchlistModel created from the data in the input dictionary.
