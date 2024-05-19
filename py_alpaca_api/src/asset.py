import json

import pandas as pd
import requests

from .data_classes import AssetClass, asset_class_from_dict


class Asset:
    def __init__(self, trade_url: str, headers: object) -> None:
        """Initialize Asset class

        Parameters:
        ___________
        trade_url: str
                Alpaca Trade API URL required

        headers: object
                API request headers required

        Raises:
        _______
        ValueError: If trade URL is not provided

        ValueError: If headers are not provided
        """  # noqa

        self.trade_url = trade_url
        self.headers = headers

    def get_all(
        self,
        status: str = "active",
        asset_class: str = "us_equity",
        exchange: str = "",
    ) -> pd.DataFrame:
        # Alpaca API URL for asset information
        url = f"{self.trade_url}/assets"

        params = {
            "status": status,
            "asset_class": asset_class,
            "exchange": exchange,
        }

        # Get request to Alpaca API for asset information
        response = requests.get(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res_df = pd.json_normalize(json.loads(response.text))

            res_df = res_df[res_df["status"] == "active"]
            res_df = res_df[res_df["fractionable"]]
            res_df = res_df[res_df["tradable"]]
            res_df = res_df[res_df["exchange"] != "OTC"]
            res_df.reset_index(drop=True, inplace=True)

            # Return asset information as an AssetClass object
            return res_df
        # If response is not successful, raise an exception
        else:
            raise ValueError(f"Failed to get asset information. Response: {response.text}")

    #####################################################
    # \\\\\\\\\\\\\\\\\\\  Get Asset ////////////////////#
    #####################################################
    def get(self, symbol: str) -> AssetClass:
        """Get asset information from Alpaca API

        Parameters:
        ___________
        symbol: str
                Asset symbol required

        Returns:
        ________
        AssetClass: Asset information as an AssetClass object

        Raises:
        _______
        ValueError: If the response is not successful

        Example:
        ________
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            asset = api.asset.get(symbol="AAPL")
            print(asset)

        AssetClass(
            asset_id="375f6b6e-3b5f-4b2b-8f6b-2e6b2a6b2e6b",
            class="us_equity",
            easy_to_borrow=True,
            exchange="NASDAQ",
            id="375f6b6e-3b5f-4b2b-8f6b-2e6b2a6b2e6b",
            marginable=True,
            name="Apple Inc",
            shortable=True,
            status="active",
            symbol="AAPL",
            tradable=True
        )
        """  # noqa

        # Alpaca API URL for asset information
        url = f"{self.trade_url}/assets/{symbol}"
        # Get request to Alpaca API for asset information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return asset information as an AssetClass object
            return asset_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise ValueError(f"Failed to get asset information. Response: {response.text}")
