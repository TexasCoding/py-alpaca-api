import json
from typing import Dict, List

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
        Retrieves an AssetModel for the specified symbol.

        Args:
            symbol (str): The symbol of the asset to retrieve.

        Returns:
            AssetModel: The AssetModel for the specified asset.

        Raises:
            Exception: If the asset is not a US Equity (stock).
        """

        url = f"{self.base_url}/assets/{symbol}"
        response = json.loads(Requests().request("GET", url, headers=self.headers).text)

        if response.get("class") != "us_equity":
            raise Exception("Asset is not a US Equity (stock)")

        return asset_class_from_dict(response)

    ############################################
    # Get All Assets
    ############################################
    def get_all(
        self,
        status: str = "active",
        exchange: str = "",
        excluded_exchanges: List[str] = ["OTC"],
    ) -> pd.DataFrame:
        """
        Retrieves a DataFrame of all active, fractionable, and tradable US equity assets, excluding those from the OTC exchange.

        Args:
            status (str, optional): The status of the assets to retrieve. Defaults to "active".
            exchange (str, optional): The exchange to filter the assets by. Defaults to an empty string, which retrieves assets from all exchanges.
            excluded_exchanges (List[str], optional): A list of exchanges to exclude from the results. Defaults to ["OTC"].

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved assets.
        """

        url = f"{self.base_url}/assets"

        params = {"status": status, "asset_class": "us_equity", "exchange": exchange}
        response = json.loads(
            Requests().request("GET", url, headers=self.headers, params=params).text
        )
        assets_df = pd.DataFrame(response)

        assets_df = assets_df[
            (assets_df["status"] == "active")
            & (assets_df["fractionable"])
            & (assets_df["tradable"])
            & (~assets_df["exchange"].isin(excluded_exchanges))
        ]
        assets_df.reset_index(drop=True, inplace=True)
        return assets_df
