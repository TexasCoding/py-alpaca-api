py_alpaca_api.models.account_config_model
=========================================

.. py:module:: py_alpaca_api.models.account_config_model


Classes
-------

.. autoapisummary::

   py_alpaca_api.models.account_config_model.AccountConfigModel


Functions
---------

.. autoapisummary::

   py_alpaca_api.models.account_config_model.account_config_class_from_dict


Module Contents
---------------

.. py:class:: AccountConfigModel

   Model for account configuration settings.

   .. attribute:: dtbp_check

      Day trade buying power check setting ("entry", "exit", "both")

   .. attribute:: fractional_trading

      Whether fractional trading is enabled

   .. attribute:: max_margin_multiplier

      Maximum margin multiplier allowed ("1", "2", "4")

   .. attribute:: no_shorting

      Whether short selling is disabled

   .. attribute:: pdt_check

      Pattern day trader check setting ("entry", "exit", "both")

   .. attribute:: ptp_no_exception_entry

      Whether PTP no exception entry is enabled

   .. attribute:: suspend_trade

      Whether trading is suspended

   .. attribute:: trade_confirm_email

      Trade confirmation email setting ("all", "none")


   .. py:attribute:: dtbp_check
      :type:  str


   .. py:attribute:: fractional_trading
      :type:  bool


   .. py:attribute:: max_margin_multiplier
      :type:  str


   .. py:attribute:: no_shorting
      :type:  bool


   .. py:attribute:: pdt_check
      :type:  str


   .. py:attribute:: ptp_no_exception_entry
      :type:  bool


   .. py:attribute:: suspend_trade
      :type:  bool


   .. py:attribute:: trade_confirm_email
      :type:  str


.. py:function:: account_config_class_from_dict(data: dict) -> AccountConfigModel

   Create AccountConfigModel from API response dictionary.

   :param data: Dictionary containing account configuration data from API

   :returns: AccountConfigModel instance
