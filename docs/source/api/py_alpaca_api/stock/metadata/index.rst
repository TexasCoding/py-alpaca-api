py_alpaca_api.stock.metadata
============================

.. py:module:: py_alpaca_api.stock.metadata


Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.metadata.Metadata


Module Contents
---------------

.. py:class:: Metadata(headers: dict[str, str])

   Market metadata API for condition codes and exchange codes.


   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v2/stocks/meta'



   .. py:method:: get_exchange_codes(use_cache: bool = True) -> dict[str, str]

      Get the mapping between exchange codes and exchange names.

      :param use_cache: Whether to use cached data if available. Defaults to True.

      :returns: Dictionary mapping exchange codes to exchange names.

      :raises APIRequestError: If the API request fails.



   .. py:method:: get_condition_codes(ticktype: str = 'trade', tape: str = 'A', use_cache: bool = True) -> dict[str, str]

      Get the mapping between condition codes and condition names.

      :param ticktype: Type of conditions to retrieve ("trade" or "quote"). Defaults to "trade".
      :param tape: Market tape ("A" for NYSE, "B" for NASDAQ, "C" for other). Defaults to "A".
      :param use_cache: Whether to use cached data if available. Defaults to True.

      :returns: Dictionary mapping condition codes to condition descriptions.

      :raises ValidationError: If invalid parameters are provided.
      :raises APIRequestError: If the API request fails.



   .. py:method:: get_all_condition_codes(use_cache: bool = True) -> dict[str, dict[str, dict[str, str]]]

      Get all condition codes for all tick types and tapes.

      :param use_cache: Whether to use cached data if available. Defaults to True.

      :returns:

                {
                    "trade": {
                        "A": {condition_code: description, ...},
                        "B": {condition_code: description, ...},
                        "C": {condition_code: description, ...}
                    },
                    "quote": {
                        "A": {condition_code: description, ...},
                        "B": {condition_code: description, ...},
                        "C": {condition_code: description, ...}
                    }
                }
      :rtype: Nested dictionary with structure

      :raises APIRequestError: If any API request fails.



   .. py:method:: clear_cache() -> None

      Clear all cached metadata.

      This forces the next request to fetch fresh data from the API.



   .. py:method:: lookup_exchange(code: str) -> str | None

      Look up an exchange name by its code.

      :param code: The exchange code to look up.

      :returns: The exchange name if found, None otherwise.



   .. py:method:: lookup_condition(code: str, ticktype: str = 'trade', tape: str = 'A') -> str | None

      Look up a condition description by its code.

      :param code: The condition code to look up.
      :param ticktype: Type of condition ("trade" or "quote"). Defaults to "trade".
      :param tape: Market tape ("A", "B", or "C"). Defaults to "A".

      :returns: The condition description if found, None otherwise.
