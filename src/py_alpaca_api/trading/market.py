import json
from typing import Dict

import pandas as pd

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.clock_model import ClockModel, clock_class_from_dict


class Market:
    def __init__(self, base_url: str, headers: Dict[str, str]) -> None:
        self.base_url = base_url
        self.headers = headers

    def clock(self) -> ClockModel:
        """
        Retrieves the current market clock.

        Returns:
            ClockModel: A model containing the current market clock data.
        """
        url = f"{self.base_url}/clock"
        response = json.loads(
            Requests().request(method="GET", url=url, headers=self.headers).text
        )
        response["market_time"] = response["timestamp"]
        del response["timestamp"]
        return clock_class_from_dict(response)

    def calendar(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Retrieves the market calendar for the specified date range.

        Args:
            start_date (str): The start date of the calendar range in the format "YYYY-MM-DD".
            end_date (str): The end date of the calendar range in the format "YYYY-MM-DD".

        Returns:
            pd.DataFrame: A DataFrame containing the market calendar data, with columns for the date, settlement date, open time, and close time.
        """

        url = f"{self.base_url}/calendar"
        params = {"start": start_date, "end": end_date}
        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        calendar_df = pd.DataFrame(response).reset_index(drop=True)

        date_cols = ["date", "settlement_date"]
        time_cols = ["open", "close"]

        for col in date_cols:
            calendar_df[col] = pd.to_datetime(calendar_df[col])

        for col in time_cols:
            calendar_df[col] = pd.to_datetime(calendar_df[col], format="mixed").dt.time

        return calendar_df
