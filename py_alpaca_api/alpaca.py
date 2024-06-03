from .src.account import Account
from .src.asset import Asset
from .src.history import History
from .src.market import Market
from .src.order import Order
from .src.position import Position
from .src.predictor import Predictor
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

        # Check API Key and Secret
        self._validate_api_key_and_secret(api_key, api_secret)

        # Set Headers
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
        }

        # Set URLs
        self.data_url = "https://data.alpaca.markets/v2"
        self.trade_url = self._set_trade_url(api_paper)

        # Initialize Components
        self._initialize_components()

    @staticmethod
    def _validate_api_key_and_secret(api_key: str, api_secret: str):
        if not api_key:
            raise ValueError("API Key is required")
        if not api_secret:
            raise ValueError("API Secret is required")

    @staticmethod
    def _set_trade_url(api_paper: bool):
        return "https://paper-api.alpaca.markets/v2" if api_paper else "https://api.alpaca.markets/v2"

    def _initialize_components(self):
        self.account = Account(trade_url=self.trade_url, headers=self.headers)
        self.asset = Asset(trade_url=self.trade_url, headers=self.headers)
        self.history = History(data_url=self.data_url, headers=self.headers, asset=self.asset)
        self.position = Position(trade_url=self.trade_url, headers=self.headers, account=self.account)
        self.order = Order(trade_url=self.trade_url, headers=self.headers)
        self.market = Market(trade_url=self.trade_url, headers=self.headers)
        self.watchlist = Watchlist(trade_url=self.trade_url, headers=self.headers)
        self.screener = Screener(data_url=self.data_url, headers=self.headers, asset=self.asset, market=self.market)
        self.predictor = Predictor(history=self.history, screener=self.screener)
