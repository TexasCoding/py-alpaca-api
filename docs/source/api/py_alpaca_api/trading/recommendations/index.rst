py_alpaca_api.trading.recommendations
=====================================

.. py:module:: py_alpaca_api.trading.recommendations


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.recommendations.Recommendations


Module Contents
---------------

.. py:class:: Recommendations

   .. py:method:: get_recommendations(symbol: str) -> dict[Any, Any] | pandas.DataFrame
      :staticmethod:


      Retrieves the latest recommendations for a given stock symbol.

      :param symbol: The stock symbol for which to retrieve recommendations.
      :type symbol: str

      :returns: A dictionary or DataFrame containing the latest recommendations for the stock symbol.
      :rtype: Union[dict, pd.DataFrame]



   .. py:method:: get_sentiment(symbol: str) -> str

      Retrieves the sentiment for a given stock symbol based on the latest recommendations.

      :param symbol: The stock symbol for which to retrieve the sentiment.
      :type symbol: str

      :returns: The sentiment for the stock symbol, either "BULLISH", "BEARISH", or "NEUTRAL".
      :rtype: str
