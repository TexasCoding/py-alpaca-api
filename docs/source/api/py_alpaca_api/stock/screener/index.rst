py_alpaca_api.stock.screener
============================

.. py:module:: py_alpaca_api.stock.screener


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.screener.Screener


Module Contents
---------------

.. py:class:: Screener(data_url: str, headers: dict[str, str], asset: py_alpaca_api.stock.assets.Assets, market: py_alpaca_api.trading.market.Market)

   .. py:attribute:: data_url


   .. py:attribute:: headers


   .. py:attribute:: asset


   .. py:attribute:: market


   .. py:attribute:: yesterday
      :value: ''



   .. py:attribute:: day_before_yesterday
      :value: ''



   .. py:method:: filter_stocks(price_greater_than: float, change_condition: collections.abc.Callable[[pandas.DataFrame], pandas.Series], volume_greater_than: int, trade_count_greater_than: int, total_returned: int, ascending_order: bool) -> pandas.DataFrame

      Filter stocks based on given parameters.

      :param price_greater_than: The minimum price threshold for the stocks.
      :param change_condition: A callable function that takes in a DataFrame and returns a boolean Series.
                               This function is used to filter the stocks based on a specific change condition.
      :param volume_greater_than: The minimum volume threshold for the stocks.
      :param trade_count_greater_than: The minimum trade count threshold for the stocks.
      :param total_returned: The number of stocks to return.
      :param ascending_order: A boolean value indicating whether to sort the stocks in ascending order by change value.

      :returns: A pandas DataFrame containing the filtered stocks.



   .. py:method:: losers(price_greater_than: float = 5.0, change_less_than: float = -2.0, volume_greater_than: int = 20000, trade_count_greater_than: int = 2000, total_losers_returned: int = 100) -> pandas.DataFrame

      Returns a filtered DataFrame of stocks that meet the specified conditions for losers.

      :param price_greater_than: The minimum price threshold for stocks to be considered losers. Default is 5.0.
      :type price_greater_than: float
      :param change_less_than: The maximum change threshold for stocks to be considered losers. Default is -2.0.
      :type change_less_than: float
      :param volume_greater_than: The minimum volume threshold for stocks to be considered losers. Default is
      :type volume_greater_than: int
      :param 20000.:
      :param trade_count_greater_than: The minimum trade count threshold for stocks to be considered losers.
                                       Default is 2000.
      :type trade_count_greater_than: int
      :param total_losers_returned: The maximum number of losers to be returned. Default is 100.
      :type total_losers_returned: int

      :returns: A filtered DataFrame containing stocks that meet the specified conditions for losers.
      :rtype: pd.DataFrame



   .. py:method:: gainers(price_greater_than: float = 5.0, change_greater_than: float = 2.0, volume_greater_than: int = 20000, trade_count_greater_than: int = 2000, total_gainers_returned: int = 100) -> pandas.DataFrame

      :param price_greater_than: The minimum price threshold for the stocks to be included in the gainers list.
      :type price_greater_than: float
      :param Default is 5.0.:
      :param change_greater_than: The minimum change (in percentage) threshold for the stocks to be included in
      :type change_greater_than: float
      :param the gainers list.:
      :param Default is 2.0.:
      :param volume_greater_than: The minimum volume threshold for the stocks to be included in the gainers list.
                                  Default is 20000.
      :type volume_greater_than: int
      :param trade_count_greater_than: The minimum trade count threshold for the stocks to be included in the
      :type trade_count_greater_than: int
      :param gainers list. Default is 2000.:
      :param total_gainers_returned: The maximum number of gainers to be returned. Default is 100.
      :type total_gainers_returned: int

      :returns: A Pandas DataFrame containing the stocks that satisfy the criteria for being gainers.
      :rtype: pd.DataFrame



   .. py:method:: set_dates()

      Sets the dates for the screener.

      This method retrieves the last two trading dates from the market calendar
      and assigns them to the `yesterday` and `day_before_yesterday` attributes.

      :returns: None
