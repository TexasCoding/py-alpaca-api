import json
from typing import Dict, List, Optional

import pendulum

from py_alpaca_api.http.requests import Requests


class LatestQuote:
    def __init__(self, headers: Dict[str, str]) -> None:
        self.headers = headers

    def get(
        self,
        symbol: Optional[List[str] | str],
        feed: str = "iex",
        currency: str = "USD",
    ) -> dict:
        url = "https://data.alpaca.markets/v2/stocks/quotes/latest"

        params = {"symbols": symbol, "feed": feed, "currency": currency}

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        quotes = []

        for key, value in response["quotes"].items():
            quotes.append(
                {
                    "symbol": key,
                    "timestamp": pendulum.parse(
                        value["t"], tz="America/New_York"
                    ).to_datetime_string(),
                    "ask": value["ap"],
                    "ask_size": value["as"],
                    "bid": value["bp"],
                    "bid_size": value["bs"],
                }
            )

        print(quotes)
