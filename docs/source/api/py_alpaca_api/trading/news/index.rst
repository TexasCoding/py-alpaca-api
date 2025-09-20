py_alpaca_api.trading.news
==========================

.. py:module:: py_alpaca_api.trading.news


Attributes
----------

.. autoapisummary::

   py_alpaca_api.trading.news.logger
   py_alpaca_api.trading.news.yfinance_logger
   py_alpaca_api.trading.news.START_DATE
   py_alpaca_api.trading.news.END_DATE


Classes
-------

.. autoapisummary::

   py_alpaca_api.trading.news.News


Module Contents
---------------

.. py:data:: logger

.. py:data:: yfinance_logger

.. py:data:: START_DATE

.. py:data:: END_DATE

.. py:class:: News(headers: dict[str, str])

   .. py:attribute:: news_url
      :value: 'https://data.alpaca.markets/v1beta1/news'



   .. py:attribute:: headers


   .. py:method:: strip_html(content: str)
      :staticmethod:


      Removes HTML tags and returns the stripped content.

      :param content: The HTML content to be stripped.
      :type content: str

      :returns: The stripped content without HTML tags.
      :rtype: str



   .. py:method:: scrape_article(url: str) -> str | None
      :staticmethod:


      Scrapes the article text from the given URL.

      :param url: The URL of the article.
      :type url: str

      :returns: The text content of the article, or None if the article body is not found.
      :rtype: str | None



   .. py:method:: truncate(text: str, length: int) -> str
      :staticmethod:


      Truncates a given text to a specified length.

      :param text: The text to be truncated.
      :type text: str
      :param length: The maximum length of the truncated text.
      :type length: int

      :returns: The truncated text.
      :rtype: str



   .. py:method:: get_news(symbol: str, limit: int = 6) -> list[dict[str, str]]

      Retrieves news articles related to a given symbol from Benzinga and Yahoo Finance.

      Note: Yahoo Finance has implemented anti-scraping measures that prevent fetching
      full article content. Yahoo news will include title, URL, publish date, and
      summary/description when available, but not full article text.

      :param symbol: The symbol for which to retrieve news articles.
      :type symbol: str
      :param limit: The maximum number of news articles to retrieve. Defaults to 6.
      :type limit: int, optional

      :returns: A list of news articles, sorted by publish date in descending order.
      :rtype: list
