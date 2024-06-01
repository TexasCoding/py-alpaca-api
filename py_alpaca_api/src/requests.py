from typing import Dict, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class Requests:
    def __init__(self) -> None:
        self.retry_strategy = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.session = requests.Session()
        self.session.mount("https://", self.adapter)

    def _issue_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, str]] = None,
    ):
        """
        Args:
            method: A string representing the HTTP method to be used in the request.
            url: A string representing the URL to send the request to.
            headers: An optional dictionary containing the headers for the request.
            params: An optional dictionary containing the query parameters for the request.
            json: An optional dictionary containing the JSON payload for the request.

        Returns:
            The response object returned by the server.

        Raises:
            Exception: If the response status code is not one of the acceptable statuses (200, 204, 207).
        """
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
        )
        acceptable_statuses = [200, 204, 207]
        if response.status_code not in acceptable_statuses:
            raise Exception(f"Request Error: {response.text}")
        return response

    def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Union[Optional[Dict[str, str]], Optional[Dict[str, bool]], Optional[Dict[str, float]]] = None,
    ):
        """
        Args:
            url: A string representing the URL to make a GET request to.
            headers: An optional dictionary containing headers to include in the request.
            params: An optional dictionary containing query parameters to include in the request.

        Returns:
            The response from the GET request.
        """
        return self._issue_request("GET", url, headers=headers, params=params)

    def post(self, url: str, headers: Optional[Dict[str, str]] = None, payload: Optional[Dict[str, str]] = None):
        """
        Sends a POST request to the specified URL with optional headers and payload.

        Args:
            url (str): The URL to which the POST request will be sent.
            headers (Dict[str, str], optional): Dictionary of headers to include in the request. Defaults to None.
            payload (Dict[str, str], optional): Dictionary of data to be sent as the payload of the request. Defaults
            to None.

        Returns:
            The response of the POST request.
        """
        return self._issue_request("POST", url, headers=headers, json=payload)

    def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Union[Optional[Dict[str, str]], Optional[Dict[str, bool]], Optional[Dict[str, float]]] = None,
    ):
        """
        Args:
            url: The URL of the endpoint to send the DELETE request to.
            headers: (optional) A dictionary of headers to be included in the request.
            params: (optional) A dictionary of query string parameters to be included in the request.

        Returns:
            The response from the DELETE request.

        Raises:
            Any exceptions raised during the request.
        """
        return self._issue_request("DELETE", url, headers=headers, params=params)

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        json: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
    ):
        """
        Args:
            method: The HTTP method to use for the request (e.g., 'GET', 'POST', 'PUT', etc.).
            url: The URL to send the request to.
            headers: Optional. A dictionary of HTTP headers to include in the request.
            json: Optional. A dictionary of JSON data to include in the request body.
            params: Optional. A dictionary of query parameters to include in the request URL.

        Returns:
            The response from the server.
        """
        return self._issue_request(method, url, headers=headers, params=params, json=json)
