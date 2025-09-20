py_alpaca_api.stock.assets
==========================

.. py:module:: py_alpaca_api.stock.assets


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.assets.Assets


Module Contents
---------------

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
