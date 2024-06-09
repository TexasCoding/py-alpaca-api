from typing import Dict
from py_alpaca_api.trading.market import Market
from py_alpaca_api.trading.positions import Positions
from py_alpaca_api.trading.stock import Stock
from py_alpaca_api.trading.account import Account


class Trading:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True) -> None:
        headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
        }
        base_url = (
            "https://paper-api.alpaca.markets/v2"
            if api_paper
            else "https://api.alpaca.markets/v2"
        )
        data_url = "https://data.alpaca.markets/v2"
        self._initialize_components(
            headers=headers, base_url=base_url, data_url=data_url
        )

    def _initialize_components(
        self, headers: Dict[str, str], base_url: str, data_url: str
    ):
        self.account = Account(headers=headers, base_url=base_url)
        self.market = Market(headers=headers, base_url=base_url)
        self.stock = Stock(
            headers=headers, base_url=base_url, data_url=data_url, market=self.market
        )
        self.positions = Positions(
            headers=headers, base_url=base_url, account=self.account
        )
