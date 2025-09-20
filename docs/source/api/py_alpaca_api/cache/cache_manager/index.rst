py_alpaca_api.cache.cache_manager
=================================

.. py:module:: py_alpaca_api.cache.cache_manager

.. autoapi-nested-parse::

   Cache manager for py-alpaca-api.



Attributes
----------

.. autoapisummary::

   py_alpaca_api.cache.cache_manager.logger


Classes
-------

.. autoapisummary::

   py_alpaca_api.cache.cache_manager.LRUCache
   py_alpaca_api.cache.cache_manager.RedisCache
   py_alpaca_api.cache.cache_manager.CacheManager


Module Contents
---------------

.. py:data:: logger

.. py:class:: LRUCache(max_size: int = 1000)

   Least Recently Used (LRU) cache implementation.


   .. py:attribute:: max_size
      :value: 1000



   .. py:attribute:: cache
      :type:  collections.OrderedDict[str, tuple[Any, float]]


   .. py:method:: get(key: str) -> Any | None

      Get item from cache.

      :param key: Cache key

      :returns: Cached value or None if not found/expired



   .. py:method:: set(key: str, value: Any, ttl: int) -> None

      Set item in cache.

      :param key: Cache key
      :param value: Value to cache
      :param ttl: Time-to-live in seconds



   .. py:method:: delete(key: str) -> bool

      Delete item from cache.

      :param key: Cache key

      :returns: True if deleted, False if not found



   .. py:method:: clear() -> None

      Clear all items from cache.



   .. py:method:: size() -> int

      Get current cache size.

      :returns: Number of items in cache



   .. py:method:: cleanup_expired() -> int

      Remove expired items from cache.

      :returns: Number of items removed



.. py:class:: RedisCache(config: py_alpaca_api.cache.cache_config.CacheConfig)

   Redis cache implementation.


   .. py:attribute:: config


   .. py:method:: get(key: str) -> Any | None

      Get item from cache.

      :param key: Cache key

      :returns: Cached value or None if not found



   .. py:method:: set(key: str, value: Any, ttl: int) -> None

      Set item in cache.

      :param key: Cache key
      :param value: Value to cache
      :param ttl: Time-to-live in seconds



   .. py:method:: delete(key: str) -> bool

      Delete item from cache.

      :param key: Cache key

      :returns: True if deleted, False if not found



   .. py:method:: clear() -> None

      Clear all items from cache.



   .. py:method:: size() -> int

      Get current cache size.

      :returns: Number of items in cache



.. py:class:: CacheManager(config: py_alpaca_api.cache.cache_config.CacheConfig | None = None)

   Manages caching for py-alpaca-api.


   .. py:attribute:: config


   .. py:method:: generate_key(prefix: str, **kwargs) -> str

      Generate cache key from prefix and parameters.

      :param prefix: Key prefix (e.g., "bars", "quotes")
      :param \*\*kwargs: Parameters to include in key

      :returns: Cache key



   .. py:method:: get(key: str, data_type: str | None = None) -> Any | None

      Get item from cache.

      :param key: Cache key
      :param data_type: Optional data type for metrics

      :returns: Cached value or None if not found



   .. py:method:: set(key: str, value: Any, data_type: str, ttl: int | None = None) -> None

      Set item in cache.

      :param key: Cache key
      :param value: Value to cache
      :param data_type: Type of data (for TTL lookup)
      :param ttl: Optional TTL override in seconds



   .. py:method:: delete(key: str) -> bool

      Delete item from cache.

      :param key: Cache key

      :returns: True if deleted, False if not found



   .. py:method:: clear(prefix: str | None = None) -> int

      Clear cache items.

      :param prefix: Optional prefix to clear only specific items

      :returns: Number of items cleared



   .. py:method:: invalidate_pattern(pattern: str) -> int

      Invalidate cache items matching a pattern.

      :param pattern: Pattern to match (e.g., "bars:*AAPL*")

      :returns: Number of items invalidated



   .. py:method:: get_stats() -> dict[str, Any]

      Get cache statistics.

      :returns: Dictionary with cache stats



   .. py:method:: reset_stats() -> None

      Reset cache statistics.



   .. py:method:: cached(data_type: str, ttl: int | None = None) -> collections.abc.Callable

      Decorator for caching function results.

      :param data_type: Type of data being cached
      :param ttl: Optional TTL override

      :returns: Decorator function
