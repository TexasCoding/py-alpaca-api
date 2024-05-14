import json

import requests

from .data_classes import ClockClass, clock_class_from_dict


class Market:
    def __init__(self, trade_url: str, headers: object) -> None:
        self.trade_url = trade_url
        self.headers = headers

    ########################################################
    # \\\\\\\\\\\\\\\\\ Market Clock //////////////////////#
    ########################################################
    def clock(self) -> ClockClass:
        # Alpaca API URL for market clock
        url = f"{self.trade_url}/clock"
        # Get request to Alpaca API for market clock
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code == 200:
            # Return market clock status
            return clock_class_from_dict(json.loads(response.text))
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to get market clock. Response: {res["message"]}')
