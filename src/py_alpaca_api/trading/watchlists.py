import json
from typing import Dict, Union

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.watchlist_model import (
    WatchlistModel,
    watchlist_class_from_dict,
)


class Watchlist:
    def __init__(self, base_url: str, headers: Dict[str, str]) -> None:
        """
        Initialize a Watchlist object.

        Args:
            base_url (str): The URL for trading.
            headers (Dict[str, str]): The headers for API requests.

        Returns:
            None
        """
        self.base_url = base_url
        self.headers = headers

    ########################################################
    # ///////////// Helper functions //////////////////////#
    ########################################################
    @staticmethod
    def _handle_response(
        response: dict, no_content_msg: str
    ) -> Union[WatchlistModel, str]:
        """
        Handles the response from the API and returns a WatchlistModel object
        if the response is not empty, otherwise returns the specified no_content_msg.

        Args:
            response (dict): The response from the API.
            no_content_msg (str): The message to return if the response is empty.

        Returns:
            Union[WatchlistModel, str]: The WatchlistModel object or the no_content_msg.
        """
        if response:
            return watchlist_class_from_dict(response)
        else:
            return no_content_msg

    ########################################################
    # ///////////// Send a request to the API //////////////#
    ########################################################
    def _request(
        self, method: str, url: str, payload: dict = None, params: dict = None
    ) -> Dict:
        """
        Sends a request to the specified URL using the specified HTTP method.

        Args:
            method (str): The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            url (str): The URL to send the request to.
            payload (dict, optional): The payload to include in the request body. Defaults to None.
            params (dict, optional): The query parameters to include in the request URL. Defaults to None.

        Returns:
            dict: The response data as a dictionary.

        Raises:
            Exception: If the response status code is not 200 or 204.
        """
        response = Requests().request(
            method=method,
            url=url,
            headers=self.headers,
            json=payload,
            params=params,
        )

        if response.text:
            return json.loads(response.text)
        return {}

    ########################################################
    # //////////////// Get a  watchlist ///////////////////#
    ########################################################
    def get(
        self, watchlist_id: str = None, watchlist_name: str = None
    ) -> WatchlistModel:
        """
        Retrieves a watchlist based on the provided watchlist ID or name.

        Args:
            watchlist_id (str, optional): The ID of the watchlist to retrieve.
            watchlist_name (str, optional): The name of the watchlist to retrieve.

        Returns:
            WatchlistModel: The retrieved watchlist.

        Raises:
            ValueError: If both watchlist_id and watchlist_name are provided, or if neither is provided.

        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if watchlist_id:
            url = f"{self.base_url}/watchlists/{watchlist_id}"
        else:
            url = f"{self.base_url}/watchlists:by_name"

        params = {"name": watchlist_name} if watchlist_name else None

        response = self._request(method="GET", url=url, params=params)
        return self._handle_response(
            response=response, no_content_msg="No watchlist was found."
        )

    ########################################################
    # ///////////// Get all watchlists ////////////////////#
    ########################################################
    def get_all(self) -> list[WatchlistModel]:
        """
        Retrieves all watchlists.

        Returns:
            A list of WatchlistModel objects representing all the watchlists.

        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.base_url}/watchlists"

        response = json.loads(
            Requests().request(method="GET", url=url, headers=self.headers).text
        )

        watchlists = []
        if response:
            for watchlist in response:
                watchlists.append(self.get(watchlist_id=watchlist["id"]))
        return watchlists

    ########################################################
    # ///////////// Create a new watchlist ////////////////#
    ########################################################
    def create(self, name: str, symbols: Union[list, str] = None) -> WatchlistModel:
        """
        Creates a new watchlist with the given name and symbols.

        Args:
            name (str): The name of the watchlist.
            symbols (str, optional): A comma-separated string of symbols to add to the watchlist. Defaults to "".

        Returns:
            WatchlistModel: The created watchlist.

        Raises:
            SomeException: An exception that may occur during the request.

        """
        # Create the URL
        url = f"{self.base_url}/watchlists"
        # Split the symbols and remove any spaces
        if isinstance(symbols, str):
            symbols = symbols.replace(" ", "").split(",")

        payload = {"symbols": symbols, "name": name}
        response = self._request(method="POST", url=url, payload=payload)
        return self._handle_response(
            response=response, no_content_msg="The watchlist was not created."
        )

    ########################################################
    # ///////////// Update a watchlist ////////////////////#
    ########################################################
    def update(
        self,
        watchlist_id: str = None,
        watchlist_name: str = None,
        name: str = "",
        symbols: Union[list, str] = None,
    ) -> WatchlistModel:
        """
        Update a watchlist with the specified parameters.

        Args:
            watchlist_id (str, optional): The ID of the watchlist to update. Either `watchlist_id` or `watchlist_name`
            must be provided.
            watchlist_name (str, optional): The name of the watchlist to update. Either `watchlist_id` or
            `watchlist_name` must be provided.
            name (str, optional): The new name for the watchlist. If not provided, the existing name will be used.
            symbols (str, optional): A comma-separated string of symbols to update the watchlist with. If not provided,
             the existing symbols
            will be used.

        Returns:
            WatchlistModel: The updated watchlist.

        Raises:
            ValueError: If both `watchlist_id` and `watchlist_name` are provided, or if neither `watchlist_id` nor
            `watchlist_name` are provided.

        """

        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")
        # Check if watchlist_id is provided
        if watchlist_id:
            watchlist = self.get(watchlist_id=watchlist_id)
            url = f"{self.base_url}/watchlists/{watchlist_id}"
        else:
            watchlist = self.get(watchlist_name=watchlist_name)
            url = f"{self.base_url}/watchlists:by_name"

        name = name if name else watchlist.name

        if isinstance(symbols, str):
            symbols = symbols.replace(" ", "").split(",")
        elif isinstance(symbols, list):
            symbols = symbols
        else:
            symbols = ",".join([o.symbol for o in watchlist.assets])

        payload = {"name": name, "symbols": symbols}
        params = {"name": watchlist_name} if watchlist_name else None

        response = self._request(method="PUT", url=url, payload=payload, params=params)
        return self._handle_response(
            response=response, no_content_msg="The watchlist was not updated."
        )

    ########################################################
    # ///////////// Delete a watchlist ////////////////////#
    ########################################################
    def delete(self, watchlist_id: str = None, watchlist_name: str = None) -> str:
        """
        Deletes a watchlist.

        Args:
            watchlist_id (str, optional): The ID of the watchlist to delete.
            watchlist_name (str, optional): The name of the watchlist to delete.

        Returns:
            str: A message indicating the successful deletion of the watchlist.

        Raises:
            ValueError: If both watchlist_id and watchlist_name are provided or if neither is provided.

        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if watchlist_id:
            url = f"{self.base_url}/watchlists/{watchlist_id}"
        else:
            url = f"{self.base_url}/watchlists:by_name"

        params = {"name": watchlist_name} if watchlist_name else None

        response = self._request(method="DELETE", url=url, params=params)
        return self._handle_response(
            response=response,
            no_content_msg=f"Watchlist {watchlist_id if watchlist_id else watchlist_name} deleted successfully.",
        )

    ########################################################
    # ///////////// Add Asset to  watchlist ///////////////#
    ########################################################
    def add_asset(
        self,
        watchlist_id: str = None,
        watchlist_name: str = None,
        symbol: str = "",
    ) -> WatchlistModel:
        """
        Adds an asset to a watchlist.

        Args:
            watchlist_id (str): The ID of the watchlist to add the asset to. If `watchlist_id` is provided,
            `watchlist_name` should be None.
            watchlist_name (str): The name of the watchlist to add the asset to. If `watchlist_name` is provided,
            `watchlist_id` should be None.
            symbol (str): The symbol of the asset to add to the watchlist.

        Returns:
            WatchlistModel: The updated watchlist after adding the asset.

        Raises:
            ValueError: If both `watchlist_id` and `watchlist_name` are provided or neither is provided.
            ValueError: If `symbol` is not provided.

        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if not symbol:
            raise ValueError("Symbol is required")

        if watchlist_id:
            url = f"{self.base_url}/watchlists/{watchlist_id}"
        else:
            url = f"{self.base_url}/watchlists:by_name"

        params = {"name": watchlist_name} if watchlist_name else None
        payload = {"symbol": symbol}

        response = self._request(method="POST", url=url, payload=payload, params=params)
        return self._handle_response(
            response=response,
            no_content_msg="Failed to add asset to watchlist.",
        )

    ########################################################
    # /////////// Remove a Asset from  watchlist //////////#
    ########################################################
    def remove_asset(
        self,
        watchlist_id: str = None,
        watchlist_name: str = None,
        symbol: str = "",
    ) -> WatchlistModel:
        """
        Removes an asset from a watchlist.

        Args:
            watchlist_id (str, optional): The ID of the watchlist. If not provided, the watchlist_name parameter
            will be used to
            retrieve the ID. Defaults to None.
            watchlist_name (str, optional): The name of the watchlist. If not provided, thewatchlist_id parameter
             will be used to
            retrieve the ID. Defaults to None.
            symbol (str): The symbol of the asset to be removed from the watchlist.

        Returns:
            WatchlistModel: The updated watchlist object.

        Raises:
            ValueError: If both watchlist_id and watchlist_name are provided, or if symbol is not provided.
        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if not symbol:
            raise ValueError("Symbol is required")

        if not watchlist_id:
            watchlist_id = self.get(watchlist_name=watchlist_name).id

        url = f"{self.base_url}/watchlists/{watchlist_id}/{symbol}"

        response = self._request(method="DELETE", url=url)
        return self._handle_response(
            response=response,
            no_content_msg="Failed to remove asset from watchlist.",
        )

    ########################################################
    # /////////// Get Assets from a watchlist /////////////#
    ########################################################
    def get_assets(self, watchlist_id: str = None, watchlist_name: str = None) -> list:
        """
        Retrieves the symbols of assets in a watchlist.

        Args:
            watchlist_id (str, optional): The ID of the watchlist. Either `watchlist_id` or `watchlist_name`
             should be provided,
            not both. Defaults to None.
            watchlist_name (str, optional): The name of the watchlist. Either `watchlist_id` or `watchlist_name`
             should be
            provided, not both. Defaults to None.

        Returns:
            list: A list of symbols of assets in the watchlist.

        Raises:
            ValueError: If both `watchlist_id` and `watchlist_name` are provided, or if neither `watchlist_id` nor
            `watchlist_name` are provided.
        """

        if watchlist_id and watchlist_name:
            raise ValueError("Watchlist ID or Name is required, not both.")

        if watchlist_id:
            watchlist = self.get(watchlist_id=watchlist_id)
        elif watchlist_name:
            watchlist = self.get(watchlist_name=watchlist_name)
        else:
            raise ValueError("Watchlist ID or Name is required")

        symbols = [o.symbol for o in watchlist.assets]

        return symbols
