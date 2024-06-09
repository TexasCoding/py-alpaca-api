import json
from collections import defaultdict
from typing import Dict

import pandas as pd

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.asset_model import AssetModel
from py_alpaca_api.stock.assets import Assets


class History:
    def __init__(self, data_url: str, headers: Dict[str, str], asset: Assets) -> None:
        """
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
        """Check if asset is stock
        Args:
            symbol: The symbol of the asset to be checked.

        Returns:
            AssetModel: The asset information for the given symbol.

        Raises:
            ValueError: If there is an error getting the asset information or if the asset is not a stock.
        """

        try:
            asset = self.asset.get(symbol)
        except Exception as e:
            raise ValueError(e)
        if asset.asset_class != "us_equity":
            raise ValueError(f"{symbol} is not a stock.")
        return asset

    ###########################################
    # ////// Get Stock Historical Data \\\\\\ #
    ###########################################
    def get_stock_data(
        self,
        symbol: str,
        start: str,
        end: str,
        timeframe: str = "1d",
        feed: str = "sip",
        currency: str = "USD",
        limit: int = 1000,
        sort: str = "asc",
        adjustment: str = "raw",
    ) -> pd.DataFrame:
        """
        Args:
            symbol: The stock symbol to fetch data for.
            start: The start date for historical data in the format "YYYY-MM-DD".
            end: The end date for historical data in the format "YYYY-MM-DD".
            timeframe: The timeframe for the historical data. Default is "1d".
            Possible values are "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", or "1M".
            feed: The data feed source. Default is "sip".
            currency: The currency for historical data. Default is "USD".
            limit: The number of data points to fetch. Default is 1000.
            sort: The sort order for the data. Default is "asc".
            adjustment: The adjustment for historical data. Default is "raw".

        Returns:
            A pandas DataFrame containing the historical stock data for the given symbol and time range.

        Raises:
            ValueError: If the given timeframe is not one of the allowed values.
        """
        self.check_if_stock(symbol)

        url = f"{self.data_url}/stocks/{symbol}/bars"

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

        params = {
            "timeframe": timeframe_mapping[
                timeframe
            ],  # Timeframe for historical data, default: 1d
            "start": start,  # Start date for historical data
            "end": end,  # End date for historical data
            "currency": currency,  # Currency for historical data, default: USD
            "limit": limit,  # Limit number of data points, default: 1000
            "adjustment": adjustment,  # Adjustment for historical data, default: raw
            "feed": feed,  # Data feed source, default: iex
            "sort": sort,  # Sort order, default: asc
        }
        symbol_data = self.get_historical_data(symbol, url, params)
        bar_data_df = self.preprocess_data(symbol_data, symbol)
        return bar_data_df

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

        bar_data_df = bar_data_df.astype(
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

        return bar_data_df

    ###########################################
    # ///////// Get Historical Data \\\\\\\\\ #
    ###########################################
    def get_historical_data(
        self, symbol: str, url: str, params: dict
    ) -> list[defaultdict]:
        """
        Retrieves historical data for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve historical data.
            url (str): The URL to send the request to.
            params (dict): Additional parameters to include in the request.

        Returns:
            list[defaultdict]: A list of historical data for the given symbol.
        """
        page_token = None
        symbols_data = defaultdict(list)
        while True:
            params["page_token"] = page_token
            response = json.loads(
                Requests()
                .request(method="GET", url=url, headers=self.headers, params=params)
                .text
            )

            if not response.get("bars"):
                raise Exception(
                    f"No historical data found for {symbol}, with the given parameters."
                )

            symbols_data[symbol].extend(response.get("bars", []))
            page_token = response.get("next_page_token", "")
            if not page_token:
                break
        return symbols_data[symbol]
