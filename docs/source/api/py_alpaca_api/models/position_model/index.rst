py_alpaca_api.models.position_model
===================================

.. py:module:: py_alpaca_api.models.position_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.position_model.PositionModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.position_model.position_class_from_dict


Module Contents
---------------

.. py:class:: PositionModel

   .. py:attribute:: asset_id
      :type:  str


   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: exchange
      :type:  str


   .. py:attribute:: asset_class
      :type:  str


   .. py:attribute:: avg_entry_price
      :type:  float


   .. py:attribute:: qty
      :type:  float


   .. py:attribute:: qty_available
      :type:  float


   .. py:attribute:: side
      :type:  str


   .. py:attribute:: market_value
      :type:  float


   .. py:attribute:: cost_basis
      :type:  float


   .. py:attribute:: profit_dol
      :type:  float


   .. py:attribute:: profit_pct
      :type:  float


   .. py:attribute:: intraday_profit_dol
      :type:  float


   .. py:attribute:: intraday_profit_pct
      :type:  float


   .. py:attribute:: portfolio_pct
      :type:  float


   .. py:attribute:: current_price
      :type:  float


   .. py:attribute:: lastday_price
      :type:  float


   .. py:attribute:: change_today
      :type:  float


   .. py:attribute:: asset_marginable
      :type:  bool


.. py:function:: position_class_from_dict(data_dict: dict) -> PositionModel

   Returns a PositionModel object created from a given data dictionary.

   :param data_dict: A dictionary containing the data for creating a PositionModel object.

   :returns: A PositionModel object created using the data from the dictionary.
   :rtype: PositionModel
