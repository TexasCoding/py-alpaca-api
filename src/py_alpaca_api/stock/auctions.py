"""Historical auctions functionality for Alpaca Market Data API."""

import json
from collections import defaultdict
from datetime import datetime

import pandas as pd

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.http.requests import Requests


class Auctions:
    """Handles historical auction data retrieval from Alpaca API."""

    def __init__(self, headers: dict[str, str]) -> None:
        """Initialize the Auctions class.

        Args:
            headers: Dictionary containing authentication headers.
        """
        self.headers = headers
        self.base_url = "https://data.alpaca.markets/v2/stocks"

    def get_auctions(
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
        """Get historical auction data for one or more symbols.

        Retrieves auction prices (opening and closing auctions) between specified dates.

        Args:
            symbols: Symbol(s) to get auction data for. Can be a string for single symbol
                or list of strings for multiple symbols.
            start: Start date/time in ISO 8601 format (e.g., "2021-01-01" or "2021-01-01T00:00:00Z").
            end: End date/time in ISO 8601 format.
            limit: Maximum number of auctions to return per symbol. Defaults to 10000.
            asof: As-of date for corporate actions adjustments in YYYY-MM-DD format.
            feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".
            page_token: Pagination token from previous request.
            sort: Sort order for results ("asc" or "desc"). Defaults to "asc".

        Returns:
            For single symbol: pd.DataFrame with auction data.
            For multiple symbols: dict mapping symbols to DataFrames with auction data.

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
            url = f"{self.base_url}/{symbols_list[0]}/auctions"
        else:
            url = f"{self.base_url}/auctions"

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
        all_auctions = self._fetch_paginated_auctions(
            url, params, symbols_list, is_single
        )

        # Convert to DataFrames
        result = self._convert_to_dataframes(all_auctions)

        # Return single DataFrame for single symbol, dict for multiple
        if is_single and symbols_list[0] in result:
            return result[symbols_list[0]]
        return result

    def get_daily_auctions(
        self,
        symbols: str | list[str],
        start: str,
        end: str,
        feed: str = "iex",
    ) -> pd.DataFrame | dict[str, pd.DataFrame]:
        """Get daily auction summary for one or more symbols.

        Retrieves opening and closing auction prices aggregated by day.

        Args:
            symbols: Symbol(s) to get auction data for.
            start: Start date in YYYY-MM-DD format.
            end: End date in YYYY-MM-DD format.
            feed: The data feed to use. Defaults to "iex".

        Returns:
            DataFrame or dict of DataFrames with daily auction summaries.
        """
        # Get all auction data
        auctions_data = self.get_auctions(symbols, start, end, feed=feed)

        # Process based on single or multiple symbols
        is_single = isinstance(symbols, str)
        if is_single:
            # auctions_data is a DataFrame for single symbol
            if isinstance(auctions_data, pd.DataFrame):
                return self._aggregate_daily_auctions(auctions_data)
            return pd.DataFrame()  # Return empty if no data

        # auctions_data is a dict for multiple symbols
        result = {}
        if isinstance(auctions_data, dict):
            for symbol, df in auctions_data.items():
                if isinstance(df, pd.DataFrame):
                    result[symbol] = self._aggregate_daily_auctions(df)
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

    def _fetch_paginated_auctions(
        self,
        url: str,
        params: dict,
        symbols_list: list[str],
        is_single: bool,
    ) -> dict[str, list[dict]]:
        """Fetch auction data with pagination support.

        Args:
            url: API endpoint URL.
            params: Request parameters.
            symbols_list: List of symbols being requested.
            is_single: Whether this is a single-symbol request.

        Returns:
            Dictionary mapping symbols to lists of auction dictionaries.

        Raises:
            Exception: If the API request fails or returns no data.
        """
        all_auctions = defaultdict(list)
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
                auctions_data = response.get("auctions", [])
                if auctions_data:
                    all_auctions[symbols_list[0]].extend(auctions_data)
            else:
                # Multi-symbol response has auctions nested under symbol keys
                auctions_data = response.get("auctions", {})
                for symbol, symbol_auctions in auctions_data.items():
                    all_auctions[symbol].extend(symbol_auctions)

            # Check for next page
            page_token = response.get("next_page_token")
            if not page_token:
                break

            # Remove page_token from params if it was there
            params.pop("page_token", None)

        if not all_auctions:
            raise Exception(
                f"No auction data found for symbols: {', '.join(symbols_list)}"
            )

        return all_auctions

    def _convert_to_dataframes(
        self, auctions_data: dict[str, list[dict]]
    ) -> dict[str, pd.DataFrame]:
        """Convert auction data to pandas DataFrames.

        Args:
            auctions_data: Dictionary mapping symbols to lists of auction dictionaries.

        Returns:
            Dictionary mapping symbols to DataFrames with auction data.
        """
        result = {}

        for symbol, auctions in auctions_data.items():
            if auctions:
                df = pd.DataFrame(auctions)

                # Convert timestamp
                if "t" in df.columns:
                    df["t"] = pd.to_datetime(df["t"])
                    df.rename(columns={"t": "timestamp"}, inplace=True)

                # Set timestamp as index
                if "timestamp" in df.columns:
                    df.set_index("timestamp", inplace=True)

                # Rename columns to be more descriptive
                column_mapping = {
                    "d": "date",
                    "o": "opening_auction",
                    "op": "opening_price",
                    "oh": "opening_high",
                    "ol": "opening_low",
                    "ov": "opening_volume",
                    "c": "closing_auction",
                    "cp": "closing_price",
                    "ch": "closing_high",
                    "cl": "closing_low",
                    "cv": "closing_volume",
                    "x": "exchange",
                }
                df.rename(columns=column_mapping, inplace=True)

                # Add derived metrics
                if "opening_price" in df.columns and "closing_price" in df.columns:
                    df["intraday_return"] = (
                        (df["closing_price"] - df["opening_price"])
                        / df["opening_price"]
                        * 100
                    ).round(4)

                result[symbol] = df

        return result

    def _aggregate_daily_auctions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate auction data by day.

        Args:
            df: DataFrame with auction data.

        Returns:
            DataFrame with daily aggregated auction data.
        """
        if df.empty:
            return df

        # Ensure we have a datetime index
        if not isinstance(df.index, pd.DatetimeIndex) and "timestamp" in df.columns:
            df.set_index("timestamp", inplace=True)

        # Group by date - use date property for datetime index
        if isinstance(df.index, pd.DatetimeIndex):
            # Group by date (removing time component)
            daily = df.groupby(pd.Grouper(freq="D")).agg(
                {
                    col: "first" if "opening" in col else "last"
                    for col in df.columns
                    if col in ["opening_price", "closing_price"]
                }
            )

            # Remove empty rows
            daily = daily.dropna(how="all")

            # Calculate daily metrics
            if "opening_price" in daily.columns and "closing_price" in daily.columns:
                daily["daily_return"] = (
                    (daily["closing_price"] - daily["opening_price"])
                    / daily["opening_price"]
                    * 100
                ).round(4)

            # Ensure we return a DataFrame
            assert isinstance(daily, pd.DataFrame)
            return daily

        return df
