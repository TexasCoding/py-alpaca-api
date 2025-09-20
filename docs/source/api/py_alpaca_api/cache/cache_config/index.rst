py_alpaca_api.cache.cache_config
================================

.. py:module:: py_alpaca_api.cache.cache_config

.. autoapi-nested-parse::

   Cache configuration for py-alpaca-api.



Classes
-------

.. autoapisummary::

   py_alpaca_api.cache.cache_config.CacheType
   py_alpaca_api.cache.cache_config.CacheConfig


Module Contents
---------------

.. py:class:: CacheType(*args, **kwds)

   Bases: :py:obj:`enum.Enum`


   Types of cache backends supported.


   .. py:attribute:: MEMORY
      :value: 'memory'



   .. py:attribute:: REDIS
      :value: 'redis'



   .. py:attribute:: DISABLED
      :value: 'disabled'



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
