from .src.account import Account
from .src.asset import Asset
from .src.history import History
from .src.market import Market
from .src.order import Order
from .src.position import Position
from .src.screener import Screener
from .src.watchlist import Watchlist


# PyAlpacaApi class
class PyAlpacaApi:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True):
        """
        Initializes an instance of the Alpaca class.

        Args:
            api_key (str): The API key for accessing the Alpaca API.
            api_secret (str): The API secret for accessing the Alpaca API.
            api_paper (bool, optional): Specifies whether to use the Alpaca paper trading API.
                Defaults to True.

        Raises:
            ValueError: If the API key or API secret is not provided.
        """
        if not api_key:
            raise ValueError("API Key is required")
        if not api_secret:
            raise ValueError("API Secret is required")

        # Set the API Key and Secret
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
        }

        # Set the API URL's
        if api_paper:
            self.trade_url = "https://paper-api.alpaca.markets/v2"
        else:
            self.trade_url = "https://api.alpaca.markets/v2"

        self.data_url = "https://data.alpaca.markets/v2"

        self.account = Account(trade_url=self.trade_url, headers=self.headers)
        self.asset = Asset(trade_url=self.trade_url, headers=self.headers)
        self.history = History(data_url=self.data_url, headers=self.headers, asset=self.asset)
        self.position = Position(
            trade_url=self.trade_url,
            headers=self.headers,
            account=self.account,
        )
        self.order = Order(trade_url=self.trade_url, headers=self.headers)
        self.market = Market(trade_url=self.trade_url, headers=self.headers)
        self.watchlist = Watchlist(trade_url=self.trade_url, headers=self.headers)
        self.screener = Screener(
            data_url=self.data_url,
            headers=self.headers,
            asset=self.asset,
            market=self.market,
        )
