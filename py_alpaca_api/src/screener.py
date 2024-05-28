import json
from typing import Dict

import pandas as pd
import pendulum
import requests

from .asset import Asset
from .market import Market


class Screener:
    def __init__(
        self,
        data_url: str,
        headers: Dict[str, str],
        asset: Asset,
        market: Market,
    ) -> None:
        """Initialize Screener class3

        Parameters:
        ___________
        data_url: str
                Alpaca Data API URL required

        headers: object
                API request headers required

        asset: Asset                 object required

        Raises:
        _______
        ValueError: If data URL is not provided

        ValueError: If headers are not provided

        ValueError: If asset is not provided
        """
        self.data_url = data_url
        self.headers = headers
        self.asset = asset
        self.market = market

        self.yesterday = ""
        self.day_before_yesterday = ""

    ##################################################
    # /////////////// Filter Stocks \\\\\\\\\\\\\\\\ #
    ##################################################
    def filter_stocks(
        self,
        price_greater_than: float,
        change_condition: callable,
        volume_greater_than: int,
        trade_count_greater_than: int,
        total_returned: int,
        ascending_order: bool,
    ) -> pd.DataFrame:
        """
        Filter stocks based on given parameters.

        Args:
            price_greater_than: The minimum price threshold for the stocks.
            change_condition: A callable function that takes in a DataFrame and returns a boolean value.
                This function is used to filter the stocks based on a specific change condition.
            volume_greater_than: The minimum volume threshold for the stocks.
            trade_count_greater_than: The minimum trade count threshold for the stocks.
            total_returned: The number of stocks to return.
            ascending_order: A boolean value indicating whether to sort the stocks in ascending order by change value.

        Returns:
            A pandas DataFrame containing the filtered stocks.
        """
        self.set_dates()
        df = self._get_percentages(start=self.day_before_yesterday, end=self.yesterday)
        df = df[df["price"] > price_greater_than]
        df = df[change_condition(df)]
        df = df[df["volume"] > volume_greater_than]
        df = df[df["trades"] > trade_count_greater_than]
        return df.sort_values(by="change", ascending=ascending_order).reset_index(drop=True).head(total_returned)

    ##################################################
    # //////////////// Get Losers \\\\\\\\\\\\\\\\\\ #
    ##################################################
    def losers(
        self,
        price_greater_than: float = 5.0,
        change_less_than: float = -2.0,
        volume_greater_than: int = 20000,
        trade_count_greater_than: int = 2000,
        total_losers_returned: int = 100,
    ) -> pd.DataFrame:
        """
        Returns a filtered DataFrame of stocks that meet the specified conditions for losers.

        Args:
            price_greater_than (float): The minimum price threshold for stocks to be considered losers. Default is 5.0.
            change_less_than (float): The maximum change threshold for stocks to be considered losers. Default is -2.0.
            volume_greater_than (int): The minimum volume threshold for stocks to be considered losers. Default is 20000.
            trade_count_greater_than (int): The minimum trade count threshold for stocks to be considered losers. Default is 2000.
            total_losers_returned (int): The maximum number of losers to be returned. Default is 100.

        Returns:
            pd.DataFrame: A filtered DataFrame containing stocks that meet the specified conditions for losers.
        """
        return self.filter_stocks(
            price_greater_than,
            lambda df: df["change"] < change_less_than,
            volume_greater_than,
            trade_count_greater_than,
            total_losers_returned,
            ascending_order=True,
        )

    ##################################################
    # //////////////// Get Gainers \\\\\\\\\\\\\\\\\ #
    ##################################################
    def gainers(
        self,
        price_greater_than: float = 5.0,
        change_greater_than: float = 2.0,
        volume_greater_than: int = 20000,
        trade_count_greater_than: int = 2000,
        total_gainers_returned: int = 100,
    ) -> pd.DataFrame:
        """
        Args:
            price_greater_than (float): The minimum price threshold for the stocks to be included in the gainers list. Default is 5.0.
            change_greater_than (float): The minimum change (in percentage) threshold for the stocks to be included in the gainers list.
            Default is 2.0.
            volume_greater_than (int): The minimum volume threshold for the stocks to be included in the gainers list. Default is 20000.
            trade_count_greater_than (int): The minimum trade count threshold for the stocks to be included in the gainers list. Default is 2000.
            total_gainers_returned (int): The maximum number of gainers to be returned. Default is 100.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the stocks that satisfy the criteria for being gainers.

        """
        return self.filter_stocks(
            price_greater_than,
            lambda df: df["change"] > change_greater_than,
            volume_greater_than,
            trade_count_greater_than,
            total_gainers_returned,
            ascending_order=False,
        )

    ##################################################
    # /////////// Calculate Percentages \\\\\\\\\\\\ #
    ##################################################
    def _get_percentages(
        self,
        start: str,
        end: str,
        timeframe: str = "1Day",
    ) -> pd.DataFrame:
        """Get percentage changes for the previous day

        Parameters:
        ___________
        timeframe: str
                Timeframe optional, default is 1Day

        start: str
                Start date optional, default is yesterday

        end: str
                End date optional, default is yesterday

        Returns:
        _______
        pd.DataFrame: Percentage changes for the previous day

        Raises:
        _______
        ValueError: If failed to get top gainers
        """
        url = f"{self.data_url}/stocks/bars"

        params = {
            "symbols": ",".join(self.asset.get_all()["symbol"].tolist()),
            "limit": 10000,
            "timeframe": timeframe,
            "start": start,
            "end": end,
            "feed": "sip",
            "currency": "USD",
            "page_token": "",
            "sort": "asc",
        }

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            res = json.loads(response.text)

            bars_df = pd.DataFrame.from_dict(res["bars"], orient="index")
            page_token = res["next_page_token"]

            while page_token:
                params["page_token"] = page_token
                response = requests.get(url, headers=self.headers, params=params)
                res = json.loads(response.text)
                bars_df = pd.concat(
                    [
                        bars_df,
                        pd.DataFrame.from_dict(res["bars"], orient="index"),
                    ]
                )
                page_token = res["next_page_token"]

            bars_df.reset_index()

            all_bars_df = pd.DataFrame()

            for bar in bars_df.iterrows():
                try:
                    change = round(
                        ((bar[1][1]["c"] - bar[1][0]["c"]) / bar[1][0]["c"]) * 100,
                        2,
                    )
                    symbol = bar[0]

                    sym_data = {
                        "symbol": symbol,
                        "change": change,
                        "price": bar[1][1]["c"],
                        "volume": bar[1][1]["v"],
                        "trades": bar[1][1]["n"],
                    }
                    all_bars_df = pd.concat([all_bars_df, pd.DataFrame([sym_data])])

                except KeyError:
                    pass
            all_bars_df.reset_index(drop=True, inplace=True)
            return all_bars_df
        else:
            raise ValueError(f"Failed to get assets. Response: {response.text}")

    ##################################################
    # ///////////////// Set Dates \\\\\\\\\\\\\\\\\\ #
    ##################################################
    def set_dates(self):
        """
        Sets the dates for the screener.

        This method retrieves the last two trading dates from the market calendar
        and assigns them to the `yesterday` and `day_before_yesterday` attributes.

        Returns:
            None
        """
        today = pendulum.now(tz="America/New_York")

        calender = (
            self.market.calender(
                start_date=today.subtract(days=7).format("YYYY-MM-DD"),
                end_date=today.subtract(days=1).format("YYYY-MM-DD"),
            )
            .tail(2)
            .reset_index(drop=True)
        )

        self.yesterday = calender.iloc[1]["date"].strftime("%Y-%m-%d")
        self.day_before_yesterday = calender.iloc[0]["date"].strftime("%Y-%m-%d")
