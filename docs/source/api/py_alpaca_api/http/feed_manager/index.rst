py_alpaca_api.http.feed_manager
===============================

.. py:module:: py_alpaca_api.http.feed_manager


Attributes
----------

.. autoapisummary::

   py_alpaca_api.http.feed_manager.logger


Classes
-------

.. autoapisummary::

   py_alpaca_api.http.feed_manager.FeedType
   py_alpaca_api.http.feed_manager.SubscriptionLevel
   py_alpaca_api.http.feed_manager.FeedConfig
   py_alpaca_api.http.feed_manager.FeedManager


Module Contents
---------------

.. py:data:: logger

.. py:class:: FeedType(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Available data feed types.


   .. py:attribute:: SIP
      :value: 'sip'



   .. py:attribute:: IEX
      :value: 'iex'



   .. py:attribute:: OTC
      :value: 'otc'



   .. py:method:: from_string(value: str) -> FeedType
      :classmethod:


      Create FeedType from string value.



.. py:class:: SubscriptionLevel(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   User subscription levels.


   .. py:attribute:: BASIC
      :value: 'basic'



   .. py:attribute:: UNLIMITED
      :value: 'unlimited'



   .. py:attribute:: BUSINESS
      :value: 'business'



   .. py:method:: from_error(error_message: str) -> SubscriptionLevel | None
      :classmethod:


      Detect subscription level from error message.



.. py:class:: FeedConfig

   Configuration for feed management.


   .. py:attribute:: preferred_feed
      :type:  FeedType


   .. py:attribute:: fallback_feeds
      :type:  list[FeedType]


   .. py:attribute:: auto_fallback
      :type:  bool
      :value: True



   .. py:attribute:: subscription_level
      :type:  SubscriptionLevel | None
      :value: None



   .. py:attribute:: endpoint_feeds
      :type:  dict[str, FeedType]


   .. py:method:: get_feed_for_endpoint(endpoint: str) -> FeedType

      Get the configured feed for a specific endpoint.



.. py:class:: FeedManager(config: FeedConfig | None = None)

   Manages data feed selection and fallback logic.


   .. py:attribute:: FEED_SUPPORTED_ENDPOINTS
      :type:  ClassVar[set[str]]


   .. py:attribute:: SUBSCRIPTION_FEEDS
      :type:  ClassVar[dict[SubscriptionLevel, list[FeedType]]]


   .. py:attribute:: config


   .. py:method:: get_feed(endpoint: str, symbol: str | None = None) -> str | None

      Get the appropriate feed for an endpoint.

      :param endpoint: The API endpoint being called
      :param symbol: Optional symbol for endpoint-specific logic

      :returns: Feed parameter value or None if endpoint doesn't support feeds



   .. py:method:: handle_feed_error(endpoint: str, feed: str, error: py_alpaca_api.exceptions.APIRequestError, symbol: str | None = None) -> str | None

      Handle feed-related errors and return alternative feed if available.

      :param endpoint: The API endpoint that failed
      :param feed: The feed that caused the error
      :param error: The API error
      :param symbol: Optional symbol for endpoint-specific tracking

      :returns: Alternative feed to try, or None if no alternatives available



   .. py:method:: detect_subscription_level(api_client: Any) -> SubscriptionLevel

      Detect user's subscription level by testing API access.

      :param api_client: API client instance to test with

      :returns: Detected subscription level



   .. py:method:: validate_feed(endpoint: str, feed: str) -> bool

      Validate if a feed is appropriate for an endpoint.

      :param endpoint: The API endpoint
      :param feed: The feed to validate

      :returns: True if feed is valid for endpoint



   .. py:method:: reset_failures(endpoint: str | None = None) -> None

      Reset tracked feed failures.

      :param endpoint: Optional endpoint to reset. If None, resets all.



   .. py:method:: get_available_feeds() -> list[FeedType]

      Get list of available feeds based on subscription level.

      :returns: List of available feed types
