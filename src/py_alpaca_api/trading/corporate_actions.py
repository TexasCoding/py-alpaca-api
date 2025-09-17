import json
from datetime import datetime
from typing import Literal

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.corporate_action_model import (
    CorporateActionModel,
    corporate_action_class_from_dict,
)


class CorporateActions:
    def __init__(self, headers: dict[str, str], base_url: str) -> None:
        self.headers = headers
        self.base_url = base_url

    def get_announcements(
        self,
        since: str,
        until: str,
        ca_types: list[str],
        symbol: str | None = None,
        cusip: str | None = None,
        date_type: Literal["declaration_date", "ex_date", "record_date", "payable_date"]
        | None = None,
        page_limit: int = 100,
        page_token: str | None = None,
    ) -> list[CorporateActionModel]:
        """Retrieve corporate action announcements.

        Args:
            since: The start (inclusive) of the date range in YYYY-MM-DD format.
                  Date range is limited to 90 days.
            until: The end (inclusive) of the date range in YYYY-MM-DD format.
                  Date range is limited to 90 days.
            ca_types: List of corporate action types to return.
                     Valid types: dividend, merger, spinoff, split
            symbol: Optional filter by symbol
            cusip: Optional filter by CUSIP
            date_type: Optional date type for filtering (declaration_date, ex_date, record_date, payable_date)
            page_limit: Number of results per page (Note: API may return all results regardless)
            page_token: Token for pagination (currently not used by API)

        Returns:
            List of CorporateActionModel objects

        Raises:
            ValidationError: If date range exceeds 90 days or invalid parameters
            APIRequestError: If the API request fails
        """
        # Validate date range
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d")
            until_date = datetime.strptime(until, "%Y-%m-%d")
            date_diff = (until_date - since_date).days

            if date_diff > 90:
                raise ValidationError("Date range cannot exceed 90 days")
            if date_diff < 0:
                raise ValidationError("'since' date must be before 'until' date")
        except ValueError as e:
            raise ValidationError(f"Invalid date format. Use YYYY-MM-DD: {e}") from e

        # Validate ca_types
        valid_types = {"dividend", "merger", "spinoff", "split"}
        for ca_type in ca_types:
            if ca_type not in valid_types:
                raise ValidationError(
                    f"Invalid corporate action type: {ca_type}. "
                    f"Valid types are: {', '.join(valid_types)}"
                )

        # Build query parameters
        params: dict[str, str | bool | float | int] = {
            "since": since,
            "until": until,
            "ca_types": ",".join(ca_types),
            "page_limit": min(page_limit, 500),
        }

        # Add optional parameters
        optional_params = {
            "symbol": symbol,
            "cusip": cusip,
            "date_type": date_type,
            "page_token": page_token,
        }
        params.update({k: v for k, v in optional_params.items() if v is not None})

        # Make request
        url = f"{self.base_url}/corporate_actions/announcements"
        http_response = Requests().request(
            "GET", url, headers=self.headers, params=params
        )

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve corporate actions: {http_response.text}",
            )

        response = json.loads(http_response.text)

        # Handle response - it can be a list directly or an object with announcements
        if isinstance(response, list):
            announcements = response
        else:
            announcements = response.get("announcements", [])

        result = []
        for announcement in announcements:
            result.append(corporate_action_class_from_dict(announcement))

        # If there's a next_page_token, we could handle pagination here
        # For now, return the current page
        return result

    def get_announcement_by_id(self, announcement_id: str) -> CorporateActionModel:
        """Retrieve a specific corporate action announcement by ID.

        Args:
            announcement_id: The unique ID of the announcement

        Returns:
            CorporateActionModel object

        Raises:
            APIRequestError: If the API request fails or announcement not found
        """
        url = f"{self.base_url}/corporate_actions/announcements/{announcement_id}"
        http_response = Requests().request("GET", url, headers=self.headers)

        if http_response.status_code == 404:
            raise APIRequestError(
                404,
                f"Corporate action announcement not found: {announcement_id}",
            )
        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve corporate action: {http_response.text}",
            )

        response = json.loads(http_response.text)
        return corporate_action_class_from_dict(response)

    def get_all_announcements(
        self,
        since: str,
        until: str,
        ca_types: list[str],
        symbol: str | None = None,
        cusip: str | None = None,
        date_type: Literal["declaration_date", "ex_date", "record_date", "payable_date"]
        | None = None,
    ) -> list[CorporateActionModel]:
        """Retrieve all corporate action announcements.

        Note: The API currently returns all results within the date range
        without pagination, so this method simply calls get_announcements.

        Args:
            since: The start (inclusive) of the date range in YYYY-MM-DD format.
            until: The end (inclusive) of the date range in YYYY-MM-DD format.
            ca_types: List of corporate action types to return.
            symbol: Optional filter by symbol
            cusip: Optional filter by CUSIP
            date_type: Optional date type for filtering

        Returns:
            List of all CorporateActionModel objects

        Raises:
            ValidationError: If date range exceeds 90 days or invalid parameters
            APIRequestError: If the API request fails
        """
        # API returns all results within date range, no pagination needed currently
        return self.get_announcements(
            since=since,
            until=until,
            ca_types=ca_types,
            symbol=symbol,
            cusip=cusip,
            date_type=date_type,
        )
