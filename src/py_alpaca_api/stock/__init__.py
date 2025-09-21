from py_alpaca_api.stock.assets import Assets
from py_alpaca_api.stock.auctions import Auctions
from py_alpaca_api.stock.history import History
from py_alpaca_api.stock.latest_quote import LatestQuote
from py_alpaca_api.stock.logos import Logos
from py_alpaca_api.stock.metadata import Metadata
from py_alpaca_api.stock.predictor import Predictor
from py_alpaca_api.stock.quotes import Quotes
from py_alpaca_api.stock.screener import Screener
from py_alpaca_api.stock.snapshots import Snapshots
from py_alpaca_api.stock.trades import Trades
from py_alpaca_api.trading.market import Market


class Stock:
    def __init__(
        self, api_key: str, api_secret: str, api_paper: bool, market: Market
    ) -> None:
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
        data_url = "https://data.alpaca.markets/v2"
        self._initialize_components(
            headers=headers, base_url=base_url, data_url=data_url, market=market
        )

    def _initialize_components(
        self,
        headers: dict[str, str],
        base_url: str,
        data_url: str,
        market: Market,
    ):
        self.assets = Assets(headers=headers, base_url=base_url)
        self.auctions = Auctions(headers=headers)
        self.history = History(headers=headers, data_url=data_url, asset=self.assets)
        self.logos = Logos(headers=headers)
        self.quotes = Quotes(headers=headers)
        self.screener = Screener(
            data_url=data_url, headers=headers, market=market, asset=self.assets
        )
        self.predictor = Predictor(history=self.history, screener=self.screener)
        self.latest_quote = LatestQuote(headers=headers)
        self.metadata = Metadata(headers=headers)
        self.snapshots = Snapshots(headers=headers)
        self.trades = Trades(headers=headers)
