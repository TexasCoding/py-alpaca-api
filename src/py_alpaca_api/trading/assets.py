import json
from typing import Dict

import pandas as pd

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.asset_model import AssetModel, asset_class_from_dict


class Assets:
    def __init__(self, base_url: str, headers: Dict[str, str]) -> None:
        self.base_url = base_url
        self.headers = headers

    ############################################
    # Get Asset
    ############################################
    def get(self, symbol: str) -> AssetModel:
        """
        Retrieves an asset model for the given symbol from the Alpaca API.

        Args:
            symbol (str): The symbol of the asset to retrieve.

        Returns:
            AssetModel: The asset model for the given symbol.
        """

        url = f"{self.base_url}/assets/{symbol}"
        response = json.loads(Requests().request("GET", url, headers=self.headers).text)
        return asset_class_from_dict(response)

    ############################################
    # Get All Assets
    ############################################
    def get_all(
        self, status: str = "active", asset_class: str = "us_equity", exchange: str = ""
    ) -> pd.DataFrame:
        """
        Retrieves a DataFrame of all active, fractionable, and tradable assets from the Alpaca API.

        Args:
            status (str, optional): The status of the assets to retrieve. Defaults to "active".
            asset_class (str, optional): The asset class of the assets to retrieve. Defaults to "us_equity".
            exchange (str, optional): The exchange of the assets to retrieve. Defaults to an empty string, which retrieves assets from all exchanges.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved assets.
        """

        url = f"{self.base_url}/assets"
        params = {"status": status, "asset_class": asset_class, "exchange": exchange}
        response = json.loads(
            Requests().request("GET", url, headers=self.headers, params=params).text
        )
        assets_df = pd.DataFrame(response)

        assets_df = assets_df[
            (assets_df["status"] == "active")
            & (assets_df["fractionable"])
            & (assets_df["tradable"])
            & (assets_df["exchange"] != "OTC")
        ]
        assets_df.reset_index(drop=True, inplace=True)
        return assets_df
