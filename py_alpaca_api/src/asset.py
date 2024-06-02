import json
from typing import Dict

import pandas as pd

from .data_classes import AssetClass, asset_class_from_dict
from .requests import Requests


class Asset:
    def __init__(self, trade_url: str, headers: Dict[str, str]) -> None:
        """
        Initialize a new Asset object.

        Args:
            trade_url (str): The trade URL for the asset.
            headers (Dict[str, str]): The headers for the asset.

        Returns:
            None
        """
        self.trade_url = trade_url
        self.headers = headers

    def get_all(
        self,
        status: str = "active",
        asset_class: str = "us_equity",
        exchange: str = "",
    ) -> pd.DataFrame:
        """
        Retrieves all assets based on the specified parameters.

        Args:
            status (str, optional): The status of the assets to retrieve. Defaults to "active".
            asset_class (str, optional): The asset class of the assets to retrieve. Defaults to "us_equity".
            exchange (str, optional): The exchange of the assets to retrieve. Defaults to "".

        Returns:
            pd.DataFrame: A DataFrame containing the asset information.

        Raises:
            ValueError: If the request to the Alpaca API fails.
        """

        url = f"{self.trade_url}/assets"
        params = {
            "status": status,
            "asset_class": asset_class,
            "exchange": exchange,
        }

        assets_df = pd.json_normalize(json.loads(Requests().get(url, headers=self.headers, params=params).text))

        assets_df = assets_df[
            (assets_df["status"] == "active") & (assets_df["fractionable"]) & (assets_df["tradable"]) & (assets_df["exchange"] != "OTC")
        ]
        assets_df.reset_index(drop=True, inplace=True)

        return assets_df

    #####################################################
    # \\\\\\\\\\\\\\\\\\\  Get Asset ////////////////////#
    #####################################################
    def get(self, symbol: str) -> AssetClass:
        """
        Retrieves asset information for a given symbol.

        Args:
            symbol (str): The symbol of the asset.

        Returns:
            AssetClass: An object representing the asset information.

        Raises:
            ValueError: If the request to the Alpaca API fails.
        """
        url = f"{self.trade_url}/assets/{symbol}"
        response = json.loads(Requests().get(url, headers=self.headers).text)
        return asset_class_from_dict(response)
