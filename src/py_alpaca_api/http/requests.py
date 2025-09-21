from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from ..exceptions import APIRequestError


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
        headers: dict[str, str] | None = None,
        params: dict[str, str | bool | float | int] | None = None,
        json: dict[str, Any] | None = None,
        raw_response: bool = False,
    ):
        """Execute HTTP request with retry logic.

        Args:
            method: A string representing the HTTP method to be used in the request.
            url: A string representing the URL to send the request to.
            headers: An optional dictionary containing the headers for the request.
            params: An optional dictionary containing the query parameters for the
                request.
            json: An optional dictionary containing the JSON payload for the request.
            raw_response: If True, return the raw response object without status checks.
                Defaults to False.

        Returns:
            The response object returned by the server.

        Raises:
            APIRequestError: If the response status code is not one of the
                acceptable statuses (200, 204, 207) and raw_response is False.
        """
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
        )

        # If raw_response is requested, return the response as-is
        if raw_response:
            return response

        acceptable_statuses = [200, 204, 207]
        if response.status_code not in acceptable_statuses:
            raise APIRequestError(
                status_code=response.status_code, message=response.text
            )
        return response
