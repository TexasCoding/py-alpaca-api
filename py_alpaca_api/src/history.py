import json

import pandas as pd
import requests

from .asset import Asset


class History:
    def __init__(self, data_url: str, headers: object, asset: Asset) -> None:
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
        """Get historical stock data for a given symbol

        Parameters:
        -----------
        symbol:     Stock symbol
                    A valid stock symbol (e.g., AAPL) string required

        start:      Start date for historical data
                    A valid start date string in the format "YYYY-MM-DD" required

        end:        End date for historical data
                    A valid end date string in the format "YYYY-MM-DD" required

        timeframe:  Timeframe for historical data
                    (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1m) (default: 1d) (optional)

        feed:       Data feed source
                    (iex, sip, tops, last, hist) (default: iex) (optional)

        currency:   Currency for historical data (default: USD)
                    Supported currencies: USD, CAD, EUR, GBP, JPY, AUD, CNY, HKD

        limit:      Limit number of data points (default: 1000)
                    Maximum number of data points to return (optional) int

        sort:       Sort order (asc, desc) (default: asc)

        adjustment: Adjustment for historical data (raw, split, dividends) (default: raw)

        Returns:
        --------
        DataFrame:  Historical stock data as a DataFrame with columns:
                    symbol, date, open, high, low, close, volume, trade_count, vwap

        Raises:
        -------
        Exception:
            Exception if failed to get historical stock data

        ValueError:
            ValueError if symbol is not a stock

        ValueError:
            ValueError if invalid timeframe

        ValueError:
            ValueError if no data available for symbol

        Example:
        --------
        >>> get_stock_historical_data(symbol="AAPL", start="2021-01-01", end="2021-12-31", timeframe="1d")
            symbol  close   high    low     trade_count open    date        volume      vwap
        0   AAPL    132.69  133.61  132.16  1           133.52  2021-01-04  100620780   132.69

        >>> get_stock_historical_data(symbol="FAKESYMBOL", start="2021-01-01", end="2021-12-31", timeframe="1d")
        ValueError: Failed to get asset information. Response: {"code":40410001,"message":"symbol not found: FAKESYMBOL"}
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
