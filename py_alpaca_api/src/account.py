import json
from typing import Dict

import pandas as pd
import pendulum
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

    def activity(self, activity_type: str, date: str = None, until_date: str = None) -> pd.DataFrame:
        """
        Retrieves account activities for a specific activity type.

        Args:
            activity_type (str): The type of activity to retrieve.
            date (str, optional): The starting date for the activities. Defaults to None.
            until_date (str, optional): The ending date for the activities. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing the account activities.

        Raises:
            ValueError: If activity_type is not provided.
            ValueError: If both date and until_date are provided or if neither is provided.
            Exception: If the request to retrieve account activities fails.
        """
        url = f"{self.trade_url}/account/activities/{activity_type}"

        if not activity_type:
            raise ValueError("Activity type is required.")

        if date and until_date or (not date and not until_date):
            raise ValueError("One of the Date and Until Date are required, not both or neither.")

        params = {
            "date": date if date else None,
            "until_date": until_date if until_date else None,
        }

        request = requests.get(url=url, headers=self.headers, params=params)

        if request.status_code != 200:
            raise Exception(f"Failed to get account activities. Response: {request.text}")

        response = json.loads(request.text)

        activity_df = pd.DataFrame()
        activity_df.assign(
            symbol="NAN",
            activity_type="NAN",
            id="NAN",
            cum_qty="NAN",
            leaves_qty="NAN",
            price="NAN",
            qty="NAN",
            side="NAN",
            transaction_time="NAN",
            order_id="NAN",
            type="NAN",
            order_status="NAN",
        )

        activity_df = pd.DataFrame(response).reset_index(drop=True)

        if activity_df.empty:
            return activity_df

        activity_df["transaction_time"] = (
            [pendulum.parse(x, tz="America/New_York").to_datetime_string() for x in activity_df["transaction_time"]]
            if "transaction_time" in activity_df.columns
            else None
        )

        activity_df = activity_df.astype(
            {
                "symbol": "str",
                "activity_type": "str",
                "id": "str",
                "cum_qty": "float",
                "leaves_qty": "float",
                "price": "float",
                "qty": "float",
                "side": "str",
                "transaction_time": "datetime64[ns, America/New_York]",
                "order_id": "str",
                "type": "str",
                "order_status": "str",
            }
        )

        return activity_df.sort_values(by="transaction_time", ascending=False)

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
