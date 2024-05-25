import json
from typing import Dict

import pandas as pd
import requests

from .data_classes import AccountClass, account_class_from_dict


class Account:
    def __init__(self, trade_url: str, headers: Dict[str, str]) -> None:
        """
        Args:
            trade_url: The URL for the trade.
            headers: The headers for the trade request.
        """
        self.trade_url = trade_url
        self.headers = headers

    ########################################################
    # \\\\\\\\\\\\\  Get Account Information ///////////////#
    ########################################################
    def get(self) -> AccountClass:
        """
        get(self) -> AccountClass
            Get account information from Alpaca API.

            Returns:
                AccountClass: An instance of the AccountClass representing the account information.

            Raises:
                Exception: If the request fails or the response status code is not 200.

            Usage:
                account = get()

            Example:
                >>> account = account.get()
        """
        # Alpaca API URL for account information
        url = f"{self.trade_url}/account"
        # Get request to Alpaca API for account information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return account information as an AccountClass object
            return account_class_from_dict(res)
        # If response is not successful, raise an exception
        else:
            raise Exception(f"Failed to get account information. Response: {response.text}")

    ########################################################
    # \\\\\\\\\\\\\  Get Portfolio History ///////////////#
    ########################################################
    def portfolio_history(
        self,
        period: str = "1W",
        timeframe: str = "1D",
        intraday_reporting: str = "market_hours",
    ) -> pd.DataFrame:
        """
        Args:
            period (str): The period of time for which the portfolio history is requested. Defaults to "1W" (1 week).
            timeframe (str): The timeframe for the intervals of the portfolio history. Defaults to "1D" (1 day).
            intraday_reporting (str): The type of intraday reporting to be used. Defaults to "market_hours".

        Returns:
            pd.DataFrame: A pandas DataFrame containing the portfolio history data.

        Raises:
            Exception: If the request to the Alpaca API fails.

        """

        url = f"{self.trade_url}/account/portfolio/history"

        response = requests.get(
            url,
            headers=self.headers,
            params={
                "period": period,
                "timeframe": timeframe,
                "intraday_reporting": intraday_reporting,
            },
        )

        if response.status_code == 200:
            res = json.loads(response.text)
            res_df = pd.DataFrame(
                res,
                columns=[
                    "timestamp",
                    "equity",
                    "profit_loss",
                    "profit_loss_pct",
                    "base_value",
                ],
            )

            timestamp_transformed = (
                pd.to_datetime(res_df["timestamp"], unit="s").dt.tz_localize("America/New_York").dt.tz_convert("UTC").apply(lambda x: x.date())
            )
            res_df["timestamp"] = timestamp_transformed
            res_df["profit_loss_pct"] = res_df["profit_loss_pct"] * 100
            return res_df
        else:
            raise Exception(f"Failed to get portfolio information. Response: {response.text}")
