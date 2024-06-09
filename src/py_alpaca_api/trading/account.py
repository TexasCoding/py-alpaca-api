from typing import Dict, List
import json
import pandas as pd
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.account_activity_model import (
    AccountActivityModel,
    account_activity_class_from_dict,
)
from py_alpaca_api.models.account_model import AccountModel, account_class_from_dict


class Account:
    def __init__(self, headers: Dict[str, str], base_url: str) -> None:
        self.headers = headers
        self.base_url = base_url

    ############################################
    # Get Account
    ############################################
    def get(self) -> AccountModel:
        """
        Retrieves the user's account information.

        Returns:
            AccountModel: The user's account model.
        """
        url = f"{self.base_url}/account"
        response = json.loads(Requests().request("GET", url, headers=self.headers).text)
        return account_class_from_dict(response)

    #######################################
    # Get Account Activities
    #######################################
    def activities(
        self, activity_type: str, date: str = None, until_date: str = None
    ) -> List[AccountActivityModel]:
        """
        Retrieves the account activities for the specified activity type, optionally filtered by date or until date.

        Args:
            activity_type (str): The type of account activity to retrieve.
            date (str, optional): The date to filter the activities by. If provided, only activities on this date will be returned.
            until_date (str, optional): The date to filter the activities up to. If provided, only activities up to and including this date will be returned.

        Returns:
            List[AccountActivityModel]: A list of account activity models representing the retrieved activities.

        Raises:
            ValueError: If the activity type is not provided, or if both date and until_date are provided.
        """
        if not activity_type:
            raise ValueError("Activity type is required.")

        if date and until_date:
            raise ValueError(
                "One or none of the Date and Until Date are required, not both."
            )

        url = f"{self.base_url}/account/activities/{activity_type}"

        params = {
            "date": date if date else None,
            "until_date": until_date if until_date else None,
        }

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        return [account_activity_class_from_dict(activity) for activity in response]

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

        url = f"{self.base_url}/account/portfolio/history"

        params = {
            "period": period,
            "timeframe": timeframe,
            "intraday_reporting": intraday_reporting,
        }

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        portfolio_df = pd.DataFrame(
            response,
            columns=[
                "timestamp",
                "equity",
                "profit_loss",
                "profit_loss_pct",
                "base_value",
            ],
        )

        timestamp_transformed = (
            pd.to_datetime(portfolio_df["timestamp"], unit="s")
            .dt.tz_localize("America/New_York")
            .dt.tz_convert("UTC")
            .apply(lambda x: x.date())
        )
        portfolio_df["timestamp"] = timestamp_transformed
        portfolio_df = portfolio_df.astype(
            {
                "equity": "float",
                "profit_loss": "float",
                "profit_loss_pct": "float",
                "base_value": "float",
            }
        )
        portfolio_df["profit_loss_pct"] = portfolio_df["profit_loss_pct"] * 100
        return portfolio_df
