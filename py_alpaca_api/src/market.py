import json
from typing import Dict

import pandas as pd
import requests

from .data_classes import ClockClass, clock_class_from_dict


class Market:
    def __init__(self, trade_url: str, headers: Dict[str, str]) -> None:
        """
        Initialize the Trade class with the provided trade URL and headers.

        Args:
            trade_url (str): The URL for the trade.
            headers (dict[str, str]): The headers required for making the trade request.
        """
        self.trade_url = trade_url
        self.headers = headers

    ########################################################
    # \\\\\\\\\\\\\\\\ Get API Response ///////////////////#
    ########################################################
    @staticmethod
    def get_api_response(url: str, headers: Dict[str, str], params: Dict[str, str] = None) -> Dict:
        response = requests.get(url, headers=headers, params=params)
        data = json.loads(response.text)
        if response.status_code != 200:
            raise Exception(f'Failed to get data from API. Response: {data["message"]}')
        return data

    ########################################################
    # \\\\\\\\\\\\\\\\\ Market Calender ///////////////////#
    ########################################################
    def calender(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        This method retrieves calendar data for a given date range.

        Args:
            start_date (str): The start date of the calendar range in the format 'yyyy-mm-dd'.
            end_date (str): The end date of the calendar range in the format 'yyyy-mm-dd'.

        Returns:
            pd.DataFrame: A pandas DataFrame object containing the calendar data for the specified date range.
        """
        url = f"{self.trade_url}/calendar"
        params = {
            "start": start_date,
            "end": end_date,
        }

        data = self.get_api_response(url=url, headers=self.headers, params=params)
        data_df = pd.DataFrame(data).reset_index(drop=True)

        data_df["date"] = pd.to_datetime(data_df["date"])
        data_df["settlement_date"] = pd.to_datetime(data_df["settlement_date"])
        data_df["open"] = pd.to_datetime(data_df["open"], format="mixed").dt.time
        data_df["close"] = pd.to_datetime(data_df["close"], format="mixed").dt.time

        return data_df

    ########################################################
    # \\\\\\\\\\\\\\\\\ Market Clock //////////////////////#
    ########################################################
    def clock(self) -> ClockClass:
        """
        Returns the market clock status.
        Returns:
            ClockClass: The market clock status.
        Raises:
            Exception: If the request to Alpaca API for market clock is not successful.
        """
        url = f"{self.trade_url}/clock"
        data = self.get_api_response(url, self.headers)
        return clock_class_from_dict(data)
