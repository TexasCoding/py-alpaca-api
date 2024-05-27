import json
from typing import Dict

# import pandas as pd
import requests


class SnapShot:
    def __init__(self, data_url: str, headers: Dict[str, str]):
        self.data_url = data_url
        self.headers = headers

    def latest_trade(self, symbol: str, feed: str = "iex", currency: str = "USD") -> dict:
        """Get the latest trade for a given symbol.
        Args:
            symbol: A string representing the symbol of the asset.
        Returns:
            pd.DataFrame: A DataFrame containing the latest trade data.
        Raises:
            ValueError: If there is an error getting the latest trade data.
        """
        url = f"{self.data_url}/stocks/{symbol}/snapshot"
        params = {"feed": feed, "currency": currency}

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(json.loads(response.text)["message"])

        snapshot_data = response.json()

        return snapshot_data["latestTrade"]
