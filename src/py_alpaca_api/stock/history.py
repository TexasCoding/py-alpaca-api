import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.asset_model import AssetModel
from py_alpaca_api.stock.assets import Assets


class History:
    BATCH_SIZE = 200  # Alpaca API limit for multi-symbol requests

    def __init__(self, data_url: str, headers: dict[str, str], asset: Assets) -> None:
        """Initializes an instance of the History class.

        Args:
            data_url: A string representing the URL of the data.
            headers: A dictionary containing the headers to be included in the request.
            asset: An instance of the Asset class representing the asset.
        """
        self.data_url = data_url
        self.headers = headers
        self.asset = asset

    ###########################################
    # /////// Check if Asset is Stock \\\\\\\ #
    ###########################################
    def check_if_stock(self, symbol: str) -> AssetModel:
        """Check if the asset corresponding to the symbol is a stock.

        Args:
            symbol (str): The symbol of the asset to be checked.

        Returns:
            AssetModel: The asset information for the given symbol.

        Raises:
            ValueError: If there is an error getting the asset information or if the asset is not a stock.
        """
        try:
            asset = self.asset.get(symbol)
        except Exception as e:
            raise ValueError(str(e)) from e

        if asset.asset_class != "us_equity":
            raise ValueError(f"{symbol} is not a stock.")

        return asset

    ###########################################
    # ////// Get Stock Historical Data \\\\\\ #
    ###########################################
    def get_stock_data(
        self,
        symbol: str | list[str],
        start: str,
        end: str,
        timeframe: str = "1d",
        feed: str = "sip",
        currency: str = "USD",
        limit: int = 1000,
        sort: str = "asc",
        adjustment: str = "raw",
    ) -> pd.DataFrame:
        """Retrieves historical stock data for one or more symbols within a specified date range and timeframe.

        Args:
            symbol: The stock symbol(s) to fetch data for. Can be a single symbol string or list of symbols.
            start: The start date for historical data in the format "YYYY-MM-DD".
            end: The end date for historical data in the format "YYYY-MM-DD".
            timeframe: The timeframe for the historical data. Default is "1d".
            feed: The data feed source. Default is "sip".
            currency: The currency for historical data. Default is "USD".
            limit: The number of data points to fetch per symbol. Default is 1000.
            sort: The sort order for the data. Default is "asc".
            adjustment: The adjustment for historical data. Default is "raw".

        Returns:
            A pandas DataFrame containing the historical stock data for the given symbol(s) and time range.

        Raises:
            ValueError: If the given timeframe is not one of the allowed values.
        """
        # Handle single symbol or list of symbols
        is_single = isinstance(symbol, str)
        if is_single:
            assert isinstance(symbol, str)  # Type guard for mypy
            symbols_list: list[str] = [symbol]
            single_symbol: str = symbol
        else:
            assert isinstance(symbol, list)  # Type guard for mypy
            symbols_list = symbol
            single_symbol = ""  # Won't be used in multi-symbol case

        # Validate symbols are stocks
        for sym in symbols_list:
            self.check_if_stock(sym)

        # If more than BATCH_SIZE symbols, need to batch the requests
        if not is_single and len(symbols_list) > self.BATCH_SIZE:
            return self._get_batched_stock_data(
                symbols_list,
                start,
                end,
                timeframe,
                feed,
                currency,
                limit,
                sort,
                adjustment,
            )

        # Determine if using single or multi-symbol endpoint
        if is_single:
            url = f"{self.data_url}/stocks/{single_symbol}/bars"
        else:
            url = f"{self.data_url}/stocks/bars"

        timeframe_mapping: dict = {
            "1m": "1Min",
            "5m": "5Min",
            "15m": "15Min",
            "30m": "30Min",
            "1h": "1Hour",
            "4h": "4Hour",
            "1d": "1Day",
            "1w": "1Week",
            "1M": "1Month",
        }

        if timeframe not in timeframe_mapping:
            raise ValueError(
                'Invalid timeframe. Must be "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", or "1M"'
            )

        params: dict = {
            "timeframe": timeframe_mapping[timeframe],
            "start": start,
            "end": end,
            "currency": currency,
            "limit": limit,
            "adjustment": adjustment,
            "feed": feed,
            "sort": sort,
        }

        # Add symbols parameter for multi-symbol request
        if not is_single:
            params["symbols"] = ",".join(symbols_list)

        symbol_data = self.get_historical_data(symbols_list, url, params, is_single)

        # Process data based on single or multi-symbol
        if is_single:
            return self.preprocess_data(symbol_data[single_symbol], single_symbol)
        return self.preprocess_multi_data(symbol_data)

    def _get_batched_stock_data(
        self,
        symbols: list[str],
        start: str,
        end: str,
        timeframe: str,
        feed: str,
        currency: str,
        limit: int,
        sort: str,
        adjustment: str,
    ) -> pd.DataFrame:
        """Handle large symbol lists by batching requests.

        Args:
            symbols: List of symbols to fetch data for.
            start: The start date for historical data.
            end: The end date for historical data.
            timeframe: The timeframe for the historical data.
            feed: The data feed source.
            currency: The currency for historical data.
            limit: The number of data points to fetch per symbol.
            sort: The sort order for the data.
            adjustment: The adjustment for historical data.

        Returns:
            A pandas DataFrame containing the historical stock data for all symbols.
        """
        # Split symbols into batches
        batches = [
            symbols[i : i + self.BATCH_SIZE]
            for i in range(0, len(symbols), self.BATCH_SIZE)
        ]

        # Use ThreadPoolExecutor for concurrent batch requests
        all_dfs = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for batch in batches:
                future = executor.submit(
                    self.get_stock_data,
                    batch,
                    start,
                    end,
                    timeframe,
                    feed,
                    currency,
                    limit,
                    sort,
                    adjustment,
                )
                futures.append(future)

            for future in as_completed(futures):
                try:
                    df = future.result()
                    if not df.empty:
                        all_dfs.append(df)
                except Exception as e:
                    # Log error but continue with other batches
                    print(f"Error fetching batch: {e}")

        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True).sort_values(["symbol", "date"])
        return pd.DataFrame()

    @staticmethod
    def preprocess_multi_data(
        symbols_data: dict[str, list[defaultdict]],
    ) -> pd.DataFrame:
        """Preprocess data for multiple symbols.

        Args:
            symbols_data: A dictionary mapping symbols to their bar data.

        Returns:
            A pandas DataFrame containing the preprocessed historical stock data for all symbols.
        """
        all_dfs = []
        for symbol, data in symbols_data.items():
            if data:  # Only process if data exists
                df = History.preprocess_data(data, symbol)
                all_dfs.append(df)

        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True).sort_values(["symbol", "date"])
        return pd.DataFrame()

    ###########################################
    # /////////// PreProcess Data \\\\\\\\\\\ #
    ###########################################
    @staticmethod
    def preprocess_data(symbol_data: list[defaultdict], symbol: str) -> pd.DataFrame:
        """Prepross data
        Preprocesses the given symbol data by converting it to a pandas DataFrame and performing various
        data transformations.

        Args:
            symbol_data: A list of defaultdict objects representing the JSON response data.
            symbol: A string representing the symbol or ticker for the stock data.

        Returns:
            A pandas DataFrame containing the preprocessed historical stock data.
        """
        bar_data_df = pd.DataFrame(symbol_data)

        bar_data_df.insert(0, "symbol", symbol)
        bar_data_df["t"] = pd.to_datetime(
            bar_data_df["t"].replace("[A-Za-z]", " ", regex=True)
        )

        bar_data_df.rename(
            columns={
                "t": "date",
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "v": "volume",
                "n": "trade_count",
                "vw": "vwap",
            },
            inplace=True,
        )

        return bar_data_df.astype(
            {
                "open": "float",
                "high": "float",
                "low": "float",
                "close": "float",
                "symbol": "str",
                "date": "datetime64[ns]",
                "vwap": "float",
                "trade_count": "int",
                "volume": "int",
            }
        )

    ###########################################
    # ///////// Get Historical Data \\\\\\\\\ #
    ###########################################
    def get_historical_data(
        self, symbols: list[str], url: str, params: dict, is_single: bool
    ) -> dict[str, list[defaultdict]]:
        """Retrieves historical data for given symbol(s).

        Args:
            symbols: List of symbols for which to retrieve historical data.
            url: The URL to send the request to.
            params: Additional parameters to include in the request.
            is_single: Whether this is a single-symbol request.

        Returns:
            dict[str, list[defaultdict]]: A dictionary mapping symbols to their historical data.
        """
        page_token: str | None = None
        symbols_data = defaultdict(list)

        while True:
            if page_token is not None:
                params["page_token"] = page_token

            response = json.loads(
                Requests()
                .request(method="GET", url=url, headers=self.headers, params=params)
                .text
            )

            # Handle single vs multi-symbol response format
            if is_single:
                if not response.get("bars"):
                    raise Exception(
                        f"No historical data found for {symbols[0]}, with the given parameters."
                    )
                symbols_data[symbols[0]].extend(response.get("bars", []))
            else:
                # Multi-symbol response has bars nested under symbol keys
                bars = response.get("bars", {})
                if not bars:
                    raise Exception(
                        f"No historical data found for symbols: {', '.join(symbols)}, with the given parameters."
                    )
                for symbol, symbol_bars in bars.items():
                    symbols_data[symbol].extend(symbol_bars)

            page_token = response.get("next_page_token")
            if not page_token:
                break

        return symbols_data

    ###########################################
    # ///////// Get Latest Bars \\\\\\\\\ #
    ###########################################
    def get_latest_bars(
        self,
        symbols: str | list[str],
        feed: str = "iex",
        currency: str = "USD",
    ) -> pd.DataFrame | dict[str, pd.DataFrame]:
        """Get the latest bars for one or more symbols.

        The latest bars endpoint returns the most recent minute bar for each requested symbol.

        Args:
            symbols: Symbol(s) to get latest bars for. Can be a string for single symbol
                or list of strings for multiple symbols.
            feed: The data feed to use ("iex", "sip", or "otc"). Defaults to "iex".
            currency: The currency for the returned prices. Defaults to "USD".

        Returns:
            For single symbol: pd.DataFrame with the latest bar data.
            For multiple symbols: dict mapping symbols to DataFrames with latest bar data.

        Raises:
            ValueError: If feed is invalid or symbols is empty.
            Exception: If the API request fails or returns no data.
        """
        # Validate feed
        valid_feeds = ["iex", "sip", "otc"]
        if feed not in valid_feeds:
            raise ValueError(f"Invalid feed. Must be one of: {', '.join(valid_feeds)}")

        # Normalize symbols to list
        is_single = isinstance(symbols, str)
        symbols_list: list[str]
        if is_single:
            assert isinstance(symbols, str)  # Type narrowing for mypy
            symbols_list = [symbols.upper()]
        else:
            assert isinstance(symbols, list)  # Type narrowing for mypy
            symbols_list = [s.upper() for s in symbols]

        if not symbols_list:
            raise ValueError("At least one symbol is required")

        # Check if all symbols are valid stocks
        for symbol in symbols_list:
            self.check_if_stock(symbol)

        # Build URL
        url = f"{self.data_url}/stocks/bars/latest"

        # Build parameters
        params: dict = {
            "symbols": ",".join(symbols_list),
            "feed": feed,
            "currency": currency,
        }

        # Make request
        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        # Process response
        bars_data = response.get("bars", {})
        if not bars_data:
            raise Exception(
                f"No latest bar data found for symbols: {', '.join(symbols_list)}"
            )

        # Convert to DataFrames
        result = {}
        for symbol, bar_data in bars_data.items():
            if bar_data:
                # Convert single bar to list for DataFrame
                df = pd.DataFrame([bar_data])
                # Convert timestamp
                if "t" in df.columns:
                    df["t"] = pd.to_datetime(df["t"])
                    df.rename(columns={"t": "timestamp"}, inplace=True)
                # Set timestamp as index
                if "timestamp" in df.columns:
                    df.set_index("timestamp", inplace=True)
                # Rename columns to match existing pattern
                column_mapping = {
                    "o": "open",
                    "h": "high",
                    "l": "low",
                    "c": "close",
                    "v": "volume",
                    "n": "trade_count",
                    "vw": "vwap",
                }
                df.rename(columns=column_mapping, inplace=True)
                result[symbol] = df

        # Return single DataFrame for single symbol, dict for multiple
        if is_single and symbols_list[0] in result:
            return result[symbols_list[0]]
        return result
