from .account import Account


class Trading:
    def __init__(self, api_key: str, api_secret: str, api_paper: bool = True) -> None:
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": api_secret,
        }
        self.base_url = (
            "https://paper-api.alpaca.markets/v2"
            if api_paper
            else "https://api.alpaca.markets/v2"
        )
        self._initialize_components()

    def _initialize_components(self):
        self.account = Account(headers=self.headers, base_url=self.base_url)
