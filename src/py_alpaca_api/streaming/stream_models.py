"""Data models for streaming market data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class StreamMessage:
    """Base class for all streaming messages."""

    symbol: str
    timestamp: datetime
    message_type: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StreamMessage:
        """Create StreamMessage from dictionary."""
        return cls(
            symbol=data.get("S", ""),
            timestamp=datetime.fromisoformat(data.get("t", "")),
            message_type=data.get("T", ""),
        )


@dataclass
class QuoteData(StreamMessage):
    """Real-time quote data."""

    bid_price: float
    bid_size: int
    ask_price: float
    ask_size: int
    bid_exchange: str
    ask_exchange: str
    conditions: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> QuoteData:
        """Create QuoteData from dictionary."""
        return cls(
            symbol=data.get("S", ""),
            timestamp=datetime.fromisoformat(data.get("t", "")),
            message_type="quote",
            bid_price=float(data.get("bp", 0.0)),
            bid_size=int(data.get("bs", 0)),
            ask_price=float(data.get("ap", 0.0)),
            ask_size=int(data.get("as", 0)),
            bid_exchange=data.get("bx", ""),
            ask_exchange=data.get("ax", ""),
            conditions=data.get("c", []),
        )


@dataclass
class TradeData(StreamMessage):
    """Real-time trade data."""

    price: float
    size: int
    exchange: str
    trade_id: str
    conditions: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TradeData:
        """Create TradeData from dictionary."""
        return cls(
            symbol=data.get("S", ""),
            timestamp=datetime.fromisoformat(data.get("t", "")),
            message_type="trade",
            price=float(data.get("p", 0.0)),
            size=int(data.get("s", 0)),
            exchange=data.get("x", ""),
            trade_id=str(data.get("i", "")),
            conditions=data.get("c", []),
        )


@dataclass
class BarData(StreamMessage):
    """Real-time bar data."""

    open: float
    high: float
    low: float
    close: float
    volume: int
    trade_count: int
    vwap: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BarData:
        """Create BarData from dictionary."""
        return cls(
            symbol=data.get("S", ""),
            timestamp=datetime.fromisoformat(data.get("t", "")),
            message_type="bar",
            open=float(data.get("o", 0.0)),
            high=float(data.get("h", 0.0)),
            low=float(data.get("l", 0.0)),
            close=float(data.get("c", 0.0)),
            volume=int(data.get("v", 0)),
            trade_count=int(data.get("n", 0)),
            vwap=float(data.get("vw", 0.0)),
        )
