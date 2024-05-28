import json
from typing import Dict, Union

import requests

from .data_classes import WatchlistClass, watchlist_class_from_dict


class Watchlist:
    def __init__(self, trade_url: str, headers: Dict[str, str]) -> None:
        """
        Initialize a Watchlist object.

        Args:
            trade_url (str): The URL for trading.
            headers (Dict[str, str]): The headers for API requests.

        Returns:
            None
        """
        self.trade_url = trade_url
        self.headers = headers

    ########################################################
    # ///////////// Helper functions //////////////////////#
    ########################################################
    @staticmethod
    def _handle_response(response: dict, no_content_msg: str) -> Union[WatchlistClass, str]:
        """
        Handles the response from the API and returns a WatchlistClass object
        if the response is not empty, otherwise returns the specified no_content_msg.

        Args:
            response (dict): The response from the API.
            no_content_msg (str): The message to return if the response is empty.

        Returns:
            Union[WatchlistClass, str]: The WatchlistClass object or the no_content_msg.
        """
        if response:
            return watchlist_class_from_dict(response)
        else:
            return no_content_msg

    ########################################################
    # ///////////// Send a request to the API //////////////#
    ########################################################
    def _request(self, method: str, url: str, payload: dict = None, params: dict = None) -> Dict:
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
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=payload,
            params=params,
        )
        if response.status_code in {200, 204}:
            if response.text:
                return json.loads(response.text)
            return {}
        else:
            raise Exception(response.text)

    ########################################################
    # //////////////// Get a  watchlist ///////////////////#
    ########################################################
    def get(self, watchlist_id: str = None, watchlist_name: str = None) -> WatchlistClass:
        """
        Retrieves a watchlist based on the provided watchlist ID or name.

        Args:
            watchlist_id (str, optional): The ID of the watchlist to retrieve.
            watchlist_name (str, optional): The name of the watchlist to retrieve.

        Returns:
            WatchlistClass: The retrieved watchlist.

        Raises:
            ValueError: If both watchlist_id and watchlist_name are provided, or if neither is provided.

        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if watchlist_id:
            url = f"{self.trade_url}/watchlists/{watchlist_id}"
        else:
            url = f"{self.trade_url}/watchlists:by_name"

        params = {"name": watchlist_name} if watchlist_name else None

        response = self._request(method="GET", url=url, params=params)
        return self._handle_response(response=response, no_content_msg="No watchlist was found.")

    ########################################################
    # ///////////// Get all watchlists ////////////////////#
    ########################################################
    def get_all(self) -> list[WatchlistClass]:
        """
        Retrieves all watchlists.

        Returns:
            A list of WatchlistClass objects representing all the watchlists.

        Raises:
            Exception: If the API request fails.
        """
        url = f"{self.trade_url}/watchlists"
        response = requests.get(url, headers=self.headers)
        res = json.loads(response.text)

        watchlists = []
        if response.status_code == 200:
            if res:
                for watchlist in res:
                    watchlists.append(self.get(watchlist_id=watchlist["id"]))
            return watchlists
        else:
            raise Exception(response.text)

    ########################################################
    # ///////////// Create a new watchlist ////////////////#
    ########################################################
    def create(self, name: str, symbols: str = "") -> WatchlistClass:
        """
        Creates a new watchlist with the given name and symbols.

        Args:
            name (str): The name of the watchlist.
            symbols (str, optional): A comma-separated string of symbols to add to the watchlist. Defaults to "".

        Returns:
            WatchlistClass: The created watchlist.

        Raises:
            SomeException: An exception that may occur during the request.

        """
        # Create the URL
        url = f"{self.trade_url}/watchlists"
        # Split the symbols and remove any spaces
        symbols = symbols.replace(" ", "").split(",") if symbols else []

        payload = {"symbols": symbols, "name": name}
        response = self._request(method="POST", url=url, payload=payload)
        return self._handle_response(response=response, no_content_msg="The watchlist was not created.")

    ########################################################
    # ///////////// Update a watchlist ////////////////////#
    ########################################################
    def update(
        self,
        watchlist_id: str = None,
        watchlist_name: str = None,
        name: str = "",
        symbols: str = "",
    ) -> WatchlistClass:
        """
        Update a watchlist with the specified parameters.

        Args:
            watchlist_id (str, optional): The ID of the watchlist to update. Either `watchlist_id` or `watchlist_name` must be provided.
            watchlist_name (str, optional): The name of the watchlist to update. Either `watchlist_id` or `watchlist_name` must be provided.
            name (str, optional): The new name for the watchlist. If not provided, the existing name will be used.
            symbols (str, optional): A comma-separated string of symbols to update the watchlist with. If not provided, the existing symbols
            will be used.

        Returns:
            WatchlistClass: The updated watchlist.

        Raises:
            ValueError: If both `watchlist_id` and `watchlist_name` are provided, or if neither `watchlist_id` nor `watchlist_name` are provided.

        """

        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")
        # Check if watchlist_id is provided
        if watchlist_id:
            watchlist = self.get(watchlist_id=watchlist_id)
            url = f"{self.trade_url}/watchlists/{watchlist_id}"
        else:
            watchlist = self.get(watchlist_name=watchlist_name)
            url = f"{self.trade_url}/watchlists:by_name"

        name = name if name else watchlist.name

        if symbols != "":
            symbols = symbols.replace(" ", "").split(",")
        else:
            symbols = ",".join([o.symbol for o in watchlist.assets])

        payload = {"name": name, "symbols": symbols}
        params = {"name": watchlist_name} if watchlist_name else None

        response = self._request(method="PUT", url=url, payload=payload, params=params)
        return self._handle_response(response=response, no_content_msg="The watchlist was not updated.")

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
            url = f"{self.trade_url}/watchlists/{watchlist_id}"
        else:
            url = f"{self.trade_url}/watchlists:by_name"

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
    ) -> WatchlistClass:
        """
        Adds an asset to a watchlist.

        Args:
            watchlist_id (str, optional): The ID of the watchlist to add the asset to. If not provided, the watchlist_name
            parameter must be provided. watchlist_name (str, optional): The name of the watchlist to add the asset to. If not provided,
            the watchlist_id parameter must be provided. symbol (str): The symbol of the asset to add to the watchlist.

        Returns:
            WatchlistClass: The updated watchlist object.

        Raises:
            ValueError: If both watchlist_id and watchlist_name are provided, or if symbol is not provided.
        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if not symbol:
            raise ValueError("Symbol is required")

        if watchlist_id:
            url = f"{self.trade_url}/watchlists/{watchlist_id}"
        else:
            url = f"{self.trade_url}/watchlists:by_name"

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
    ) -> WatchlistClass:
        """
        Removes an asset from a watchlist.

        Args:
            watchlist_id (str, optional): The ID of the watchlist. If not provided, the watchlist_name parameter will be used to
            retrieve the ID. Defaults to None.
            watchlist_name (str, optional): The name of the watchlist. If not provided, thewatchlist_id parameter will be used to
            retrieve the ID. Defaults to None.
            symbol (str): The symbol of the asset to be removed from the watchlist.

        Returns:
            WatchlistClass: The updated watchlist object.

        Raises:
            ValueError: If both watchlist_id and watchlist_name are provided, or if symbol is not provided.
        """
        if watchlist_id and watchlist_name or (not watchlist_id and not watchlist_name):
            raise ValueError("Watchlist ID or Name is required, not both.")

        if not symbol:
            raise ValueError("Symbol is required")

        if not watchlist_id:
            watchlist_id = self.get(watchlist_name=watchlist_name).id

        url = f"{self.trade_url}/watchlists/{watchlist_id}/{symbol}"

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
            watchlist_id (str, optional): The ID of the watchlist. Either `watchlist_id` or `watchlist_name` should be provided,
            not both. Defaults to None.
            watchlist_name (str, optional): The name of the watchlist. Either `watchlist_id` or `watchlist_name` should be
            provided, not both. Defaults to None.

        Returns:
            list: A list of symbols of assets in the watchlist.

        Raises:
            ValueError: If both `watchlist_id` and `watchlist_name` are provided, or if neither `watchlist_id` nor `watchlist_name` are provided.
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
