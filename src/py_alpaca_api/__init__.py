from .trading import Trading


class PyAlpacaAPI:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_paper = api_paper
        if not api_key or not api_secret:
            raise Exception("API Key and Secret are required")
        self._initialize_components()

    def _initialize_components(self):
        self.trading = Trading(
            api_key=self.api_key, api_secret=self.api_secret, api_paper=self.api_paper
        )
