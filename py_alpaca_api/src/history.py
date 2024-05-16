import json

import pandas as pd
import requests

from .asset import Asset


class History:
    def __init__(self, data_url: str, headers: object, asset: Asset) -> None:
        """Initialize History class

        Parameters:
        ___________
        data_url: str
                Alpaca Data API URL required

        headers: object
                API request headers required

        asset: Asset
                Asset object required

        Raises:
        _______
        ValueError: If data URL is not provided

        ValueError: If headers are not provided

        ValueError: If asset is not provided
        """  # noqa

        self.data_url = data_url
        self.headers = headers
        self.asset = asset

    ############################
    # Get Stock Historical Data
    ############################
    def get_stock_data(
        self,
        symbol,
        start,
        end,
        timeframe="1d",
        feed="iex",
        currency="USD",
        limit=1000,
        sort="asc",
        adjustment="raw",
    ) -> pd.DataFrame:
        """Get historical stock data from Alpaca API

        Parameters:
        ___________
        symbol: str
                Stock symbol required

        start: str
                Start date for historical data required, format: YYYY-MM-DD

        end: str
                End date for historical data required, format: YYYY-MM-DD

        timeframe: str
                Timeframe for historical data, default: 1d
                Choices: "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1m"

        feed: str
                Data feed source, default: iex
                Choices: "iex", "sip", "otc"

        currency: str
                Currency for historical data, default: USD

        limit: int
                Limit number of data points, default: 1000
                The maximum number of data points to return in the response.

        sort: str
                Sort order, default: asc, Choices: "asc", "desc"

        adjustment: str
                Adjustment for historical data, default: raw
                Choices: "raw", "split", "dividend", "merger", "all"

        Returns:
        ________
        pd.DataFrame: Historical stock data as a DataFrame

        Raises:
        _______
        ValueError: If the response is not successful

        ValueError: If the asset is not a stock

        ValueError: If no data is available

        ValueError: If invalid timeframe is provided

        Example:
        ________
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            stock_data = api.history.get_stock_data(symbol="AAPL", start="2021-01-01", end="2021-12-31", timeframe="1d")
            print(stock_data)

        symbol       date    open    high     low   close    volume  trade_count     vwap
        AAPL    2021-01-04  133.52  133.61  126.76  129.41  143301887      1009115  130.914
        AAPL    2021-01-05  128.89  131.74  128.43  131.01   97664898       678471  130.573
        AAPL    2021-01-06  127.72  131.05  126.38  126.60  155087970      1135783  128.073
        AAPL    2021-01-07  128.36  131.63  127.86  130.92  109578157       791297  129.918
        AAPL    2021-01-08  132.43  132.63  130.23  132.05  105158245       743315  131.573
        ...            ...     ...     ...     ...     ...        ...          ...      ...
        AAPL    2021-12-23  176.69  177.36  175.55  177.36   30925200       123456  176.423
        AAPL    2021-12-27  177.41  179.15  177.36  179.15   36254100       145236  178.423
        AAPL    2021-12-28  179.15  179.25  177.36  177.36   30925200       123456  178.423
        AAPL    2021-12-29  177.36  179.15  177.36  179.15   36254100       145236  178.423
        AAPL    2021-12-30  179.15  179.25  177.36  177.36   30925200       123456  178.423

        [252 rows x 9 columns]
        """  # noqa

        # Get asset information for the symbol
        try:
            asset = self.asset.get(symbol)
        # Raise exception if failed to get asset information
        except Exception as e:
            raise ValueError(e)
        else:
            # Check if asset is a stock
            if asset.asset_class != "us_equity":
                # Raise exception if asset is not a stock
                raise ValueError(f"{symbol} is not a stock.")
        # URL for historical stock data request
        url = f"{self.data_url}/stocks/{symbol}/bars"
        # Set timeframe
        match timeframe:
            case "1m":
                timeframe = "1Min"
            case "5m":
                timeframe = "5Min"
            case "15m":
                timeframe = "15Min"
            case "30m":
                timeframe = "30Min"
            case "1h":
                timeframe = "1Hour"
            case "4h":
                timeframe = "4Hour"
            case "1d":
                timeframe = "1Day"
            case "1w":
                timeframe = "1Week"
            case "1m":
                timeframe = "1Month"
            case _:
                # Raise exception if invalid timeframe is provided
                raise ValueError('Invalid timeframe. Must be "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", or "1m"')
        # Parameters for historical stock data request
        params = {
            "timeframe": timeframe,  # Timeframe for historical data, default: 1d
            "start": start,  # Start date for historical data
            "end": end,  # End date for historical data
            "currency": currency,  # Currency for historical data, default: USD
            "limit": limit,  # Limit number of data points, default: 1000
            "adjustment": adjustment,  # Adjustment for historical data, default: raw
            "feed": feed,  # Data feed source, default: iex
            "sort": sort,  # Sort order, default: asc
        }
        # Get historical stock data from Alpaca API
        response = requests.get(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code != 200:
            # Raise exception if response is not successful
            raise Exception(json.loads(response.text)["message"])
        # Convert JSON response to dictionary
        res_json = json.loads(response.text)["bars"]
        # Check if data is available
        if not res_json:
            raise ValueError(f"No data available for {symbol}.")
        # Normalize JSON response and convert to DataFrame
        bar_data_df = pd.json_normalize(res_json)
        # Add symbol column to DataFrame
        bar_data_df.insert(0, "symbol", symbol)
        # Reformat date column
        bar_data_df["t"] = pd.to_datetime(bar_data_df["t"].replace("[A-Za-z]", " ", regex=True))
        # Rename columns for consistency
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
        # Convert columns to appropriate data types
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
        # Return historical stock data as a DataFrame
        return bar_data_df
