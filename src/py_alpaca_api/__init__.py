from .exceptions import AuthenticationError
from .stock import Stock
from .streaming import StreamClient
from .trading import Trading


class PyAlpacaAPI:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True) -> None:
        if not api_key or not api_secret:
            raise AuthenticationError()
        # Store credentials for streaming
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_paper = api_paper
        self._initialize_components(
            api_key=api_key, api_secret=api_secret, api_paper=api_paper
        )

    def _initialize_components(
        self, api_key: str, api_secret: str, api_paper: bool = True
    ):
        self.trading = Trading(
            api_key=api_key, api_secret=api_secret, api_paper=api_paper
        )
        self.stock = Stock(
            api_key=api_key,
            api_secret=api_secret,
            api_paper=api_paper,
            market=self.trading.market,
        )

    def create_stream_client(self, feed: str = "iex") -> StreamClient:
        """Create a new streaming client for real-time market data.

        Args:
            feed: Data feed to use (iex, sip, otc). Defaults to "iex".

        Returns:
            StreamClient instance for real-time data streaming.
        """
        return StreamClient(
            api_key=self.api_key,
            api_secret=self.api_secret,
            feed=feed,
            paper=self.api_paper,
        )
