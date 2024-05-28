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

        asset: Asset
                Asset object required

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

    def losers(
        self,
        price_greater_than: float = 5.0,
        change_less_than: float = -2.0,
        volume_greater_than: int = 20000,
        trade_count_greater_than: int = 2000,
        total_losers_returned: int = 100,
    ) -> pd.DataFrame:
        """
        This method filters and returns a DataFrame of stock losers based on specific criteria.

        Args:
            price_greater_than (float): The minimum price of the losers. Defaults to 5.0.
            change_less_than (float): The maximum change percentage of the losers. Defaults to -2.0.
            volume_greater_than (int): The minimum trading volume of the losers. Defaults to 20000.
            trade_count_greater_than (int): The minimum trade count of the losers. Defaults to 2000.
            total_losers_returned (int): The number of losers to be returned. Defaults to 100.

        Returns:
            pd.DataFrame: DataFrame containing the filtered stock losers sorted by change percentage in ascending order.

        Example:
            losers_df = losers(price_greater_than=10.0, change_less_than=-5.0, volume_greater_than=50000,
            trade_count_greater_than=3000, total_losers_returned=50)
        """
        self.set_dates()

        losers_df = self._get_percentages(start=self.day_before_yesterday, end=self.yesterday)

        losers_df = losers_df[losers_df["price"] > price_greater_than]
        losers_df = losers_df[losers_df["change"] < change_less_than]
        losers_df = losers_df[losers_df["volume"] > volume_greater_than]
        losers_df = losers_df[losers_df["trades"] > trade_count_greater_than]
        return losers_df.sort_values(by="change", ascending=True).reset_index(drop=True).head(total_losers_returned)

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
            price_greater_than: The minimum price threshold for filtering gainers. Only gainers with prices greater
            than this value will be included. Default is 5.0.
            change_greater_than: The minimum change threshold for filtering gainers. Only gainers with changes greater
            than this value will be included. Default is 2.0.
            volume_greater_than: The minimum volume threshold for filtering gainers. Only gainers with volumes greater
            than this value will be included. Default is 20000.
            trade_count_greater_than: The minimum trade count threshold for filtering gainers. Only gainers with trade
            counts greater than this value will be included. Default is 2000.
            total_gainers_returned: The total number of gainers to be returned. Only the top gainers based on their
            change will be included. Default is 100.

        Returns:
            pd.DataFrame: A DataFrame that contains the filtered gainers that satisfy the given thresholds.
            The DataFrame is sorted by the "change" column in descending order and is limited to the specified
            number of gainers.
        """
        self.set_dates()

        gainers_df = self._get_percentages(start=self.day_before_yesterday, end=self.yesterday)

        gainers_df = gainers_df[gainers_df["price"] > price_greater_than]
        gainers_df = gainers_df[gainers_df["change"] > change_greater_than]
        gainers_df = gainers_df[gainers_df["volume"] > volume_greater_than]
        gainers_df = gainers_df[gainers_df["trades"] > trade_count_greater_than]
        return gainers_df.sort_values(by="change", ascending=False).reset_index(drop=True).head(total_gainers_returned)

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

                except Exception:
                    pass
            all_bars_df.reset_index(drop=True, inplace=True)
            return all_bars_df
        else:
            raise ValueError(f"Failed to get assets. Response: {response.text}")

    @staticmethod
    def get_previous_date(current_date, day_to_look):
        """
        Get the previous date based on the day_to_look from the current_date.
        """
        return current_date.previous(day_to_look).strftime("%Y-%m-%d")

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

        print(f"Yesterday: {self.yesterday}")
        print(f"Day Before Yesterday: {self.day_before_yesterday}")
