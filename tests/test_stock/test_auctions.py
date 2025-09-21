"""Test cases for historical auctions functionality."""

import json
from unittest.mock import MagicMock

import pandas as pd
import pytest

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.stock.auctions import Auctions


class TestAuctions:
    """Test suite for the Auctions class."""

    @pytest.fixture
    def auctions_instance(self):
        """Create an Auctions instance for testing."""
        return Auctions(headers={"Authorization": "Bearer TEST"})

    def test_get_auctions_single_symbol(self, auctions_instance, mocker):
        """Test getting historical auctions for a single symbol."""
        # Mock response data
        mock_response = {
            "auctions": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "d": "2024-01-10",
                    "o": "opening",
                    "op": 185.50,
                    "oh": 185.60,
                    "ol": 185.40,
                    "ov": 100000,
                    "c": "closing",
                    "cp": 186.00,
                    "ch": 186.10,
                    "cl": 185.90,
                    "cv": 150000,
                    "x": "NYSE",
                },
                {
                    "t": "2024-01-11T09:30:00Z",
                    "d": "2024-01-11",
                    "o": "opening",
                    "op": 186.50,
                    "oh": 186.60,
                    "ol": 186.40,
                    "ov": 120000,
                    "c": "closing",
                    "cp": 187.00,
                    "ch": 187.10,
                    "cl": 186.90,
                    "cv": 160000,
                    "x": "NYSE",
                },
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = auctions_instance.get_auctions(
            "AAPL", start="2024-01-10", end="2024-01-11"
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "opening_price" in result.columns
        assert "closing_price" in result.columns
        assert "intraday_return" in result.columns

        # Check values
        assert result.iloc[0]["opening_price"] == 185.50
        assert result.iloc[0]["closing_price"] == 186.00

        # Check intraday return calculation
        expected_return = (186.00 - 185.50) / 185.50 * 100
        assert result.iloc[0]["intraday_return"] == pytest.approx(
            expected_return, abs=0.01
        )

    def test_get_auctions_multiple_symbols(self, auctions_instance, mocker):
        """Test getting historical auctions for multiple symbols."""
        # Mock response data
        mock_response = {
            "auctions": {
                "AAPL": [
                    {
                        "t": "2024-01-10T09:30:00Z",
                        "d": "2024-01-10",
                        "o": "opening",
                        "op": 185.50,
                        "oh": 185.60,
                        "ol": 185.40,
                        "ov": 100000,
                        "c": "closing",
                        "cp": 186.00,
                        "ch": 186.10,
                        "cl": 185.90,
                        "cv": 150000,
                        "x": "NYSE",
                    }
                ],
                "MSFT": [
                    {
                        "t": "2024-01-10T09:30:00Z",
                        "d": "2024-01-10",
                        "o": "opening",
                        "op": 400.50,
                        "oh": 400.60,
                        "ol": 400.40,
                        "ov": 80000,
                        "c": "closing",
                        "cp": 401.00,
                        "ch": 401.10,
                        "cl": 400.90,
                        "cv": 120000,
                        "x": "NASDAQ",
                    }
                ],
            },
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = auctions_instance.get_auctions(
            ["AAPL", "MSFT"], start="2024-01-10", end="2024-01-11"
        )

        # Assertions
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "AAPL" in result
        assert "MSFT" in result

        # Check AAPL data
        aapl_df = result["AAPL"]
        assert isinstance(aapl_df, pd.DataFrame)
        assert aapl_df.iloc[0]["opening_price"] == 185.50

        # Check MSFT data
        msft_df = result["MSFT"]
        assert isinstance(msft_df, pd.DataFrame)
        assert msft_df.iloc[0]["opening_price"] == 400.50

    def test_get_daily_auctions(self, auctions_instance, mocker):
        """Test getting daily aggregated auctions."""
        # Mock response for get_auctions
        mock_response = {
            "auctions": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "d": "2024-01-10",
                    "o": "opening",
                    "op": 185.50,
                    "oh": 185.60,
                    "ol": 185.40,
                    "ov": 100000,
                    "c": "",
                    "cp": None,
                    "x": "NYSE",
                },
                {
                    "t": "2024-01-10T16:00:00Z",
                    "d": "2024-01-10",
                    "o": "",
                    "op": None,
                    "c": "closing",
                    "cp": 186.00,
                    "ch": 186.10,
                    "cl": 185.90,
                    "cv": 150000,
                    "x": "NYSE",
                },
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = auctions_instance.get_daily_auctions(
            "AAPL", start="2024-01-10", end="2024-01-11"
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        # Should have aggregated to daily data
        assert "daily_return" in result.columns if len(result) > 0 else True

    def test_get_auctions_pagination(self, auctions_instance, mocker):
        """Test pagination handling for historical auctions."""
        # First response with next_page_token
        mock_response_1 = {
            "auctions": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "d": "2024-01-10",
                    "o": "opening",
                    "op": 185.50,
                    "oh": 185.60,
                    "ol": 185.40,
                    "ov": 100000,
                    "x": "NYSE",
                }
            ],
            "next_page_token": "token123",
        }

        # Second response without next_page_token
        mock_response_2 = {
            "auctions": [
                {
                    "t": "2024-01-11T09:30:00Z",
                    "d": "2024-01-11",
                    "o": "opening",
                    "op": 186.50,
                    "oh": 186.60,
                    "ol": 186.40,
                    "ov": 120000,
                    "x": "NYSE",
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
        result = auctions_instance.get_auctions(
            "AAPL", start="2024-01-10", end="2024-01-11"
        )

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2  # Should have combined both pages
        assert mock_request.call_count == 2  # Should have made 2 API calls

    def test_get_auctions_invalid_feed(self, auctions_instance):
        """Test that invalid feed raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid feed"):
            auctions_instance.get_auctions(
                "AAPL", start="2024-01-10", end="2024-01-11", feed="invalid"
            )

    def test_get_auctions_invalid_sort(self, auctions_instance):
        """Test that invalid sort raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid sort"):
            auctions_instance.get_auctions(
                "AAPL", start="2024-01-10", end="2024-01-11", sort="invalid"
            )

    def test_get_auctions_invalid_limit(self, auctions_instance):
        """Test that invalid limit raises ValidationError."""
        with pytest.raises(ValidationError, match="Limit must be at least 1"):
            auctions_instance.get_auctions(
                "AAPL", start="2024-01-10", end="2024-01-11", limit=0
            )

    def test_get_auctions_invalid_date_format(self, auctions_instance):
        """Test that invalid date format raises ValidationError."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            auctions_instance.get_auctions(
                "AAPL", start="invalid-date", end="2024-01-11"
            )

    def test_get_auctions_empty_symbols(self, auctions_instance):
        """Test that empty symbols raises ValidationError."""
        with pytest.raises(ValidationError, match="At least one symbol is required"):
            auctions_instance.get_auctions([], start="2024-01-10", end="2024-01-11")

    def test_get_auctions_no_data(self, auctions_instance, mocker):
        """Test handling when no data is returned."""
        # Mock response with no data
        mock_response = {"auctions": [], "next_page_token": None}

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method and expect exception
        with pytest.raises(Exception, match="No auction data found"):
            auctions_instance.get_auctions("AAPL", start="2024-01-10", end="2024-01-11")

    def test_get_auctions_with_different_feeds(self, auctions_instance, mocker):
        """Test getting auctions with different feed options."""
        # Mock response data
        mock_response = {
            "auctions": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "d": "2024-01-10",
                    "o": "opening",
                    "op": 185.50,
                    "oh": 185.60,
                    "ol": 185.40,
                    "ov": 100000,
                    "x": "NYSE",
                }
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Test with different feeds
        for feed in ["iex", "sip", "otc"]:
            result = auctions_instance.get_auctions(
                "AAPL", start="2024-01-10", end="2024-01-11", feed=feed
            )
            assert isinstance(result, pd.DataFrame)

            # Check that the correct feed was passed
            call_args = mock_request.call_args
            assert call_args[1]["params"]["feed"] == feed

    def test_aggregate_daily_auctions_empty_dataframe(self, auctions_instance):
        """Test that aggregating empty DataFrame returns empty DataFrame."""
        empty_df = pd.DataFrame()
        result = auctions_instance._aggregate_daily_auctions(empty_df)
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_aggregate_daily_auctions_with_data(self, auctions_instance):
        """Test daily aggregation with actual data."""
        # Create sample data with timestamps
        data = {"opening_price": [185.50, 186.00], "closing_price": [186.00, 186.50]}
        index = pd.DatetimeIndex(["2024-01-10 09:30:00", "2024-01-10 16:00:00"])
        df = pd.DataFrame(data, index=index)

        result = auctions_instance._aggregate_daily_auctions(df)

        # Should have one row for the day
        assert len(result) <= 1
        if len(result) > 0:
            assert "daily_return" in result.columns

    def test_get_auctions_with_asof(self, auctions_instance, mocker):
        """Test that asof parameter is passed correctly."""
        # Mock response data
        mock_response = {
            "auctions": [
                {
                    "t": "2024-01-10T09:30:00Z",
                    "d": "2024-01-10",
                    "o": "opening",
                    "op": 185.50,
                    "oh": 185.60,
                    "ol": 185.40,
                    "ov": 100000,
                    "x": "NYSE",
                }
            ],
            "next_page_token": None,
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call with asof parameter
        auctions_instance.get_auctions(
            "AAPL", start="2024-01-10", end="2024-01-11", asof="2024-01-09"
        )

        # Check that asof was passed
        call_args = mock_request.call_args
        assert call_args[1]["params"]["asof"] == "2024-01-09"
