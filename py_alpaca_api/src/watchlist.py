import json

import requests

from .data_classes import watchlist_class_from_dict


class Watchlist:
    def __init__(self, trade_url: str, headers: object) -> None:
        self.trade_url = trade_url
        self.headers = headers

    def get(self, watchlist_id: str = None, watchlist_name: str = None) -> watchlist_class_from_dict:

        if watchlist_id and watchlist_name:
            raise ValueError("Watchlist ID or Name is required, not both.")

        if watchlist_id:
            url = f"{self.trade_url}/watchlists/{watchlist_id}"

            response = requests.get(url, headers=self.headers)
        elif watchlist_name:
            url = f"{self.trade_url}/watchlists:by_name"
            params = {"name": watchlist_name}
            response = requests.get(url, headers=self.headers, params=params)
        else:
            raise ValueError("Watchlist ID or Name is required")

        res = json.loads(response.text)

        if response.status_code == 200:
            return watchlist_class_from_dict(res)
        else:
            raise Exception(response.text)

    def get_all(self) -> object:
        """Get all watchlists

        Returns:
        --------
        object: List of WatchlistClass objects

        Example:
        --------
        >>> from py_alpaca_api.alpaca import PyAlpacaApi
        >>> alpaca = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
        >>> alpaca.watchlist.get_all()
        [  WatchlistClass(
                id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
                account_id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
                name='asdf',
                assets=[],
                created_at='2021-09-21T16:39:52.000000Z',
                updated_at='2021-09-21T16:39:52.000000Z'
            ),
            WatchlistClass(
                id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
                account_id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
                name='asdf',
                assets=[],
                created_at='2021-09-21T16:39:52.000000Z',
                updated_at='2021-09-21T16:39:52.000000Z'
            )
        ]
        """  # noqa

        url = f"{self.trade_url}/watchlists"

        response = requests.get(url, headers=self.headers)

        res = json.loads(response.text)

        watchlists = []
        for watchlist in res:
            watchlists.append(self.get(watchlist_id=watchlist["id"]))

        if response.status_code == 200:
            return watchlists if response.text else []
        else:
            raise Exception(response.text)

    ########################################################
    # ///////////// Create a new watchlist /////////////////#
    ########################################################
    def create(self, name: str, symbols: str = "") -> watchlist_class_from_dict:
        """Create a new watchlist

        Parameters:
        -----------
        name: str
            Watchlist name

        symbols: str
            Comma separated list of symbols, e.g. "AAPL, EVH" (default: "") optional

        Returns:
        --------
        watchlist_class_from_dict: object
            WatchlistClass object

        Example:
        --------
        >>> from py_alpaca_api.alpaca import PyAlpacaApi
        >>> alpaca = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
        >>> alpaca.watchlist.create(name='asdf', symbols="AAPL, EVH")
        WatchlistClass(
            id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
            account_id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
            name='asdf',
            assets=AssetClass(
                id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
                asset_class='us_equity',
                exchange='NASDAQ',
                symbol='AAPL',
                status='active',
                tradable=True,
                marginable=True,
                shortable=True,
                easy_to_borrow=True,
                fractionable=True
            ),
            AssetClass(
                id='d0c6a0e9-9d6d-4b0a-bd2c-375b0e0b5e3d',
                asset_class='us_equity',
                exchange='NASDAQ',
                symbol='EVH',
                status='active',
                tradable=True,
                marginable=True,
                shortable=True,
                easy_to_borrow=True,
                fractionable=True
            ),
            created_at='2021-09-21T16:39:52.000000Z',
            updated_at='2021-09-21T16:39:52.000000Z'
        )
        """  # noqa
        # Create the URL
        url = f"{self.trade_url}/watchlists"
        # Split the symbols and remove any spaces
        symbols = symbols.replace(" ", "").split(",")
        # Create the payload
        payload = {"symbols": symbols, "name": name}
        # Send the request
        response = requests.post(url, headers=self.headers, json=payload)
        # Check the response, if 200 return the WatchlistClass object
        if response.status_code == 200:
            return watchlist_class_from_dict(json.loads(response.text))
        # Otherwise raise an exception
        else:
            raise Exception(response.text)

    def update(self, watchlist_id: str = None, watchlist_name: str = None, symbols: object = []) -> object:
        pass

    def delete(self, watchlist_id: str = None, watchlist_name: str = None) -> object:
        pass

    def add_asset(self, watchlist_id: str = None, watchlist_name: str = None, symbol: str = "") -> object:
        pass

    def remove_asset(self, watchlist_id: str = None, watchlist_name: str = None, symbol: str = "") -> object:
        pass
