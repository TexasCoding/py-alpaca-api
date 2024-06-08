from typing import Dict
from py_alpaca_api.trading.stock.assets import Assets
from py_alpaca_api.trading.stock.history import History


class Stock:
    def __init__(self, headers: Dict[str, str], base_url: str, data_url: str) -> None:
        self._initialize_components(
            headers=headers, base_url=base_url, data_url=data_url
        )

    def _initialize_components(
        self, headers: Dict[str, str], base_url: str, data_url: str = ""
    ):
        self.assets = Assets(headers=headers, base_url=base_url)
        self.history = History(headers=headers, data_url=data_url, asset=self.assets)
