"""Unit tests for streaming data models."""

from datetime import datetime

from py_alpaca_api.streaming.stream_models import BarData, QuoteData, TradeData


class TestStreamModels:
    """Test streaming data models."""

    def test_quote_data_from_dict(self):
        """Test creating QuoteData from dictionary."""
        data = {
            "T": "q",
            "S": "AAPL",
            "t": "2024-01-01T10:00:00",
            "bp": 150.50,
            "bs": 100,
            "ap": 150.55,
            "as": 200,
            "bx": "Q",
            "ax": "P",
            "c": ["R"],
        }

        quote = QuoteData.from_dict(data)

        assert quote.symbol == "AAPL"
        assert quote.message_type == "quote"
        assert quote.bid_price == 150.50
        assert quote.bid_size == 100
        assert quote.ask_price == 150.55
        assert quote.ask_size == 200
        assert quote.bid_exchange == "Q"
        assert quote.ask_exchange == "P"
        assert quote.conditions == ["R"]

    def test_quote_data_with_missing_fields(self):
        """Test QuoteData with missing fields."""
        data = {
            "T": "q",
            "S": "AAPL",
            "t": "2024-01-01T10:00:00",
        }

        quote = QuoteData.from_dict(data)

        assert quote.symbol == "AAPL"
        assert quote.bid_price == 0.0
        assert quote.bid_size == 0
        assert quote.conditions == []

    def test_trade_data_from_dict(self):
        """Test creating TradeData from dictionary."""
        data = {
            "T": "t",
            "S": "AAPL",
            "t": "2024-01-01T10:00:00",
            "p": 150.52,
            "s": 100,
            "x": "Q",
            "i": 12345,
            "c": ["@", "I"],
        }

        trade = TradeData.from_dict(data)

        assert trade.symbol == "AAPL"
        assert trade.message_type == "trade"
        assert trade.price == 150.52
        assert trade.size == 100
        assert trade.exchange == "Q"
        assert trade.trade_id == "12345"
        assert trade.conditions == ["@", "I"]

    def test_trade_data_with_missing_fields(self):
        """Test TradeData with missing fields."""
        data = {
            "T": "t",
            "S": "AAPL",
            "t": "2024-01-01T10:00:00",
        }

        trade = TradeData.from_dict(data)

        assert trade.symbol == "AAPL"
        assert trade.price == 0.0
        assert trade.size == 0
        assert trade.exchange == ""
        assert trade.trade_id == ""

    def test_bar_data_from_dict(self):
        """Test creating BarData from dictionary."""
        data = {
            "T": "b",
            "S": "AAPL",
            "t": "2024-01-01T10:00:00",
            "o": 150.00,
            "h": 151.00,
            "l": 149.50,
            "c": 150.75,
            "v": 1000000,
            "n": 5000,
            "vw": 150.45,
        }

        bar = BarData.from_dict(data)

        assert bar.symbol == "AAPL"
        assert bar.message_type == "bar"
        assert bar.open == 150.00
        assert bar.high == 151.00
        assert bar.low == 149.50
        assert bar.close == 150.75
        assert bar.volume == 1000000
        assert bar.trade_count == 5000
        assert bar.vwap == 150.45

    def test_bar_data_with_missing_fields(self):
        """Test BarData with missing fields."""
        data = {
            "T": "b",
            "S": "AAPL",
            "t": "2024-01-01T10:00:00",
        }

        bar = BarData.from_dict(data)

        assert bar.symbol == "AAPL"
        assert bar.open == 0.0
        assert bar.high == 0.0
        assert bar.low == 0.0
        assert bar.close == 0.0
        assert bar.volume == 0
        assert bar.trade_count == 0

    def test_timestamp_parsing(self):
        """Test timestamp parsing in all models."""
        timestamp_str = "2024-01-01T10:30:45.123456"

        quote_data = {"T": "q", "S": "TEST", "t": timestamp_str}
        trade_data = {"T": "t", "S": "TEST", "t": timestamp_str}
        bar_data = {"T": "b", "S": "TEST", "t": timestamp_str}

        quote = QuoteData.from_dict(quote_data)
        trade = TradeData.from_dict(trade_data)
        bar = BarData.from_dict(bar_data)

        expected_time = datetime.fromisoformat(timestamp_str)
        assert quote.timestamp == expected_time
        assert trade.timestamp == expected_time
        assert bar.timestamp == expected_time
