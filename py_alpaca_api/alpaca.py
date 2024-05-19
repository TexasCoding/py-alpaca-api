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
        """Initialize PyAlpacaApi class

        Parameters:
        -----------
        api_key:    Alpaca API Key
                    A valid Alpaca API Key string required

        api_secret: Alpaca API Secret
                    A valid Alpaca API Secret string required

        api_paper:  Alpaca Paper Trading
                    Alpaca Paper Trading (default: True) bool

        Raises:
        -------
        ValueError:
            ValueError if API Key is not provided

        ValueError:
            ValueError if API Secret is not provided

        Example:
        --------
        >>> PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
        PyAlpacaApi()
        """  # noqa

        # Check if API Key and Secret are provided
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
        self.screener = Screener(data_url=self.data_url, headers=self.headers, asset=self.asset)
