import json
from datetime import datetime
from typing import Literal

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.trade_model import (
    TradeModel,
    TradesResponse,
    trade_class_from_dict,
)


def _validate_datetime_format(start: str, end: str) -> None:
    """Validate that datetime strings include time component.

    Args:
        start: Start datetime string
        end: End datetime string

    Raises:
        ValueError: If dates don't include time component
    """
    if "T" not in start or "T" not in end:
        raise ValueError("Date must include time (RFC-3339 format)")


class Trades:
    def __init__(self, headers: dict[str, str]) -> None:
        self.headers = headers
        self.base_url = "https://data.alpaca.markets/v2"

    def get_trades(
        self,
        symbol: str,
        start: str,
        end: str,
        limit: int = 1000,
        feed: Literal["iex", "sip", "otc"] | None = None,
        page_token: str | None = None,
        asof: str | None = None,
    ) -> TradesResponse:
        """Retrieve historical trades for a symbol.

        Args:
            symbol: The stock symbol to retrieve trades for
            start: Start time in RFC-3339 format (YYYY-MM-DDTHH:MM:SSZ)
            end: End time in RFC-3339 format (YYYY-MM-DDTHH:MM:SSZ)
            limit: Number of trades to return (1-10000, default 1000)
            feed: Data feed to use (iex, sip, otc)
            page_token: Token for pagination
            asof: As-of time for historical data in RFC-3339 format

        Returns:
            TradesResponse with list of trades and pagination token

        Raises:
            ValidationError: If parameters are invalid
            APIRequestError: If the API request fails
        """
        # Validate parameters
        if not symbol:
            raise ValidationError("Symbol is required")

        if limit < 1 or limit > 10000:
            raise ValidationError("Limit must be between 1 and 10000")

        # Validate date formats (must include time)
        try:
            _validate_datetime_format(start, end)
            datetime.fromisoformat(start.replace("Z", "+00:00"))
            datetime.fromisoformat(end.replace("Z", "+00:00"))
        except (ValueError, AttributeError) as e:
            raise ValidationError(
                f"Invalid date format. Use RFC-3339 format (YYYY-MM-DDTHH:MM:SSZ): {e}"
            ) from e

        # Build query parameters
        params: dict[str, str | bool | float | int] = {
            "start": start,
            "end": end,
            "limit": limit,
        }

        if feed:
            params["feed"] = feed
        if page_token:
            params["page_token"] = page_token
        if asof:
            params["asof"] = asof

        # Make request
        url = f"{self.base_url}/stocks/{symbol}/trades"
        http_response = Requests().request(
            "GET", url, headers=self.headers, params=params
        )

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve trades: {http_response.text}",
            )

        response = json.loads(http_response.text) if http_response.text else {}

        # Parse trades
        trades = []
        for trade_data in response.get("trades", []) or []:
            trades.append(trade_class_from_dict(trade_data, symbol))

        return TradesResponse(
            trades=trades,
            symbol=response.get("symbol", symbol),
            next_page_token=response.get("next_page_token"),
        )

    def get_latest_trade(
        self,
        symbol: str,
        feed: Literal["iex", "sip", "otc"] | None = None,
        asof: str | None = None,
    ) -> TradeModel:
        """Get the latest trade for a symbol.

        Args:
            symbol: The stock symbol to retrieve latest trade for
            feed: Data feed to use (iex, sip, otc)
            asof: As-of time for historical data in RFC-3339 format

        Returns:
            TradeModel with the latest trade data

        Raises:
            ValidationError: If symbol is invalid
            APIRequestError: If the API request fails
        """
        if not symbol:
            raise ValidationError("Symbol is required")

        # Build query parameters
        params: dict[str, str | bool | float | int] = {"symbols": symbol}

        if feed:
            params["feed"] = feed
        if asof:
            params["asof"] = asof

        # Make request
        url = f"{self.base_url}/stocks/trades/latest"
        http_response = Requests().request(
            "GET", url, headers=self.headers, params=params
        )

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve latest trade: {http_response.text}",
            )

        response = json.loads(http_response.text)

        # Handle response format
        if "trades" in response and symbol in response["trades"]:
            trade_data = response["trades"][symbol]
        elif symbol in response:
            trade_data = response[symbol]
        else:
            raise APIRequestError(
                404,
                f"No trade data found for symbol: {symbol}",
            )

        return trade_class_from_dict(trade_data, symbol)

    def get_trades_multi(
        self,
        symbols: list[str],
        start: str,
        end: str,
        limit: int = 1000,
        feed: Literal["iex", "sip", "otc"] | None = None,
        page_token: str | None = None,
        asof: str | None = None,
    ) -> dict[str, TradesResponse]:
        """Retrieve historical trades for multiple symbols.

        Args:
            symbols: List of stock symbols (max 100)
            start: Start time in RFC-3339 format
            end: End time in RFC-3339 format
            limit: Number of trades per symbol (1-10000, default 1000)
            feed: Data feed to use
            page_token: Token for pagination
            asof: As-of time for historical data

        Returns:
            Dictionary mapping symbols to TradesResponse objects

        Raises:
            ValidationError: If parameters are invalid
            APIRequestError: If the API request fails
        """
        if not symbols:
            raise ValidationError("At least one symbol is required")

        if len(symbols) > 100:
            raise ValidationError("Maximum 100 symbols allowed")

        if limit < 1 or limit > 10000:
            raise ValidationError("Limit must be between 1 and 10000")

        # Validate date formats (must include time)
        try:
            _validate_datetime_format(start, end)
            datetime.fromisoformat(start.replace("Z", "+00:00"))
            datetime.fromisoformat(end.replace("Z", "+00:00"))
        except (ValueError, AttributeError) as e:
            raise ValidationError(
                f"Invalid date format. Use RFC-3339 format (YYYY-MM-DDTHH:MM:SSZ): {e}"
            ) from e

        # Build query parameters
        params: dict[str, str | bool | float | int] = {
            "symbols": ",".join(symbols),
            "start": start,
            "end": end,
            "limit": limit,
        }

        if feed:
            params["feed"] = feed
        if page_token:
            params["page_token"] = page_token
        if asof:
            params["asof"] = asof

        # Make request
        url = f"{self.base_url}/stocks/trades"
        http_response = Requests().request(
            "GET", url, headers=self.headers, params=params
        )

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve trades: {http_response.text}",
            )

        response = json.loads(http_response.text)

        # Parse response for each symbol
        result = {}
        trades_data = response.get("trades", {})
        next_page_token = response.get("next_page_token")

        for symbol in symbols:
            if symbol in trades_data:
                trades = [
                    trade_class_from_dict(trade, symbol)
                    for trade in trades_data[symbol]
                ]
                result[symbol] = TradesResponse(
                    trades=trades,
                    symbol=symbol,
                    next_page_token=next_page_token,
                )
            else:
                # Symbol had no trades in the time period
                result[symbol] = TradesResponse(
                    trades=[],
                    symbol=symbol,
                    next_page_token=None,
                )

        return result

    def get_latest_trades_multi(
        self,
        symbols: list[str],
        feed: Literal["iex", "sip", "otc"] | None = None,
        asof: str | None = None,
    ) -> dict[str, TradeModel]:
        """Get latest trades for multiple symbols.

        Args:
            symbols: List of stock symbols (max 100)
            feed: Data feed to use
            asof: As-of time for historical data

        Returns:
            Dictionary mapping symbols to their latest TradeModel

        Raises:
            ValidationError: If parameters are invalid
            APIRequestError: If the API request fails
        """
        if not symbols:
            raise ValidationError("At least one symbol is required")

        if len(symbols) > 100:
            raise ValidationError("Maximum 100 symbols allowed")

        # Build query parameters
        params: dict[str, str | bool | float | int] = {"symbols": ",".join(symbols)}

        if feed:
            params["feed"] = feed
        if asof:
            params["asof"] = asof

        # Make request
        url = f"{self.base_url}/stocks/trades/latest"
        http_response = Requests().request(
            "GET", url, headers=self.headers, params=params
        )

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve latest trades: {http_response.text}",
            )

        response = json.loads(http_response.text)

        # Parse response
        result = {}
        trades_data = response.get("trades", response)

        for symbol in symbols:
            if symbol in trades_data:
                result[symbol] = trade_class_from_dict(trades_data[symbol], symbol)

        return result

    def get_all_trades(
        self,
        symbol: str,
        start: str,
        end: str,
        feed: Literal["iex", "sip", "otc"] | None = None,
        asof: str | None = None,
    ) -> list[TradeModel]:
        """Retrieve all trades for a symbol with automatic pagination.

        Args:
            symbol: The stock symbol
            start: Start time in RFC-3339 format
            end: End time in RFC-3339 format
            feed: Data feed to use
            asof: As-of time for historical data

        Returns:
            List of all TradeModel objects across all pages

        Raises:
            ValidationError: If parameters are invalid
            APIRequestError: If the API request fails
        """
        all_trades = []
        page_token = None

        while True:
            response = self.get_trades(
                symbol=symbol,
                start=start,
                end=end,
                limit=10000,  # Max limit for efficiency
                feed=feed,
                page_token=page_token,
                asof=asof,
            )

            all_trades.extend(response.trades)

            # Check if there are more pages
            if response.next_page_token:
                page_token = response.next_page_token
            else:
                break

        return all_trades
