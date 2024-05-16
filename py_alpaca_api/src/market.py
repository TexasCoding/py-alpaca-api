import json

import requests

from .data_classes import ClockClass, clock_class_from_dict


class Market:
    def __init__(self, trade_url: str, headers: object) -> None:
        """Initialize Market class

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

    ########################################################
    # \\\\\\\\\\\\\\\\\ Market Clock //////////////////////#
    ########################################################
    def clock(self) -> ClockClass:
        """Get market clock from Alpaca API

        Returns:
        ________
        ClockClass: Market clock status as a ClockClass object

        Raises:
        _______
        Exception: If the response is not successful

        Example:
        ________
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            clock = api.market.clock()
            print(clock)

        ClockClass(
            market_time="2021-07-08T18:18:08.182Z",
            is_open=True,
            next_open="2021-07-08T18:18:08.182Z",
            next_close="2021-07-08T18:18:08.182Z"
        )
        """  # noqa

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
