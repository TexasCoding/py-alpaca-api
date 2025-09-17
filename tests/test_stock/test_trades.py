import os
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.models.trade_model import (
    TradeModel,
    TradesResponse,
    trade_class_from_dict,
)


@pytest.fixture
def alpaca():
    """Create PyAlpacaAPI instance for testing."""
    return PyAlpacaAPI(
        api_key=os.environ.get("ALPACA_API_KEY", "test_key"),
        api_secret=os.environ.get("ALPACA_SECRET_KEY", "test_secret"),
        api_paper=True,
    )


@pytest.fixture
def mock_trade_response():
    """Sample trade response data."""
    return {
        "t": "2024-01-15T14:30:00Z",
        "x": "V",  # IEX exchange
        "p": 150.25,
        "s": 100,
        "c": ["@", "I"],
        "i": 12345,
        "z": "C",
    }


@pytest.fixture
def mock_trades_response():
    """Sample multiple trades response."""
    return {
        "trades": [
            {
                "t": "2024-01-15T14:30:00Z",
                "x": "V",
                "p": 150.25,
                "s": 100,
                "c": ["@"],
                "i": 12345,
                "z": "C",
            },
            {
                "t": "2024-01-15T14:30:01Z",
                "x": "K",
                "p": 150.26,
                "s": 200,
                "c": ["F"],
                "i": 12346,
                "z": "C",
            },
        ],
        "symbol": "AAPL",
        "next_page_token": "token123",
    }


class TestTrades:
    """Test suite for Trades functionality."""

    def test_trade_model_creation(self, mock_trade_response):
        """Test creating a TradeModel from dict."""
        trade = trade_class_from_dict(mock_trade_response, "AAPL")

        assert isinstance(trade, TradeModel)
        assert trade.timestamp == "2024-01-15T14:30:00Z"
        assert trade.symbol == "AAPL"
        assert trade.exchange == "V"
        assert trade.price == 150.25
        assert trade.size == 100
        assert trade.conditions == ["@", "I"]
        assert trade.id == 12345
        assert trade.tape == "C"

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_trades_success(self, mock_request, alpaca, mock_trades_response):
        """Test successful retrieval of historical trades."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"trades": [{"t": "2024-01-15T14:30:00Z", "x": "V", "p": 150.25, "s": 100, "c": ["@"], "i": 12345, "z": "C"}], "symbol": "AAPL", "next_page_token": null}'
        mock_request.return_value = mock_response

        # Call method
        result = alpaca.stock.trades.get_trades(
            symbol="AAPL",
            start="2024-01-15T14:00:00Z",
            end="2024-01-15T15:00:00Z",
            limit=100,
        )

        # Verify
        assert isinstance(result, TradesResponse)
        assert len(result.trades) == 1
        assert result.symbol == "AAPL"
        assert result.trades[0].price == 150.25

    def test_get_trades_validation(self, alpaca):
        """Test validation for get_trades parameters."""
        # Test missing symbol
        with pytest.raises(ValidationError, match="Symbol is required"):
            alpaca.stock.trades.get_trades(
                symbol="",
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
            )

        # Test invalid limit
        with pytest.raises(ValidationError, match="Limit must be between"):
            alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
                limit=10001,
            )

        # Test invalid date format
        with pytest.raises(ValidationError, match="Invalid date format"):
            alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start="2024-01-15",  # Missing time
                end="2024-01-15T15:00:00Z",
            )

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_latest_trade_success(self, mock_request, alpaca):
        """Test successful retrieval of latest trade."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"trades": {"AAPL": {"t": "2024-01-15T14:30:00Z", "x": "V", "p": 150.25, "s": 100, "c": ["@"], "i": 12345, "z": "C"}}}'
        mock_request.return_value = mock_response

        # Call method
        result = alpaca.stock.trades.get_latest_trade("AAPL")

        # Verify
        assert isinstance(result, TradeModel)
        assert result.symbol == "AAPL"
        assert result.price == 150.25
        assert result.exchange == "V"

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_latest_trade_not_found(self, mock_request, alpaca):
        """Test handling when symbol not found in latest trades."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"trades": {}}'
        mock_request.return_value = mock_response

        # Call method and expect error
        with pytest.raises(APIRequestError, match="No trade data found"):
            alpaca.stock.trades.get_latest_trade("INVALID")

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_trades_multi_success(self, mock_request, alpaca):
        """Test successful retrieval of trades for multiple symbols."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """{
            "trades": {
                "AAPL": [{"t": "2024-01-15T14:30:00Z", "x": "V", "p": 150.25, "s": 100, "c": ["@"], "i": 12345, "z": "C"}],
                "MSFT": [{"t": "2024-01-15T14:30:00Z", "x": "K", "p": 380.50, "s": 50, "c": ["F"], "i": 12346, "z": "C"}]
            },
            "next_page_token": null
        }"""
        mock_request.return_value = mock_response

        # Call method
        result = alpaca.stock.trades.get_trades_multi(
            symbols=["AAPL", "MSFT"],
            start="2024-01-15T14:00:00Z",
            end="2024-01-15T15:00:00Z",
        )

        # Verify
        assert isinstance(result, dict)
        assert "AAPL" in result
        assert "MSFT" in result
        assert isinstance(result["AAPL"], TradesResponse)
        assert len(result["AAPL"].trades) == 1
        assert result["AAPL"].trades[0].price == 150.25
        assert result["MSFT"].trades[0].price == 380.50

    def test_get_trades_multi_validation(self, alpaca):
        """Test validation for multi-symbol trades."""
        # Test empty symbols list
        with pytest.raises(ValidationError, match="At least one symbol"):
            alpaca.stock.trades.get_trades_multi(
                symbols=[],
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
            )

        # Test too many symbols
        with pytest.raises(ValidationError, match="Maximum 100 symbols"):
            alpaca.stock.trades.get_trades_multi(
                symbols=["AAPL"] * 101,
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
            )

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_latest_trades_multi(self, mock_request, alpaca):
        """Test getting latest trades for multiple symbols."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """{
            "trades": {
                "AAPL": {"t": "2024-01-15T14:30:00Z", "x": "V", "p": 150.25, "s": 100, "c": ["@"], "i": 12345, "z": "C"},
                "MSFT": {"t": "2024-01-15T14:30:01Z", "x": "K", "p": 380.50, "s": 50, "c": ["F"], "i": 12346, "z": "C"}
            }
        }"""
        mock_request.return_value = mock_response

        # Call method
        result = alpaca.stock.trades.get_latest_trades_multi(["AAPL", "MSFT"])

        # Verify
        assert isinstance(result, dict)
        assert "AAPL" in result
        assert "MSFT" in result
        assert isinstance(result["AAPL"], TradeModel)
        assert result["AAPL"].price == 150.25
        assert result["MSFT"].price == 380.50

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_all_trades_pagination(self, mock_request, alpaca):
        """Test get_all_trades with pagination."""
        # Setup mock responses for pagination
        responses = [
            MagicMock(
                status_code=200,
                text='{"trades": [{"t": "2024-01-15T14:30:00Z", "x": "V", "p": 150.25, "s": 100, "c": ["@"], "i": 1, "z": "C"}], "symbol": "AAPL", "next_page_token": "page2"}',
            ),
            MagicMock(
                status_code=200,
                text='{"trades": [{"t": "2024-01-15T14:31:00Z", "x": "K", "p": 150.30, "s": 200, "c": ["F"], "i": 2, "z": "C"}], "symbol": "AAPL", "next_page_token": null}',
            ),
        ]
        mock_request.side_effect = responses

        # Call method
        result = alpaca.stock.trades.get_all_trades(
            symbol="AAPL",
            start="2024-01-15T14:00:00Z",
            end="2024-01-15T15:00:00Z",
        )

        # Verify
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].price == 150.25
        assert result[1].price == 150.30

    def test_feed_parameter(self, alpaca):
        """Test that feed parameter is properly handled."""
        with patch("py_alpaca_api.http.requests.Requests.request") as mock_request:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = '{"trades": [], "symbol": "AAPL"}'
            mock_request.return_value = mock_response

            # Call with feed parameter
            alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
                feed="sip",
            )

            # Verify feed was included in params
            call_args = mock_request.call_args
            assert call_args[1]["params"]["feed"] == "sip"

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_api_error_handling(self, mock_request, alpaca):
        """Test handling of API errors."""
        # Setup mock error response
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden: Subscription required"
        mock_request.return_value = mock_response

        # Call method and expect error
        with pytest.raises(APIRequestError) as exc_info:
            alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
            )

        assert exc_info.value.status_code == 403
        assert "Failed to retrieve trades" in str(exc_info.value)

    def test_trades_response_model(self):
        """Test TradesResponse model creation."""
        trades = [
            TradeModel(
                timestamp="2024-01-15T14:30:00Z",
                symbol="AAPL",
                exchange="V",
                price=150.25,
                size=100,
                conditions=["@"],
                id=12345,
                tape="C",
            )
        ]

        response = TradesResponse(
            trades=trades, symbol="AAPL", next_page_token="token123"
        )

        assert response.symbol == "AAPL"
        assert len(response.trades) == 1
        assert response.next_page_token == "token123"
