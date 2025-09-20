py_alpaca_api
=============

.. py:module:: py_alpaca_api


Submodules
----------

.. toctree::
   :maxdepth: 1

   /api/py_alpaca_api/cache/index
   /api/py_alpaca_api/exceptions/index
   /api/py_alpaca_api/stock/index
   /api/py_alpaca_api/trading/index


Exceptions
----------

.. autoapisummary::

   py_alpaca_api.AuthenticationError


Classes
-------

.. autoapisummary::

   py_alpaca_api.Stock
   py_alpaca_api.Trading
   py_alpaca_api.PyAlpacaAPI


Package Contents
----------------

.. py:exception:: AuthenticationError(message: str = 'API Key and Secret are required')

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when API authentication fails.


   .. py:attribute:: message
      :value: 'API Key and Secret are required'



.. py:class:: Stock(api_key: str, api_secret: str, api_paper: bool, market: py_alpaca_api.trading.market.Market)

.. py:class:: Trading(api_key: str, api_secret: str, api_paper: bool)

.. py:class:: PyAlpacaAPI(api_key: str, api_secret: str, api_paper: bool = True)
