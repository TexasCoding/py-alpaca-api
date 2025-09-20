py_alpaca_api.models.trade_model
================================

.. py:module:: py_alpaca_api.models.trade_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.trade_model.TradeModel
   py_alpaca_api.models.trade_model.LatestTradeModel
   py_alpaca_api.models.trade_model.TradesResponse


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.trade_model.trade_class_from_dict
   py_alpaca_api.models.trade_model.extract_trades_data


Module Contents
---------------

.. py:class:: TradeModel

   Model for individual stock trade data.


   .. py:attribute:: timestamp
      :type:  str


   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: exchange
      :type:  str


   .. py:attribute:: price
      :type:  float


   .. py:attribute:: size
      :type:  int


   .. py:attribute:: conditions
      :type:  list[str] | None


   .. py:attribute:: id
      :type:  int


   .. py:attribute:: tape
      :type:  str


.. py:function:: trade_class_from_dict(data: dict[str, Any], symbol: str | None = None) -> TradeModel

   Create TradeModel from API response dictionary.

   :param data: Dictionary containing trade data from API
   :param symbol: Optional symbol to use if not in data

   :returns: TradeModel instance


.. py:class:: LatestTradeModel

   Model for latest trade data with symbol.


   .. py:attribute:: trade
      :type:  TradeModel


   .. py:attribute:: symbol
      :type:  str


.. py:class:: TradesResponse

   Response model for trades endpoint with pagination.


   .. py:attribute:: trades
      :type:  list[TradeModel]


   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: next_page_token
      :type:  str | None
      :value: None



.. py:function:: extract_trades_data(data: dict[str, Any]) -> dict[str, Any]

   Extract and transform trades data from API response.

   :param data: Raw API response data

   :returns: Transformed dictionary ready for model creation
