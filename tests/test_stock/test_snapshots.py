import json
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.models.snapshot_model import (
    BarModel,
    SnapshotModel,
    bar_class_from_dict,
    snapshot_class_from_dict,
)
from py_alpaca_api.stock.snapshots import Snapshots


class TestSnapshots:
    @pytest.fixture
    def snapshots(self):
        headers = {
            "APCA-API-KEY-ID": "test_key",
            "APCA-API-SECRET-KEY": "test_secret",
        }
        return Snapshots(headers=headers)

    @pytest.fixture
    def mock_snapshot_response(self):
        return {
            "latestTrade": {
                "t": "2025-01-14T10:30:00Z",
                "p": 150.25,
                "s": 100,
                "c": ["@", "F"],
                "x": "Q",
                "z": "C",
            },
            "latestQuote": {
                "t": "2025-01-14T10:30:01Z",
                "ap": 150.30,
                "as": 100,
                "bp": 150.20,
                "bs": 200,
                "ax": "Q",
                "bx": "N",
                "c": ["R"],
                "z": "C",
            },
            "minuteBar": {
                "t": "2025-01-14T10:30:00Z",
                "o": 150.10,
                "h": 150.35,
                "l": 150.05,
                "c": 150.25,
                "v": 10000,
                "n": 250,
                "vw": 150.20,
            },
            "dailyBar": {
                "t": "2025-01-14T00:00:00Z",
                "o": 149.50,
                "h": 151.00,
                "l": 149.00,
                "c": 150.25,
                "v": 1000000,
                "n": 25000,
                "vw": 150.00,
            },
            "prevDailyBar": {
                "t": "2025-01-13T00:00:00Z",
                "o": 148.50,
                "h": 150.00,
                "l": 148.00,
                "c": 149.50,
                "v": 1200000,
                "n": 28000,
                "vw": 149.25,
            },
        }

    @pytest.fixture
    def mock_snapshots_response(self):
        # API returns symbols as top-level keys
        return {
            "AAPL": {
                "latestTrade": {
                    "t": "2025-01-14T10:30:00Z",
                    "p": 150.25,
                    "s": 100,
                    "c": ["@"],
                    "x": "Q",
                    "z": "C",
                },
                "latestQuote": {
                    "t": "2025-01-14T10:30:01Z",
                    "ap": 150.30,
                    "as": 100,
                    "bp": 150.20,
                    "bs": 200,
                    "ax": "Q",
                    "bx": "N",
                    "c": ["R"],
                    "z": "C",
                },
                "minuteBar": {
                    "t": "2025-01-14T10:30:00Z",
                    "o": 150.10,
                    "h": 150.35,
                    "l": 150.05,
                    "c": 150.25,
                    "v": 10000,
                    "n": 250,
                    "vw": 150.20,
                },
                "dailyBar": None,
                "prevDailyBar": None,
            },
            "MSFT": {
                "latestTrade": {
                    "t": "2025-01-14T10:30:00Z",
                    "p": 380.50,
                    "s": 50,
                    "c": [],
                    "x": "N",
                    "z": "C",
                },
                "latestQuote": {
                    "t": "2025-01-14T10:30:01Z",
                    "ap": 380.60,
                    "as": 50,
                    "bp": 380.40,
                    "bs": 100,
                    "ax": "N",
                    "bx": "P",
                    "c": [],
                    "z": "C",
                },
                "minuteBar": {
                    "t": "2025-01-14T10:30:00Z",
                    "o": 380.25,
                    "h": 380.75,
                    "l": 380.00,
                    "c": 380.50,
                    "v": 5000,
                    "n": 150,
                    "vw": 380.40,
                },
                "dailyBar": {
                    "t": "2025-01-14T00:00:00Z",
                    "o": 379.00,
                    "h": 381.00,
                    "l": 378.50,
                    "c": 380.50,
                    "v": 500000,
                    "n": 12000,
                    "vw": 380.00,
                },
                "prevDailyBar": {
                    "t": "2025-01-13T00:00:00Z",
                    "o": 378.00,
                    "h": 380.00,
                    "l": 377.50,
                    "c": 379.00,
                    "v": 600000,
                    "n": 14000,
                    "vw": 378.75,
                },
            },
        }

    def test_get_snapshot_valid_symbol(self, snapshots, mock_snapshot_response):
        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_snapshot_response)
            mock_requests.return_value.request.return_value = mock_response

            result = snapshots.get_snapshot("AAPL")

            assert isinstance(result, SnapshotModel)
            assert result.symbol == "AAPL"
            assert result.latest_trade is not None
            assert result.latest_trade.price == 150.25
            assert result.latest_quote is not None
            assert result.latest_quote.ask == 150.30
            assert result.minute_bar is not None
            assert result.minute_bar.close == 150.25
            assert result.daily_bar is not None
            assert result.prev_daily_bar is not None

    def test_get_snapshot_with_feed(self, snapshots, mock_snapshot_response):
        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_snapshot_response)
            mock_requests.return_value.request.return_value = mock_response

            snapshots.get_snapshot("AAPL", feed="sip")

            mock_requests.return_value.request.assert_called_once()
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["params"]["feed"] == "sip"

    def test_get_snapshot_invalid_symbol(self, snapshots):
        with pytest.raises(ValidationError, match="Symbol is required"):
            snapshots.get_snapshot("")

        with pytest.raises(ValidationError, match="Symbol is required"):
            snapshots.get_snapshot(None)

    def test_get_snapshot_invalid_feed(self, snapshots):
        with pytest.raises(ValidationError, match="Invalid feed"):
            snapshots.get_snapshot("AAPL", feed="invalid")

    def test_get_snapshot_api_error(self, snapshots):
        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_requests.return_value.request.side_effect = Exception("API Error")

            with pytest.raises(APIRequestError) as exc_info:
                snapshots.get_snapshot("AAPL")
            assert "Failed to get snapshot" in str(exc_info.value)

    def test_get_snapshots_multiple_symbols(self, snapshots, mock_snapshots_response):
        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_snapshots_response)
            mock_requests.return_value.request.return_value = mock_response

            result = snapshots.get_snapshots(["AAPL", "MSFT"])

            assert isinstance(result, dict)
            assert len(result) == 2
            assert "AAPL" in result
            assert "MSFT" in result
            assert isinstance(result["AAPL"], SnapshotModel)
            assert isinstance(result["MSFT"], SnapshotModel)
            assert result["AAPL"].symbol == "AAPL"
            assert result["MSFT"].symbol == "MSFT"

    def test_get_snapshots_single_symbol_returns_list(
        self, snapshots, mock_snapshots_response
    ):
        mock_single_response = {"AAPL": mock_snapshots_response["AAPL"]}

        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_single_response)
            mock_requests.return_value.request.return_value = mock_response

            result = snapshots.get_snapshots("AAPL")

            assert isinstance(result, list)
            assert len(result) == 1
            assert isinstance(result[0], SnapshotModel)
            assert result[0].symbol == "AAPL"

    def test_get_snapshots_comma_separated_string(
        self, snapshots, mock_snapshots_response
    ):
        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_snapshots_response)
            mock_requests.return_value.request.return_value = mock_response

            result = snapshots.get_snapshots("AAPL,MSFT")

            assert isinstance(result, dict)
            assert len(result) == 2
            assert "AAPL" in result
            assert "MSFT" in result

    def test_get_snapshots_invalid_symbols(self, snapshots):
        with pytest.raises(ValidationError, match="Symbols are required"):
            snapshots.get_snapshots([])

        with pytest.raises(ValidationError, match="Symbols are required"):
            snapshots.get_snapshots(None)

    def test_get_snapshots_invalid_feed(self, snapshots):
        with pytest.raises(ValidationError, match="Invalid feed"):
            snapshots.get_snapshots(["AAPL"], feed="invalid")

    def test_get_snapshots_api_error(self, snapshots):
        with patch("py_alpaca_api.stock.snapshots.Requests") as mock_requests:
            mock_requests.return_value.request.side_effect = Exception("API Error")

            with pytest.raises(APIRequestError) as exc_info:
                snapshots.get_snapshots(["AAPL", "MSFT"])
            assert "Failed to get snapshots" in str(exc_info.value)


class TestSnapshotModels:
    def test_bar_class_from_dict(self):
        # Use API field names as they come from the API
        bar_data = {
            "t": "2025-01-14T10:30:00Z",
            "o": 150.10,
            "h": 150.35,
            "l": 150.05,
            "c": 150.25,
            "v": 10000,
            "n": 250,
            "vw": 150.20,
        }

        bar = bar_class_from_dict(bar_data)

        assert isinstance(bar, BarModel)
        assert bar.open == 150.10
        assert bar.high == 150.35
        assert bar.low == 150.05
        assert bar.close == 150.25
        assert bar.volume == 10000
        assert bar.trade_count == 250
        assert bar.vwap == 150.20

    def test_bar_class_from_dict_minimal(self):
        # Use API field names, minimal data
        bar_data = {
            "t": "2025-01-14T10:30:00Z",
            "o": 150.10,
            "h": 150.35,
            "l": 150.05,
            "c": 150.25,
            "v": 10000,
        }

        bar = bar_class_from_dict(bar_data)

        assert isinstance(bar, BarModel)
        assert bar.trade_count is None
        assert bar.vwap is None

    def test_snapshot_class_from_dict_full(self):
        snapshot_data = {
            "symbol": "AAPL",
            "latestTrade": {
                "t": "2025-01-14T10:30:00Z",
                "p": 150.25,
                "s": 100,
                "c": ["@"],
                "x": "Q",
                "z": "C",
            },
            "latestQuote": {
                "t": "2025-01-14T10:30:01Z",
                "ap": 150.30,
                "as": 100,
                "bp": 150.20,
                "bs": 200,
                "ax": "Q",
                "bx": "N",
                "c": ["R"],
                "z": "C",
            },
            "minuteBar": {
                "t": "2025-01-14T10:30:00Z",
                "o": 150.10,
                "h": 150.35,
                "l": 150.05,
                "c": 150.25,
                "v": 10000,
                "n": 250,
                "vw": 150.20,
            },
            "dailyBar": {
                "t": "2025-01-14T00:00:00Z",
                "o": 149.50,
                "h": 151.00,
                "l": 149.00,
                "c": 150.25,
                "v": 1000000,
                "n": 25000,
                "vw": 150.00,
            },
            "prevDailyBar": {
                "t": "2025-01-13T00:00:00Z",
                "o": 148.50,
                "h": 150.00,
                "l": 148.00,
                "c": 149.50,
                "v": 1200000,
                "n": 28000,
                "vw": 149.25,
            },
        }

        snapshot = snapshot_class_from_dict(snapshot_data)

        assert isinstance(snapshot, SnapshotModel)
        assert snapshot.symbol == "AAPL"
        assert snapshot.latest_trade is not None
        assert snapshot.latest_trade.price == 150.25
        assert snapshot.latest_quote is not None
        assert snapshot.latest_quote.ask == 150.30
        assert snapshot.minute_bar is not None
        assert snapshot.minute_bar.close == 150.25
        assert snapshot.daily_bar is not None
        assert snapshot.daily_bar.close == 150.25
        assert snapshot.prev_daily_bar is not None
        assert snapshot.prev_daily_bar.close == 149.50

    def test_snapshot_class_from_dict_partial(self):
        snapshot_data = {
            "symbol": "AAPL",
            "latestTrade": {
                "t": "2025-01-14T10:30:00Z",
                "p": 150.25,
                "s": 100,
                "c": [],
                "x": "Q",
                "z": "C",
            },
            "latestQuote": None,
            "minuteBar": None,
            "dailyBar": None,
            "prevDailyBar": None,
        }

        snapshot = snapshot_class_from_dict(snapshot_data)

        assert isinstance(snapshot, SnapshotModel)
        assert snapshot.symbol == "AAPL"
        assert snapshot.latest_trade is not None
        assert snapshot.latest_quote is None
        assert snapshot.minute_bar is None
        assert snapshot.daily_bar is None
        assert snapshot.prev_daily_bar is None
