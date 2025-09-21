"""Company logos functionality for Alpaca Market Data API."""

import base64
from pathlib import Path
from typing import NoReturn

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.http.requests import Requests


class Logos:
    """Handles company logo retrieval from Alpaca API."""

    def __init__(self, headers: dict[str, str]) -> None:
        """Initialize the Logos class.

        Args:
            headers: Dictionary containing authentication headers.
        """
        self.headers = headers
        self.base_url = "https://data.alpaca.markets/v1beta1/logos"

    def get_logo(
        self,
        symbol: str,
        placeholder: bool = False,
    ) -> bytes:
        """Get the logo for a specific symbol.

        Retrieves the company logo as binary image data.

        Args:
            symbol: The stock symbol to get the logo for.
            placeholder: If True, returns a placeholder image when logo is not available.
                Defaults to False.

        Returns:
            bytes: The logo image as binary data.

        Raises:
            ValidationError: If the symbol is invalid.
            Exception: If the API request fails.
        """
        # Validate symbol
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string")

        symbol = symbol.upper()

        # Build URL
        url = f"{self.base_url}/{symbol}"

        # Build parameters
        params: dict[str, str | bool | float | int] = {}
        if placeholder:
            params["placeholder"] = "true"

        try:
            # Make request - expecting binary response
            response = Requests().request(
                method="GET",
                url=url,
                headers=self.headers,
                params=params if params else None,
                raw_response=True,  # Return raw response for binary data
            )

            # Check if we got a valid response
            if response.status_code == 404:
                self._raise_logo_error(f"Logo not found for symbol: {symbol}")
            elif response.status_code != 200:
                self._raise_logo_error(
                    f"Failed to retrieve logo: {response.status_code} - {response.text}"
                )
            else:
                return response.content

        except Exception as e:
            raise Exception(f"Failed to retrieve logo for {symbol}: {e!s}") from e

    def get_logo_url(
        self,
        symbol: str,
        placeholder: bool = False,
    ) -> str:
        """Get the URL for a symbol's logo.

        This method returns the direct URL to fetch the logo, which can be used
        in HTML img tags or for direct browser access.

        Args:
            symbol: The stock symbol to get the logo URL for.
            placeholder: If True, includes placeholder parameter in URL.
                Defaults to False.

        Returns:
            str: The URL to the logo image.

        Raises:
            ValidationError: If the symbol is invalid.
        """
        # Validate symbol
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol must be a non-empty string")

        symbol = symbol.upper()

        # Build URL
        url = f"{self.base_url}/{symbol}"

        # Add placeholder parameter if requested
        if placeholder:
            url += "?placeholder=true"

        return url

    def save_logo(
        self,
        symbol: str,
        filepath: str,
        placeholder: bool = False,
    ) -> None:
        """Save a symbol's logo to a file.

        Downloads the logo and saves it to the specified file path.

        Args:
            symbol: The stock symbol to get the logo for.
            filepath: The path where the logo should be saved.
            placeholder: If True, saves a placeholder image when logo is not available.
                Defaults to False.

        Raises:
            ValidationError: If the symbol or filepath is invalid.
            Exception: If the API request fails or file cannot be written.
        """
        if not filepath or not isinstance(filepath, str):
            raise ValidationError("Filepath must be a non-empty string")

        # Get the logo data
        logo_data = self.get_logo(symbol, placeholder=placeholder)

        # Save to file
        try:
            path = Path(filepath)
            with path.open("wb") as f:
                f.write(logo_data)
        except Exception as e:
            raise Exception(f"Failed to save logo to {filepath}: {e!s}") from e

    def get_logo_base64(
        self,
        symbol: str,
        placeholder: bool = False,
    ) -> str:
        """Get the logo as a base64 encoded string.

        Useful for embedding logos directly in HTML or JSON responses.

        Args:
            symbol: The stock symbol to get the logo for.
            placeholder: If True, returns a placeholder image when logo is not available.
                Defaults to False.

        Returns:
            str: The logo image as a base64 encoded string.

        Raises:
            ValidationError: If the symbol is invalid.
            Exception: If the API request fails.
        """
        # Get the logo data
        logo_data = self.get_logo(symbol, placeholder=placeholder)

        # Convert to base64
        return base64.b64encode(logo_data).decode("utf-8")

    def get_multiple_logos(
        self,
        symbols: list[str],
        placeholder: bool = False,
    ) -> dict[str, bytes | None]:
        """Get logos for multiple symbols.

        Retrieves logos for multiple symbols in a single batch operation.

        Args:
            symbols: List of stock symbols to get logos for.
            placeholder: If True, returns placeholder images when logos are not available.
                Defaults to False.

        Returns:
            dict: Dictionary mapping symbols to their logo binary data.
                Symbols without logos will have None as value unless placeholder is True.

        Raises:
            ValidationError: If symbols list is invalid.
        """
        if not symbols or not isinstance(symbols, list):
            raise ValidationError("Symbols must be a non-empty list")

        if len(symbols) == 0:
            raise ValidationError("At least one symbol is required")

        logos: dict[str, bytes | None] = {}
        for symbol in symbols:
            try:
                logos[symbol.upper()] = self.get_logo(symbol, placeholder=placeholder)
            except Exception:
                # If logo not found and no placeholder requested, set to None
                if not placeholder:
                    logos[symbol.upper()] = None
                else:
                    logos[symbol.upper()] = self.get_logo(symbol, placeholder=True)

        return logos

    def _raise_logo_error(self, message: str) -> NoReturn:
        """Raise an exception with the given message.

        Args:
            message: The error message.

        Raises:
            Exception: Always raises with the provided message.
        """
        raise Exception(message)
