py_alpaca_api.models.snapshot_model
===================================

.. py:module:: py_alpaca_api.models.snapshot_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.snapshot_model.BarModel
   py_alpaca_api.models.snapshot_model.SnapshotModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.snapshot_model.bar_class_from_dict
   py_alpaca_api.models.snapshot_model.snapshot_class_from_dict


Module Contents
---------------

.. py:class:: BarModel

   .. py:attribute:: timestamp
      :type:  str


   .. py:attribute:: open
      :type:  float


   .. py:attribute:: high
      :type:  float


   .. py:attribute:: low
      :type:  float


   .. py:attribute:: close
      :type:  float


   .. py:attribute:: volume
      :type:  int


   .. py:attribute:: trade_count
      :type:  int | None
      :value: None



   .. py:attribute:: vwap
      :type:  float | None
      :value: None



.. py:class:: SnapshotModel

   .. py:attribute:: symbol
      :type:  str


   .. py:attribute:: latest_trade
      :type:  py_alpaca_api.models.trade_model.TradeModel | None
      :value: None



   .. py:attribute:: latest_quote
      :type:  py_alpaca_api.models.quote_model.QuoteModel | None
      :value: None



   .. py:attribute:: minute_bar
      :type:  BarModel | None
      :value: None



   .. py:attribute:: daily_bar
      :type:  BarModel | None
      :value: None



   .. py:attribute:: prev_daily_bar
      :type:  BarModel | None
      :value: None



.. py:function:: bar_class_from_dict(data: dict) -> BarModel

.. py:function:: snapshot_class_from_dict(data: dict) -> SnapshotModel
