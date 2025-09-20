py_alpaca_api.cache
===================

.. py:module:: py_alpaca_api.cache

.. autoapi-nested-parse::

   Cache module for py-alpaca-api.

   This module provides caching functionality to improve performance and reduce API calls.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /api/py_alpaca_api/cache/cache_config/index
   /api/py_alpaca_api/cache/cache_manager/index


Classes
-------

.. autoapisummary::

   py_alpaca_api.cache.CacheConfig
   py_alpaca_api.cache.CacheType
   py_alpaca_api.cache.CacheManager


Package Contents
----------------

.. py:class:: CacheConfig

   Configuration for cache system.

   .. attribute:: cache_type

      Type of cache backend to use

   .. attribute:: max_size

      Maximum number of items in memory cache

   .. attribute:: default_ttl

      Default time-to-live in seconds

   .. attribute:: data_ttls

      TTL overrides per data type

   .. attribute:: redis_host

      Redis host (if using Redis)

   .. attribute:: redis_port

      Redis port (if using Redis)

   .. attribute:: redis_db

      Redis database number (if using Redis)

   .. attribute:: redis_password

      Redis password (if using Redis)

   .. attribute:: enabled

      Whether caching is enabled


   .. py:attribute:: cache_type
      :type:  CacheType


   .. py:attribute:: max_size
      :type:  int
      :value: 1000



   .. py:attribute:: default_ttl
      :type:  int
      :value: 300



   .. py:attribute:: data_ttls
      :type:  dict[str, int]


   .. py:attribute:: redis_host
      :type:  str
      :value: 'localhost'



   .. py:attribute:: redis_port
      :type:  int
      :value: 6379



   .. py:attribute:: redis_db
      :type:  int
      :value: 0



   .. py:attribute:: redis_password
      :type:  str | None
      :value: None



   .. py:attribute:: enabled
      :type:  bool
      :value: True



   .. py:method:: get_ttl(data_type: str) -> int

      Get TTL for a specific data type.

      :param data_type: Type of data to get TTL for

      :returns: TTL in seconds



.. py:class:: CacheType(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Types of cache backends supported.


   .. py:attribute:: MEMORY
      :value: 'memory'



   .. py:attribute:: REDIS
      :value: 'redis'



   .. py:attribute:: DISABLED
      :value: 'disabled'



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
