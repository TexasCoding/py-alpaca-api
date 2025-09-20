py_alpaca_api.exceptions
========================

.. py:module:: py_alpaca_api.exceptions

.. autoapi-nested-parse::

   Custom exceptions for the py-alpaca-api library.



Exceptions
----------

.. autoapisummary::

   py_alpaca_api.exceptions.PyAlpacaAPIError
   py_alpaca_api.exceptions.AuthenticationError
   py_alpaca_api.exceptions.APIRequestError
   py_alpaca_api.exceptions.ValidationError
   py_alpaca_api.exceptions.OrderError
   py_alpaca_api.exceptions.PositionError
   py_alpaca_api.exceptions.DataError


Module Contents
---------------

.. py:exception:: PyAlpacaAPIError

   Bases: :py:obj:`Exception`


   Base exception for all py-alpaca-api errors.


.. py:exception:: AuthenticationError(message: str = 'API Key and Secret are required')

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when API authentication fails.


   .. py:attribute:: message
      :value: 'API Key and Secret are required'



.. py:exception:: APIRequestError(status_code: int | None = None, message: str = '')

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when an API request fails.


   .. py:attribute:: status_code
      :value: None



   .. py:attribute:: message
      :value: 'Request Error'



.. py:exception:: ValidationError

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when input validation fails.


.. py:exception:: OrderError

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when order operations fail.


.. py:exception:: PositionError

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when position operations fail.


.. py:exception:: DataError

   Bases: :py:obj:`PyAlpacaAPIError`


   Raised when data processing fails.
