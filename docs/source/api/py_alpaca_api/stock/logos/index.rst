py_alpaca_api.stock.logos
=========================

.. py:module:: py_alpaca_api.stock.logos

.. autoapi-nested-parse::

   Company logos functionality for Alpaca Market Data API.



Classes
-------

.. autoapisummary::

   py_alpaca_api.stock.logos.Logos


Module Contents
---------------

.. py:class:: Logos(headers: dict[str, str])

   Handles company logo retrieval from Alpaca API.


   .. py:attribute:: headers


   .. py:attribute:: base_url
      :value: 'https://data.alpaca.markets/v1beta1/logos'



   .. py:method:: get_logo(symbol: str, placeholder: bool = False) -> bytes

      Get the logo for a specific symbol.

      Retrieves the company logo as binary image data.

      :param symbol: The stock symbol to get the logo for.
      :param placeholder: If True, returns a placeholder image when logo is not available.
                          Defaults to False.

      :returns: The logo image as binary data.
      :rtype: bytes

      :raises ValidationError: If the symbol is invalid.
      :raises Exception: If the API request fails.



   .. py:method:: get_logo_url(symbol: str, placeholder: bool = False) -> str

      Get the URL for a symbol's logo.

      This method returns the direct URL to fetch the logo, which can be used
      in HTML img tags or for direct browser access.

      :param symbol: The stock symbol to get the logo URL for.
      :param placeholder: If True, includes placeholder parameter in URL.
                          Defaults to False.

      :returns: The URL to the logo image.
      :rtype: str

      :raises ValidationError: If the symbol is invalid.



   .. py:method:: save_logo(symbol: str, filepath: str, placeholder: bool = False) -> None

      Save a symbol's logo to a file.

      Downloads the logo and saves it to the specified file path.

      :param symbol: The stock symbol to get the logo for.
      :param filepath: The path where the logo should be saved.
      :param placeholder: If True, saves a placeholder image when logo is not available.
                          Defaults to False.

      :raises ValidationError: If the symbol or filepath is invalid.
      :raises Exception: If the API request fails or file cannot be written.



   .. py:method:: get_logo_base64(symbol: str, placeholder: bool = False) -> str

      Get the logo as a base64 encoded string.

      Useful for embedding logos directly in HTML or JSON responses.

      :param symbol: The stock symbol to get the logo for.
      :param placeholder: If True, returns a placeholder image when logo is not available.
                          Defaults to False.

      :returns: The logo image as a base64 encoded string.
      :rtype: str

      :raises ValidationError: If the symbol is invalid.
      :raises Exception: If the API request fails.



   .. py:method:: get_multiple_logos(symbols: list[str], placeholder: bool = False) -> dict[str, bytes | None]

      Get logos for multiple symbols.

      Retrieves logos for multiple symbols in a single batch operation.

      :param symbols: List of stock symbols to get logos for.
      :param placeholder: If True, returns placeholder images when logos are not available.
                          Defaults to False.

      :returns:

                Dictionary mapping symbols to their logo binary data.
                    Symbols without logos will have None as value unless placeholder is True.
      :rtype: dict

      :raises ValidationError: If symbols list is invalid.
