import json

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.http.requests import Requests


class Metadata:
    """Market metadata API for condition codes and exchange codes."""

    def __init__(self, headers: dict[str, str]) -> None:
        """Initialize the Metadata class.

        Args:
            headers: Dictionary containing authentication headers.
        """
        self.headers = headers
        self.base_url = "https://data.alpaca.markets/v2/stocks/meta"
        # Cache for metadata that rarely changes
        self._exchange_cache: dict[str, str] | None = None
        self._condition_cache: dict[str, dict[str, str]] = {}

    def get_exchange_codes(self, use_cache: bool = True) -> dict[str, str]:
        """Get the mapping between exchange codes and exchange names.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            Dictionary mapping exchange codes to exchange names.

        Raises:
            APIRequestError: If the API request fails.
        """
        if use_cache and self._exchange_cache is not None:
            return self._exchange_cache

        url = f"{self.base_url}/exchanges"

        try:
            response = json.loads(
                Requests().request(method="GET", url=url, headers=self.headers).text
            )
        except Exception as e:
            raise APIRequestError(message=f"Failed to get exchange codes: {e!s}") from e

        if not response:
            raise APIRequestError(message="No exchange data returned")

        # Cache the result
        self._exchange_cache = response
        return response

    def get_condition_codes(
        self,
        ticktype: str = "trade",
        tape: str = "A",
        use_cache: bool = True,
    ) -> dict[str, str]:
        """Get the mapping between condition codes and condition names.

        Args:
            ticktype: Type of conditions to retrieve ("trade" or "quote"). Defaults to "trade".
            tape: Market tape ("A" for NYSE, "B" for NASDAQ, "C" for other). Defaults to "A".
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            Dictionary mapping condition codes to condition descriptions.

        Raises:
            ValidationError: If invalid parameters are provided.
            APIRequestError: If the API request fails.
        """
        # Validate parameters
        valid_ticktypes = ["trade", "quote"]
        if ticktype not in valid_ticktypes:
            raise ValidationError(
                f"Invalid ticktype. Must be one of: {', '.join(valid_ticktypes)}"
            )

        valid_tapes = ["A", "B", "C"]
        if tape not in valid_tapes:
            raise ValidationError(
                f"Invalid tape. Must be one of: {', '.join(valid_tapes)}"
            )

        # Check cache
        cache_key = f"{ticktype}_{tape}"
        if use_cache and cache_key in self._condition_cache:
            return self._condition_cache[cache_key]

        url = f"{self.base_url}/conditions/{ticktype}"
        params: dict[str, str | bool | float | int] = {"tape": tape}

        try:
            response = json.loads(
                Requests()
                .request(method="GET", url=url, headers=self.headers, params=params)
                .text
            )
        except Exception as e:
            raise APIRequestError(
                message=f"Failed to get condition codes: {e!s}"
            ) from e

        if response is None:
            raise APIRequestError(message="No condition data returned")

        # Cache the result
        self._condition_cache[cache_key] = response
        return response

    def get_all_condition_codes(
        self, use_cache: bool = True
    ) -> dict[str, dict[str, dict[str, str]]]:
        """Get all condition codes for all tick types and tapes.

        Args:
            use_cache: Whether to use cached data if available. Defaults to True.

        Returns:
            Nested dictionary with structure:
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

        Raises:
            APIRequestError: If any API request fails.
        """
        result: dict[str, dict[str, dict[str, str]]] = {}

        for ticktype in ["trade", "quote"]:
            result[ticktype] = {}
            for tape in ["A", "B", "C"]:
                try:
                    result[ticktype][tape] = self.get_condition_codes(
                        ticktype=ticktype, tape=tape, use_cache=use_cache
                    )
                except APIRequestError:
                    # Some tape/ticktype combinations might not be available
                    result[ticktype][tape] = {}

        return result

    def clear_cache(self) -> None:
        """Clear all cached metadata.

        This forces the next request to fetch fresh data from the API.
        """
        self._exchange_cache = None
        self._condition_cache = {}

    def lookup_exchange(self, code: str) -> str | None:
        """Look up an exchange name by its code.

        Args:
            code: The exchange code to look up.

        Returns:
            The exchange name if found, None otherwise.
        """
        exchanges = self.get_exchange_codes()
        return exchanges.get(code)

    def lookup_condition(
        self, code: str, ticktype: str = "trade", tape: str = "A"
    ) -> str | None:
        """Look up a condition description by its code.

        Args:
            code: The condition code to look up.
            ticktype: Type of condition ("trade" or "quote"). Defaults to "trade".
            tape: Market tape ("A", "B", or "C"). Defaults to "A".

        Returns:
            The condition description if found, None otherwise.
        """
        conditions = self.get_condition_codes(ticktype=ticktype, tape=tape)
        return conditions.get(code)
