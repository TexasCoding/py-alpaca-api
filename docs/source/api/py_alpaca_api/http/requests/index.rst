py_alpaca_api.http.requests
===========================

.. py:module:: py_alpaca_api.http.requests


Classes
-------

.. autoapisummary::

   py_alpaca_api.http.requests.Requests


Module Contents
---------------

.. py:class:: Requests

   .. py:attribute:: retry_strategy


   .. py:attribute:: adapter


   .. py:attribute:: session


   .. py:method:: request(method: str, url: str, headers: dict[str, str] | None = None, params: dict[str, str | bool | float | int] | None = None, json: dict[str, Any] | None = None, raw_response: bool = False)

      Execute HTTP request with retry logic.

      :param method: A string representing the HTTP method to be used in the request.
      :param url: A string representing the URL to send the request to.
      :param headers: An optional dictionary containing the headers for the request.
      :param params: An optional dictionary containing the query parameters for the
                     request.
      :param json: An optional dictionary containing the JSON payload for the request.
      :param raw_response: If True, return the raw response object without status checks.
                           Defaults to False.

      :returns: The response object returned by the server.

      :raises APIRequestError: If the response status code is not one of the
          acceptable statuses (200, 204, 207) and raw_response is False.
