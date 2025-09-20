py_alpaca_api.trading.account
=============================

.. py:module:: py_alpaca_api.trading.account


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.account.Account


Module Contents
---------------

.. py:class:: Account(headers: dict[str, str], base_url: str)

   .. py:attribute:: headers


   .. py:attribute:: base_url


   .. py:method:: get() -> py_alpaca_api.models.account_model.AccountModel

      Retrieves the user's account information.

      :returns: The user's account model.
      :rtype: AccountModel



   .. py:method:: activities(activity_type: str, date: str | None = None, until_date: str | None = None) -> list[py_alpaca_api.models.account_activity_model.AccountActivityModel]

      Retrieves the account activities for the specified activity type.

      Optionally filtered by date or until date.

      :param activity_type: The type of account activity to retrieve.
      :type activity_type: str
      :param date: The date to filter the activities by.
                   If provided, only activities on this date will be returned.
      :type date: str, optional
      :param until_date: The date to filter the activities up to.
                         If provided, only activities up to and including this date
                         will be returned.
      :type until_date: str, optional

      :returns:

                A list of account activity models
                    representing the retrieved activities.
      :rtype: List[AccountActivityModel]

      :raises ValueError: If the activity type is not provided, or if both
          date and until_date are provided.



   .. py:method:: portfolio_history(period: str = '1W', timeframe: str = '1D', intraday_reporting: str = 'market_hours') -> pandas.DataFrame

      Retrieves portfolio history data.

      :param period: The period of time for which the portfolio history
                     is requested. Defaults to "1W" (1 week).
      :type period: str
      :param timeframe: The timeframe for the intervals of the portfolio
                        history. Defaults to "1D" (1 day).
      :type timeframe: str
      :param intraday_reporting: The type of intraday reporting to be used.
                                 Defaults to "market_hours".
      :type intraday_reporting: str

      :returns: A pandas DataFrame containing the portfolio history data.
      :rtype: pd.DataFrame

      :raises Exception: If the request to the Alpaca API fails.



   .. py:method:: get_configuration() -> py_alpaca_api.models.account_config_model.AccountConfigModel

      Retrieves the current account configuration settings.

      :returns: The current account configuration.
      :rtype: AccountConfigModel

      :raises APIRequestError: If the request to retrieve configuration fails.



   .. py:method:: update_configuration(dtbp_check: str | None = None, fractional_trading: bool | None = None, max_margin_multiplier: str | None = None, no_shorting: bool | None = None, pdt_check: str | None = None, ptp_no_exception_entry: bool | None = None, suspend_trade: bool | None = None, trade_confirm_email: str | None = None) -> py_alpaca_api.models.account_config_model.AccountConfigModel

      Updates the account configuration settings.

      :param dtbp_check: Day trade buying power check ("entry", "exit", "both")
      :param fractional_trading: Whether to enable fractional trading
      :param max_margin_multiplier: Maximum margin multiplier ("1", "2", "4")
      :param no_shorting: Whether to disable short selling
      :param pdt_check: Pattern day trader check ("entry", "exit", "both")
      :param ptp_no_exception_entry: Whether to enable PTP no exception entry
      :param suspend_trade: Whether to suspend trading
      :param trade_confirm_email: Trade confirmation emails ("all", "none")

      :returns: The updated account configuration.
      :rtype: AccountConfigModel

      :raises APIRequestError: If the request to update configuration fails.
      :raises ValueError: If invalid parameter values are provided.
