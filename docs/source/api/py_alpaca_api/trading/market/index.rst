py_alpaca_api.trading.market
============================

.. py:module:: py_alpaca_api.trading.market


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.market.Market


Module Contents
---------------

.. py:class:: Market(base_url: str, headers: dict[str, str])

   .. py:attribute:: base_url


   .. py:attribute:: headers


   .. py:method:: clock() -> py_alpaca_api.models.clock_model.ClockModel

      Retrieves the current market clock.

      :returns: A model containing the current market clock data.
      :rtype: ClockModel



   .. py:method:: calendar(start_date: str, end_date: str) -> pandas.DataFrame

      Retrieves the market calendar for the specified date range.

      :param start_date: The start date of the calendar range in the format "YYYY-MM-DD".
      :type start_date: str
      :param end_date: The end date of the calendar range in the format "YYYY-MM-DD".
      :type end_date: str

      :returns: A DataFrame containing the market calendar data, with columns for the date, settlement date, open time, and close time.
      :rtype: pd.DataFrame
