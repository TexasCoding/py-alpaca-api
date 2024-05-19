import json

import pandas as pd
import pendulum
import requests

from .asset import Asset

# This keeps the date in sync with the market
# If it's a weekend, it will return the previous Friday
# If it's a weekday, it will return the previous day, other than Monday
# If it's Monday, it will return the previous Friday
today = pendulum.now(tz="America/New_York")
yesterday = today.subtract(days=1).strftime("%Y-%m-%d")
if today.day_of_week == (pendulum.SUNDAY or pendulum.MONDAY):
    yesterday = today.previous(pendulum.FRIDAY).strftime("%Y-%m-%d")
######################################################################


class Screener:
    def __init__(self, data_url: str, headers: object, asset: Asset) -> None:
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
        """  # noqa
        self.data_url = data_url
        self.headers = headers
        self.asset = asset

    def losers(
        self,
        price_greater_than: float = 5.0,
        change_less_than: float = -2.0,
        volume_greater_than: int = 20000,
        trade_count_greater_than: int = 2000,
        total_losers_returned: int = 100,
    ) -> pd.DataFrame:
        """Get top losers for the day

        Parameters:
        ___________
        price_greater_than: float
                Price greater than optional, default is 5.0

        change_less_than: float
                Change less than optional, default is -2.0

        volume_greater_than: int
                Volume greater than optional, default is 20000

        trade_count_greater_than: int
                Trade count greater than optional, default is 2000

        total_losers_returned: int
                Total losers returned optional, default is 100

        Returns:
        _______
        pd.DataFrame: Top losers for the day

        Raises:
        _______
        ValueError: If failed to get top losers
        """  # noqa
        losers_df = self._get_percentages()

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
        """Get top gainers for the day

        Parameters:
        ___________
        price_greater_than: float
                Price greater than optional, default is 5.0

        change_greater_than: float
                Change greater than optional, default is 2.0

        volume_greater_than: int
                Volume greater than optional, default is 20000

        trade_count_greater_than: int
                Trade count greater than optional, default is 2000

        total_gainers_returned: int
                Total gainers returned optional, default is 100

        Returns:
        _______
        pd.DataFrame: Top gainers for the day

        Raises:
        _______
        ValueError: If failed to get top gainers
        """  # noqa

        gainers_df = self._get_percentages()

        gainers_df = gainers_df[gainers_df["price"] > price_greater_than]
        gainers_df = gainers_df[gainers_df["change"] > change_greater_than]
        gainers_df = gainers_df[gainers_df["volume"] > volume_greater_than]
        gainers_df = gainers_df[gainers_df["trades"] > trade_count_greater_than]
        return gainers_df.sort_values(by="change", ascending=False).reset_index(drop=True).head(total_gainers_returned)

    def _get_percentages(
        self,
        timeframe: str = "1Day",
        start: str = yesterday,
        end: str = yesterday,
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
        """  # noqa
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

            gainer_df = pd.DataFrame()

            for bar in bars_df.iterrows():
                # bar[0] is symbol
                # bar[1][1] is current bar
                # bar[1][0] is previous bar
                # bar[1][1]["c"] is current close
                # bar[1][0]["c"] is previous close
                # ((current close - previous close) / previous close) * 100
                # print(bar[1][0])
                try:
                    change = round(
                        ((bar[1][0]["c"] - bar[1][0]["o"]) / bar[1][0]["o"]) * 100,
                        2,
                    )

                    symbol = bar[0]

                    sym_data = {
                        "symbol": symbol,
                        "change": change,
                        "price": bar[1][0]["c"],
                        "volume": bar[1][0]["v"],
                        "trades": bar[1][0]["n"],
                    }
                    gainer_df = pd.concat([gainer_df, pd.DataFrame([sym_data])])

                except Exception:
                    pass
            gainer_df.reset_index(drop=True, inplace=True)
            return gainer_df
        else:
            raise ValueError(f"Failed to get top gainers. Response: {response.text}")
