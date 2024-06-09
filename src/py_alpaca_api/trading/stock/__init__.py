from typing import Dict
from py_alpaca_api.trading.market import Market
from py_alpaca_api.trading.stock.assets import Assets
from py_alpaca_api.trading.stock.history import History
from py_alpaca_api.trading.stock.screener import Screener


class Stock:
    def __init__(
        self, headers: Dict[str, str], base_url: str, data_url: str, market: Market
    ) -> None:
        self._initialize_components(
            headers=headers,
            base_url=base_url,
            data_url=data_url,
            market=market,
        )

    def _initialize_components(
        self,
        headers: Dict[str, str],
        base_url: str,
        data_url: str,
        market: Market,
    ):
        self.assets = Assets(headers=headers, base_url=base_url)
        self.history = History(headers=headers, data_url=data_url, asset=self.assets)
        self.screener = Screener(
            data_url=data_url, headers=headers, market=market, asset=self.assets
        )
