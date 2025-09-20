py_alpaca_api.stock.predictor
=============================

.. py:module:: py_alpaca_api.stock.predictor


Attributes
----------

.. autoapisummary::

   py_alpaca_api.stock.predictor.yesterday
   py_alpaca_api.stock.predictor.four_years_ago
   py_alpaca_api.stock.predictor.logger


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.predictor.Predictor


Module Contents
---------------

.. py:data:: yesterday

.. py:data:: four_years_ago

.. py:data:: logger

.. py:class:: Predictor(history: py_alpaca_api.stock.history.History, screener: py_alpaca_api.stock.screener.Screener)

   .. py:attribute:: history


   .. py:attribute:: screener


   .. py:method:: get_stock_data(symbol: str, timeframe: str = '1d', start: str = four_years_ago, end: str = yesterday) -> pandas.DataFrame

      Retrieves historical stock data for a given symbol within a specified timeframe.

      :param symbol: The stock symbol to retrieve data for.
      :type symbol: str
      :param timeframe: The timeframe for the data. Defaults to "1d".
      :type timeframe: str, optional
      :param start: The start date for the data. Defaults to four_years_ago.
      :type start: str, optional
      :param end: The end date for the data. Defaults to yesterday.
      :type end: str, optional

      :returns: A DataFrame containing the historical stock data with columns "ds" (date) and "y" (vwap).
      :rtype: pd.DataFrame



   .. py:method:: train_prophet_model(data)
      :staticmethod:


      Trains a Prophet model using the provided data.

      :param data: The input data used for training the model.

      :returns: The trained Prophet model.



   .. py:method:: generate_forecast(model, future_periods=14)
      :staticmethod:


      Generates a forecast using the specified model for a given number of future periods.

      :param model: The model used for forecasting.
      :param future_periods: The number of future periods to forecast.

      :returns: The forecasted value for the next two weeks.



   .. py:method:: get_losers_to_gainers(gain_ratio: float = 10.0, losers_to_scan: int = 200, future_periods: int = 5) -> list
