py_alpaca_api.models.account_model
==================================

.. py:module:: py_alpaca_api.models.account_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.account_model.AccountModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.account_model.account_class_from_dict


Module Contents
---------------

.. py:class:: AccountModel

   .. py:attribute:: id
      :type:  str


   .. py:attribute:: account_number
      :type:  str


   .. py:attribute:: status
      :type:  str


   .. py:attribute:: crypto_status
      :type:  str


   .. py:attribute:: options_approved_level
      :type:  int


   .. py:attribute:: options_trading_level
      :type:  int


   .. py:attribute:: currency
      :type:  str


   .. py:attribute:: buying_power
      :type:  float


   .. py:attribute:: regt_buying_power
      :type:  float


   .. py:attribute:: daytrading_buying_power
      :type:  float


   .. py:attribute:: effective_buying_power
      :type:  float


   .. py:attribute:: non_marginable_buying_power
      :type:  float


   .. py:attribute:: options_buying_power
      :type:  float


   .. py:attribute:: bod_dtbp
      :type:  float


   .. py:attribute:: cash
      :type:  float


   .. py:attribute:: accrued_fees
      :type:  float


   .. py:attribute:: pending_transfer_in
      :type:  float


   .. py:attribute:: portfolio_value
      :type:  float


   .. py:attribute:: pattern_day_trader
      :type:  bool


   .. py:attribute:: trading_blocked
      :type:  bool


   .. py:attribute:: transfers_blocked
      :type:  bool


   .. py:attribute:: account_blocked
      :type:  bool


   .. py:attribute:: created_at
      :type:  datetime.datetime


   .. py:attribute:: trade_suspended_by_user
      :type:  bool


   .. py:attribute:: multiplier
      :type:  int


   .. py:attribute:: shorting_enabled
      :type:  bool


   .. py:attribute:: equity
      :type:  float


   .. py:attribute:: last_equity
      :type:  float


   .. py:attribute:: long_market_value
      :type:  float


   .. py:attribute:: short_market_value
      :type:  float


   .. py:attribute:: position_market_value
      :type:  float


   .. py:attribute:: initial_margin
      :type:  float


   .. py:attribute:: maintenance_margin
      :type:  float


   .. py:attribute:: last_maintenance_margin
      :type:  float


   .. py:attribute:: sma
      :type:  float


   .. py:attribute:: daytrade_count
      :type:  int


   .. py:attribute:: balance_asof
      :type:  str


   .. py:attribute:: crypto_tier
      :type:  int


   .. py:attribute:: intraday_adjustments
      :type:  int


   .. py:attribute:: pending_reg_taf_fees
      :type:  float


.. py:function:: account_class_from_dict(data_dict: dict) -> AccountModel

   Converts a dictionary into an instance of the `AccountModel`.

   :param data_dict: A dictionary containing the data for the `AccountModel` instance.
   :type data_dict: dict

   :returns: An instance of the `AccountModel` created from the provided dictionary.
   :rtype: AccountModel
