import json
from datetime import datetime, timedelta

import pandas as pd
import requests
from pytz import timezone

from .asset import Asset

tz = timezone("US/Eastern")
ctime = datetime.now(tz)
close = (ctime - timedelta(days=1)).strftime("%Y-%m-%d")
prev_close = (ctime - timedelta(days=2)).strftime("%Y-%m-%d")


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

    def gainers(self, timeframe: str = "1Day", start: str = prev_close, end: str = close) -> pd.DataFrame:
        """Get top gainers for the day

        Returns:
        _______
        pd.DataFrame: Top gainers for the day
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

            # res_df = pd.json_normalize(res, max_level=0)["bars"]
            # bars_df = pd.json_normalize(res_df[0], max_level=0)

            bars_df = pd.DataFrame.from_dict(res["bars"], orient="index")
            page_token = res["next_page_token"]

            while page_token:
                params["page_token"] = page_token
                response = requests.get(url, headers=self.headers, params=params)
                res = json.loads(response.text)
                bars_df = pd.concat([bars_df, pd.DataFrame.from_dict(res["bars"], orient="index")])
                page_token = res["next_page_token"]

            bars_df.reset_index()

            # gainer_df = pd.DataFrame()

            for bar in bars_df.iterrows():
                # bar[0] is symbol
                # bar[1][1] is current bar
                # bar[1][0] is previous bar
                # bar[1][1]["c"] is current close
                # bar[1][0]["c"] is previous close
                # ((current close - previous close) / previous close) * 100
                try:
                    change = ((bar[1][1]["c"] - bar[1][0]["c"]) / bar[1][0]["c"]) * 100
                except Exception:
                    pass
                print(change)

            # print(bars_df)

            # return res_df["bars"]
        else:
            raise ValueError(f"Failed to get top gainers. Response: {response.text}")
