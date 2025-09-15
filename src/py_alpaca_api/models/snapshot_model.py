from dataclasses import dataclass

import pendulum

from py_alpaca_api.models.quote_model import QuoteModel, quote_class_from_dict
from py_alpaca_api.models.trade_model import TradeModel, trade_class_from_dict


@dataclass
class BarModel:
    timestamp: str  # Store as string for consistency with other models
    open: float
    high: float
    low: float
    close: float
    volume: int
    trade_count: int | None = None
    vwap: float | None = None


@dataclass
class SnapshotModel:
    symbol: str
    latest_trade: TradeModel | None = None
    latest_quote: QuoteModel | None = None
    minute_bar: BarModel | None = None
    daily_bar: BarModel | None = None
    prev_daily_bar: BarModel | None = None


def bar_class_from_dict(data: dict) -> BarModel:
    # Parse timestamp
    timestamp_str = data.get("t", "")
    if timestamp_str:
        timestamp = pendulum.parse(timestamp_str, tz="America/New_York")
        if isinstance(timestamp, pendulum.DateTime):
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_str = str(timestamp)

    return BarModel(
        timestamp=timestamp_str,
        open=float(data.get("o", 0.0)),
        high=float(data.get("h", 0.0)),
        low=float(data.get("l", 0.0)),
        close=float(data.get("c", 0.0)),
        volume=int(data.get("v", 0)),
        trade_count=int(data["n"]) if "n" in data and data["n"] is not None else None,
        vwap=float(data["vw"]) if "vw" in data and data["vw"] is not None else None,
    )


def snapshot_class_from_dict(data: dict) -> SnapshotModel:
    snapshot_data = {"symbol": data.get("symbol", "")}

    if data.get("latestTrade"):
        trade_data = data["latestTrade"]
        snapshot_data["latest_trade"] = trade_class_from_dict(
            trade_data, data.get("symbol", "")
        )

    if data.get("latestQuote"):
        quote_data = data["latestQuote"]
        # Map API field names to model field names
        quote_dict = {
            "symbol": data.get("symbol", ""),
            "timestamp": quote_data.get("t", ""),
            "ask": quote_data.get("ap", 0.0),
            "ask_size": quote_data.get("as", 0),
            "bid": quote_data.get("bp", 0.0),
            "bid_size": quote_data.get("bs", 0),
        }
        snapshot_data["latest_quote"] = quote_class_from_dict(quote_dict)

    if data.get("minuteBar"):
        bar_data = data["minuteBar"]
        snapshot_data["minute_bar"] = bar_class_from_dict(bar_data)

    if data.get("dailyBar"):
        bar_data = data["dailyBar"]
        snapshot_data["daily_bar"] = bar_class_from_dict(bar_data)

    if data.get("prevDailyBar"):
        bar_data = data["prevDailyBar"]
        snapshot_data["prev_daily_bar"] = bar_class_from_dict(bar_data)

    return SnapshotModel(**snapshot_data)
