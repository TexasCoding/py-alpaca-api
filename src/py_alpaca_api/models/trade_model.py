from dataclasses import dataclass
from typing import Any


@dataclass
class TradeModel:
    """Model for individual stock trade data."""

    timestamp: str  # RFC-3339 format timestamp
    symbol: str
    exchange: str
    price: float
    size: int
    conditions: list[str] | None
    id: int
    tape: str


def trade_class_from_dict(
    data: dict[str, Any], symbol: str | None = None
) -> TradeModel:
    """Create TradeModel from API response dictionary.

    Args:
        data: Dictionary containing trade data from API
        symbol: Optional symbol to use if not in data

    Returns:
        TradeModel instance
    """
    return TradeModel(
        timestamp=data.get("t", ""),
        symbol=data.get("symbol", symbol or ""),
        exchange=data.get("x", ""),
        price=float(data.get("p", 0.0)),
        size=int(data.get("s", 0)),
        conditions=data.get("c", []),
        id=int(data.get("i", 0)),
        tape=data.get("z", ""),
    )


@dataclass
class LatestTradeModel:
    """Model for latest trade data with symbol."""

    trade: TradeModel
    symbol: str


@dataclass
class TradesResponse:
    """Response model for trades endpoint with pagination."""

    trades: list[TradeModel]
    symbol: str
    next_page_token: str | None = None


def extract_trades_data(data: dict[str, Any]) -> dict[str, Any]:
    """Extract and transform trades data from API response.

    Args:
        data: Raw API response data

    Returns:
        Transformed dictionary ready for model creation
    """
    # Handle both single trade and multiple trades response formats
    if "trades" in data:
        # Multiple trades response
        return data
    if "trade" in data:
        # Single latest trade response
        return {"trades": [data["trade"]], "symbol": data.get("symbol", "")}
    # Direct trade data
    return {"trades": [data], "symbol": data.get("symbol", "")}
