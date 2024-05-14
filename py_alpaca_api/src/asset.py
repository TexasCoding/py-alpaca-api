import json

import requests

from .data_classes import AssetClass, asset_class_from_dict


class Asset:
    def __init__(self, trade_url: str, headers: object) -> None:
        self.trade_url = trade_url
        self.headers = headers

    #####################################################
    # \\\\\\\\\\\\\\\\\\\  Get Asset ////////////////////#
    #####################################################
    def get(self, symbol: str) -> AssetClass:
        """Get asset information by symbol

        Parameters:
        -----------
        symbol:     Asset symbol to get information
                    A valid asset symbol string required

        Returns:
        --------
        AssetClass: Asset information as an AssetClass object with values:
                    id, class, exchange, symbol, status, tradable, marginable, shortable, easy_to_borrow
                
        Raises:
        -------
        ValueError: 
            ValueError if failed to get asset information

        Example:
        --------
        >>> get_asset(symbol="AAPL")
        AssetClass(id='ASSET_ID', class='us_equity', exchange='NASDAQ', symbol='AAPL', status='active', \
                    tradable=True, marginable=True, shortable=True, easy_to_borrow=True)

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
