"""Test cases for historical quotes functionality."""

import json
from unittest.mock import MagicMock

import pandas as pd
import pytest

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.stock.quotes import Quotes


class TestQuotes:
    """Test suite for the Quotes class."""

    @pytest.fixture
    def quotes_instance(self):
        """Create a Quotes instance for testing."""
        return Quotes(headers={"Authorization": "Bearer TEST"})

    def test_get_historical_quotes_single_symbol(self, quotes_instance, mocker):
        """Test getting historical quotes for a single symbol."""
        # Mock response data
        mock_response = {
            "quotes": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "ax": "Q",
                    "ap": 185.50,
                    "as": 100,
                    "bx": "Q",
                    "bp": 185.45,
                    "bs": 200,
                    "c": ["R"],
                    "z": "A",
                },
                {
                    "t": "2024-01-10T09:30:01Z",
                    "ax": "Q",
                    "ap": 185.52,
                    "as": 150,
                    "bx": "Q",
                    "bp": 185.48,
                    "bs": 250,
                    "c": ["R"],
                    "z": "A",
                },
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = quotes_instance.get_historical_quotes(
            "AAPL", start="2024-01-10T09:30:00Z", end="2024-01-10T16:00:00Z"
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "ask_price" in result.columns
        assert "bid_price" in result.columns
        assert "ask_size" in result.columns
        assert "bid_size" in result.columns
        assert "spread" in result.columns
        assert "spread_pct" in result.columns

        # Check values
        assert result.iloc[0]["ask_price"] == 185.50
        assert result.iloc[0]["bid_price"] == 185.45
        assert result.iloc[0]["spread"] == pytest.approx(0.05)

    def test_get_historical_quotes_multiple_symbols(self, quotes_instance, mocker):
        """Test getting historical quotes for multiple symbols."""
        # Mock response data
        mock_response = {
            "quotes": {
                "AAPL": [
                    {
                        "t": "2024-01-10T09:30:00Z",
                        "ax": "Q",
                        "ap": 185.50,
                        "as": 100,
                        "bx": "Q",
                        "bp": 185.45,
                        "bs": 200,
                        "c": ["R"],
                        "z": "A",
                    }
                ],
                "MSFT": [
                    {
                        "t": "2024-01-10T09:30:00Z",
                        "ax": "Q",
                        "ap": 400.50,
                        "as": 50,
                        "bx": "Q",
                        "bp": 400.45,
                        "bs": 75,
                        "c": ["R"],
                        "z": "A",
                    }
                ],
            },
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = quotes_instance.get_historical_quotes(
            ["AAPL", "MSFT"], start="2024-01-10T09:30:00Z", end="2024-01-10T16:00:00Z"
        )

        # Assertions
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "AAPL" in result
        assert "MSFT" in result

        # Check AAPL data
        aapl_df = result["AAPL"]
        assert isinstance(aapl_df, pd.DataFrame)
        assert aapl_df.iloc[0]["ask_price"] == 185.50

        # Check MSFT data
        msft_df = result["MSFT"]
        assert isinstance(msft_df, pd.DataFrame)
        assert msft_df.iloc[0]["ask_price"] == 400.50

    def test_get_historical_quotes_pagination(self, quotes_instance, mocker):
        """Test pagination handling for historical quotes."""
        # First response with next_page_token
        mock_response_1 = {
            "quotes": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "ax": "Q",
                    "ap": 185.50,
                    "as": 100,
                    "bx": "Q",
                    "bp": 185.45,
                    "bs": 200,
                    "c": ["R"],
                    "z": "A",
                }
            ],
            "next_page_token": "token123",
        }

        # Second response without next_page_token
        mock_response_2 = {
            "quotes": [
                {
                    "t": "2024-01-10T09:30:01Z",
                    "ax": "Q",
                    "ap": 185.52,
                    "as": 150,
                    "bx": "Q",
                    "bp": 185.48,
                    "bs": 250,
                    "c": ["R"],
                    "z": "A",
                }
            ],
            "next_page_token": None,
        }

        # Mock the Requests call to return different responses
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.side_effect = [
            MagicMock(text=json.dumps(mock_response_1)),
            MagicMock(text=json.dumps(mock_response_2)),
        ]

        # Call the method
        result = quotes_instance.get_historical_quotes(
            "AAPL", start="2024-01-10T09:30:00Z", end="2024-01-10T16:00:00Z"
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2  # Should have combined both pages
        assert mock_request.call_count == 2  # Should have made 2 API calls

    def test_get_historical_quotes_invalid_feed(self, quotes_instance):
        """Test that invalid feed raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid feed"):
            quotes_instance.get_historical_quotes(
                "AAPL", start="2024-01-10", end="2024-01-11", feed="invalid"
            )

    def test_get_historical_quotes_invalid_sort(self, quotes_instance):
        """Test that invalid sort raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid sort"):
            quotes_instance.get_historical_quotes(
                "AAPL", start="2024-01-10", end="2024-01-11", sort="invalid"
            )

    def test_get_historical_quotes_invalid_limit(self, quotes_instance):
        """Test that invalid limit raises ValidationError."""
        with pytest.raises(ValidationError, match="Limit must be at least 1"):
            quotes_instance.get_historical_quotes(
                "AAPL", start="2024-01-10", end="2024-01-11", limit=0
            )

    def test_get_historical_quotes_invalid_date_format(self, quotes_instance):
        """Test that invalid date format raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            quotes_instance.get_historical_quotes(
                "AAPL", start="invalid-date", end="2024-01-11"
            )

    def test_get_historical_quotes_empty_symbols(self, quotes_instance):
        """Test that empty symbols raises ValidationError."""
        with pytest.raises(ValidationError, match="At least one symbol is required"):
            quotes_instance.get_historical_quotes(
                [], start="2024-01-10", end="2024-01-11"
            )

    def test_get_historical_quotes_no_data(self, quotes_instance, mocker):
        """Test handling when no data is returned."""
        # Mock response with no data
        mock_response = {"quotes": [], "next_page_token": None}

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method and expect exception
        with pytest.raises(Exception, match="No quote data found"):
            quotes_instance.get_historical_quotes(
                "AAPL", start="2024-01-10", end="2024-01-11"
            )

    def test_get_historical_quotes_spread_calculation(self, quotes_instance, mocker):
        """Test that spread is calculated correctly."""
        # Mock response data
        mock_response = {
            "quotes": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "ax": "Q",
                    "ap": 100.00,
                    "as": 100,
                    "bx": "Q",
                    "bp": 99.50,
                    "bs": 200,
                    "c": ["R"],
                    "z": "A",
                }
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = quotes_instance.get_historical_quotes(
            "AAPL", start="2024-01-10", end="2024-01-11"
        )

        # Check spread calculations
        assert result.iloc[0]["spread"] == pytest.approx(0.50)
        assert result.iloc[0]["spread_pct"] == pytest.approx(0.5025, rel=1e-3)

    def test_get_historical_quotes_with_asof(self, quotes_instance, mocker):
        """Test that asof parameter is passed correctly."""
        # Mock response data
        mock_response = {
            "quotes": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "ax": "Q",
                    "ap": 185.50,
                    "as": 100,
                    "bx": "Q",
                    "bp": 185.45,
                    "bs": 200,
                    "c": ["R"],
                    "z": "A",
                }
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call with asof parameter
        quotes_instance.get_historical_quotes(
            "AAPL", start="2024-01-10", end="2024-01-11", asof="2024-01-09"
        )

        # Check that asof was passed
        call_args = mock_request.call_args
        assert call_args[1]["params"]["asof"] == "2024-01-09"
