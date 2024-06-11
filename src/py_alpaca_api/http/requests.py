from typing import Dict, Optional

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

    def request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str] | Dict[str, bool] | Dict[str, float]] = None,
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
