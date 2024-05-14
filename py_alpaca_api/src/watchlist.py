# import json

# import requests


class Watchlist:
    def __init__(self, trade_url: str, headers: object) -> None:
        self.trade_url = trade_url
        self.headers = headers
