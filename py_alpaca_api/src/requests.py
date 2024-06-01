from typing import Dict

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
        self.session.mount("http://", self.adapter)

    def get(
        self,
        url: str,
        headers: Dict[str, str] = None,
        params: Dict[str, str] = None,
    ):
        response = self.session.get(url=url, headers=headers, params=params)
        if response.status_code not in [200, 204]:
            raise Exception(f"Request Error: {response.text}")

        return response

    def post(
        self,
        url: str,
        headers: Dict[str, str] = None,
        payload: Dict[str, str] = None,
    ):
        response = self.session.post(url=url, headers=headers, json=payload)
        if response.status_code not in [200, 204]:
            raise Exception(f"Request Error: {response.text}")

        return response

    def delete(
        self,
        url: str,
        headers: Dict[str, str] = None,
        params: Dict[str, str] = None,
    ):
        response = self.session.delete(url=url, headers=headers, params=params)
        if response.status_code not in [200, 204, 207]:
            raise Exception(f"Request Error: {response.text}")

        return response

    def request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str] = None,
        json: Dict[str, str] = None,
        params: Dict[str, str] = None,
    ):
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json,
        )
        if response.status_code not in [200, 204, 207]:
            raise Exception(f"Request Error: {response.text}")

        return response
