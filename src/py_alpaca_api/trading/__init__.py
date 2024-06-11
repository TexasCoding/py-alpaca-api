from typing import Dict
from py_alpaca_api.trading.market import Market
from py_alpaca_api.trading.news import News
from py_alpaca_api.trading.positions import Positions

# from py_alpaca_api.trading.stock import Stock
from py_alpaca_api.trading.account import Account
from py_alpaca_api.trading.orders import Orders
from py_alpaca_api.trading.recommendations import Recommendations
from py_alpaca_api.trading.watchlists import Watchlist


class Trading:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool) -> None:
        headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
        }
        base_url = (
            "https://paper-api.alpaca.markets/v2"
            if api_paper
            else "https://api.alpaca.markets/v2"
        )
        self._initialize_components(headers=headers, base_url=base_url)

    def _initialize_components(self, headers: Dict[str, str], base_url: str):
        self.account = Account(headers=headers, base_url=base_url)
        self.market = Market(headers=headers, base_url=base_url)
        self.positions = Positions(
            headers=headers, base_url=base_url, account=self.account
        )
        self.orders = Orders(headers=headers, base_url=base_url)
        self.watchlists = Watchlist(headers=headers, base_url=base_url)
        self.news = News(headers=headers)
        self.recommendations = Recommendations()
