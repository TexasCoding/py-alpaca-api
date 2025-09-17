import json

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.snapshot_model import SnapshotModel, snapshot_class_from_dict


class Snapshots:
    def __init__(self, headers: dict[str, str]) -> None:
        """Initialize the Snapshots class.

        Args:
            headers: Dictionary containing authentication headers.
        """
        self.headers = headers
        self.base_url = "https://data.alpaca.markets/v2/stocks"

    def get_snapshot(
        self,
        symbol: str,
        feed: str = "iex",
    ) -> SnapshotModel:
        """Get a snapshot of a single stock symbol.

        The snapshot includes the latest trade, latest quote, minute bar,
        daily bar, and previous daily bar data.

        Args:
            symbol: The stock symbol to get snapshot for.
            feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".

        Returns:
            A SnapshotModel containing the snapshot data.

        Raises:
            ValidationError: If symbol is invalid or feed is invalid.
            APIRequestError: If the API request fails.
        """
        if not symbol or not isinstance(symbol, str):
            raise ValidationError("Symbol is required and must be a string.")

        valid_feeds = ["iex", "sip", "otc"]
        if feed not in valid_feeds:
            raise ValidationError(
                f"Invalid feed. Must be one of: {', '.join(valid_feeds)}"
            )

        symbol = symbol.upper().strip()

        url = f"{self.base_url}/{symbol}/snapshot"

        params: dict[str, str | bool | float | int] = {"feed": feed}

        try:
            response = json.loads(
                Requests()
                .request(method="GET", url=url, headers=self.headers, params=params)
                .text
            )
        except Exception as e:
            raise APIRequestError(
                message=f"Failed to get snapshot for {symbol}: {e!s}"
            ) from e

        if not response:
            raise APIRequestError(message=f"No snapshot data returned for {symbol}")

        response["symbol"] = symbol
        return snapshot_class_from_dict(response)

    def get_snapshots(
        self,
        symbols: list[str] | str,
        feed: str = "iex",
    ) -> list[SnapshotModel] | dict[str, SnapshotModel]:
        """Get snapshots for multiple stock symbols.

        The snapshot includes the latest trade, latest quote, minute bar,
        daily bar, and previous daily bar data for each symbol.

        Args:
            symbols: A list of stock symbols or comma-separated string of symbols.
            feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".

        Returns:
            A dictionary mapping symbols to their SnapshotModel objects, or a list
            of SnapshotModel objects if only one symbol is provided.

        Raises:
            ValidationError: If symbols are invalid or feed is invalid.
            APIRequestError: If the API request fails.
        """
        if not symbols:
            raise ValidationError("Symbols are required.")

        valid_feeds = ["iex", "sip", "otc"]
        if feed not in valid_feeds:
            raise ValidationError(
                f"Invalid feed. Must be one of: {', '.join(valid_feeds)}"
            )

        if isinstance(symbols, str):
            symbols_str = symbols.upper().strip()
            symbols_list = [s.strip() for s in symbols_str.split(",")]
        else:
            symbols_list = [s.upper().strip() for s in symbols]
            symbols_str = ",".join(symbols_list)

        if not symbols_str:
            raise ValidationError("At least one symbol is required.")

        url = f"{self.base_url}/snapshots"

        params: dict[str, str | bool | float | int] = {
            "symbols": symbols_str,
            "feed": feed,
        }

        try:
            response = json.loads(
                Requests()
                .request(method="GET", url=url, headers=self.headers, params=params)
                .text
            )
        except Exception as e:
            raise APIRequestError(message=f"Failed to get snapshots: {e!s}") from e

        if not response:
            raise APIRequestError(message="No snapshot data returned")

        # The API returns symbols as top-level keys directly
        snapshots = {}
        for symbol, data in response.items():
            if isinstance(data, dict):  # Ensure it's snapshot data
                data["symbol"] = symbol
                snapshots[symbol] = snapshot_class_from_dict(data)

        if len(symbols_list) == 1:
            return list(snapshots.values())

        return snapshots
