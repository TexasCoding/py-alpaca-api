"""Historical quotes functionality for Alpaca Market Data API."""

import json
from collections import defaultdict
from datetime import datetime

import pandas as pd

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.http.requests import Requests


class Quotes:
    """Handles historical quote data retrieval from Alpaca API."""

    def __init__(self, headers: dict[str, str]) -> None:
        """Initialize the Quotes class.

        Args:
            headers: Dictionary containing authentication headers.
        """
        self.headers = headers
        self.base_url = "https://data.alpaca.markets/v2/stocks"

    def get_historical_quotes(
        self,
        symbols: str | list[str],
        start: str,
        end: str,
        limit: int = 10000,
        asof: str | None = None,
        feed: str = "iex",
        page_token: str | None = None,
        sort: str = "asc",
    ) -> pd.DataFrame | dict[str, pd.DataFrame]:
        """Get historical quote data for one or more symbols.

        Retrieves historical quote (bid/ask) data between specified dates.

        Args:
            symbols: Symbol(s) to get quote data for. Can be a string for single symbol
                or list of strings for multiple symbols.
            start: Start date/time in ISO 8601 format (e.g., "2021-01-01" or "2021-01-01T00:00:00Z").
            end: End date/time in ISO 8601 format.
            limit: Maximum number of quotes to return per symbol. Defaults to 10000.
            asof: As-of date for corporate actions adjustments in YYYY-MM-DD format.
            feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".
            page_token: Pagination token from previous request.
            sort: Sort order for results ("asc" or "desc"). Defaults to "asc".

        Returns:
            For single symbol: pd.DataFrame with quote data.
            For multiple symbols: dict mapping symbols to DataFrames with quote data.

        Raises:
            ValidationError: If parameters are invalid.
            Exception: If the API request fails or returns no data.
        """
        # Validate parameters
        self._validate_parameters(symbols, start, end, limit, feed, sort)

        # Normalize symbols to list
        is_single = isinstance(symbols, str)
        symbols_list: list[str]
        if is_single:
            assert isinstance(symbols, str)  # Type narrowing for mypy
            symbols_list = [symbols.upper()]
        else:
            assert isinstance(symbols, list)  # Type narrowing for mypy
            symbols_list = [s.upper() for s in symbols]

        # Determine endpoint URL
        if is_single:
            url = f"{self.base_url}/{symbols_list[0]}/quotes"
        else:
            url = f"{self.base_url}/quotes"

        # Build parameters
        params: dict[str, str | int] = {
            "start": start,
            "end": end,
            "limit": limit,
            "feed": feed,
            "sort": sort,
        }

        # Add optional parameters
        if asof:
            params["asof"] = asof
        if page_token:
            params["page_token"] = page_token
        if not is_single:
            params["symbols"] = ",".join(symbols_list)

        # Fetch all data with pagination
        all_quotes = self._fetch_paginated_quotes(url, params, symbols_list, is_single)

        # Convert to DataFrames
        result = self._convert_to_dataframes(all_quotes)

        # Return single DataFrame for single symbol, dict for multiple
        if is_single and symbols_list[0] in result:
            return result[symbols_list[0]]
        return result

    def _validate_parameters(
        self,
        symbols: str | list[str],
        start: str,
        end: str,
        limit: int,
        feed: str,
        sort: str,
    ) -> None:
        """Validate input parameters.

        Args:
            symbols: Symbol(s) to validate.
            start: Start date/time to validate.
            end: End date/time to validate.
            limit: Limit to validate.
            feed: Feed to validate.
            sort: Sort order to validate.

        Raises:
            ValidationError: If any parameter is invalid.
        """
        if not symbols:
            raise ValidationError("At least one symbol is required")

        valid_feeds = ["iex", "sip", "otc"]
        if feed not in valid_feeds:
            raise ValidationError(
                f"Invalid feed. Must be one of: {', '.join(valid_feeds)}"
            )

        valid_sorts = ["asc", "desc"]
        if sort not in valid_sorts:
            raise ValidationError(
                f"Invalid sort. Must be one of: {', '.join(valid_sorts)}"
            )

        if limit < 1:
            raise ValidationError("Limit must be at least 1")

        # Validate date format
        try:
            datetime.fromisoformat(start.replace("Z", "+00:00"))
            datetime.fromisoformat(end.replace("Z", "+00:00"))
        except ValueError as e:
            raise ValidationError(f"Invalid date format: {e}") from e

    def _fetch_paginated_quotes(
        self,
        url: str,
        params: dict,
        symbols_list: list[str],
        is_single: bool,
    ) -> dict[str, list[dict]]:
        """Fetch quotes data with pagination support.

        Args:
            url: API endpoint URL.
            params: Request parameters.
            symbols_list: List of symbols being requested.
            is_single: Whether this is a single-symbol request.

        Returns:
            Dictionary mapping symbols to lists of quote dictionaries.

        Raises:
            Exception: If the API request fails or returns no data.
        """
        all_quotes = defaultdict(list)
        page_token = params.get("page_token")

        while True:
            if page_token:
                params["page_token"] = page_token

            response = json.loads(
                Requests()
                .request(method="GET", url=url, headers=self.headers, params=params)
                .text
            )

            # Handle single vs multi-symbol response format
            if is_single:
                quotes_data = response.get("quotes", [])
                if quotes_data:
                    all_quotes[symbols_list[0]].extend(quotes_data)
            else:
                # Multi-symbol response has quotes nested under symbol keys
                quotes_data = response.get("quotes", {})
                for symbol, symbol_quotes in quotes_data.items():
                    all_quotes[symbol].extend(symbol_quotes)

            # Check for next page
            page_token = response.get("next_page_token")
            if not page_token:
                break

            # Remove page_token from params if it was there
            params.pop("page_token", None)

        if not all_quotes:
            raise Exception(
                f"No quote data found for symbols: {', '.join(symbols_list)}"
            )

        return all_quotes

    def _convert_to_dataframes(
        self, quotes_data: dict[str, list[dict]]
    ) -> dict[str, pd.DataFrame]:
        """Convert quote data to pandas DataFrames.

        Args:
            quotes_data: Dictionary mapping symbols to lists of quote dictionaries.

        Returns:
            Dictionary mapping symbols to DataFrames with quote data.
        """
        result = {}

        for symbol, quotes in quotes_data.items():
            if quotes:
                df = pd.DataFrame(quotes)

                # Convert timestamp
                if "t" in df.columns:
                    df["t"] = pd.to_datetime(df["t"])
                    df.rename(columns={"t": "timestamp"}, inplace=True)

                # Set timestamp as index
                if "timestamp" in df.columns:
                    df.set_index("timestamp", inplace=True)

                # Rename columns to be more descriptive
                column_mapping = {
                    "ax": "ask_exchange",
                    "ap": "ask_price",
                    "as": "ask_size",
                    "bx": "bid_exchange",
                    "bp": "bid_price",
                    "bs": "bid_size",
                    "c": "conditions",
                    "z": "tape",
                }
                df.rename(columns=column_mapping, inplace=True)

                # Calculate spread
                if "ask_price" in df.columns and "bid_price" in df.columns:
                    df["spread"] = df["ask_price"] - df["bid_price"]
                    df["spread_pct"] = (df["spread"] / df["bid_price"] * 100).round(4)

                result[symbol] = df

        return result
