"""Test cases for latest bars functionality in history module."""

import json
from unittest.mock import MagicMock

import pandas as pd
import pytest

from py_alpaca_api.stock.history import History


class TestLatestBars:
    """Test suite for the get_latest_bars method."""

    @pytest.fixture
    def mock_history(self, mocker):
        """Create a mock History instance with mocked dependencies."""
        mock_asset = mocker.Mock()
        mock_asset.get.return_value = mocker.Mock(
            tradable=True, asset_class="us_equity"
        )

        history = History(
            headers={"Authorization": "Bearer TEST"},
            data_url="https://data.alpaca.markets/v2",
            asset=mock_asset,
        )
        return history

    def test_get_latest_bars_single_symbol(self, mock_history, mocker):
        """Test getting latest bar for a single symbol."""
        # Mock response data
        mock_response = {
            "bars": {
                "AAPL": {
                    "t": "2024-01-10T15:59:00Z",
                    "o": 185.50,
                    "h": 186.00,
                    "l": 185.25,
                    "c": 185.75,
                    "v": 1000000,
                    "n": 5000,
                    "vw": 185.60,
                }
            }
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = mock_history.get_latest_bars("AAPL")

        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["open"] == 185.50
        assert result.iloc[0]["high"] == 186.00
        assert result.iloc[0]["low"] == 185.25
        assert result.iloc[0]["close"] == 185.75
        assert result.iloc[0]["volume"] == 1000000

        # Verify API call
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["method"] == "GET"
        assert "bars/latest" in call_args[1]["url"]
        assert call_args[1]["params"]["symbols"] == "AAPL"

    def test_get_latest_bars_multiple_symbols(self, mock_history, mocker):
        """Test getting latest bars for multiple symbols."""
        # Mock response data
        mock_response = {
            "bars": {
                "AAPL": {
                    "t": "2024-01-10T15:59:00Z",
                    "o": 185.50,
                    "h": 186.00,
                    "l": 185.25,
                    "c": 185.75,
                    "v": 1000000,
                    "n": 5000,
                    "vw": 185.60,
                },
                "MSFT": {
                    "t": "2024-01-10T15:59:00Z",
                    "o": 400.50,
                    "h": 401.00,
                    "l": 400.00,
                    "c": 400.75,
                    "v": 500000,
                    "n": 3000,
                    "vw": 400.60,
                },
            }
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = mock_history.get_latest_bars(["AAPL", "MSFT"])

        # Assertions
        assert isinstance(result, dict)
        assert len(result) == 2
        assert "AAPL" in result
        assert "MSFT" in result

        # Check AAPL data
        aapl_df = result["AAPL"]
        assert isinstance(aapl_df, pd.DataFrame)
        assert aapl_df.iloc[0]["close"] == 185.75

        # Check MSFT data
        msft_df = result["MSFT"]
        assert isinstance(msft_df, pd.DataFrame)
        assert msft_df.iloc[0]["close"] == 400.75

    def test_get_latest_bars_invalid_feed(self, mock_history):
        """Test that invalid feed raises ValueError."""
        with pytest.raises(ValueError, match="Invalid feed"):
            mock_history.get_latest_bars("AAPL", feed="invalid")

    def test_get_latest_bars_empty_symbols(self, mock_history):
        """Test that empty symbols list raises ValueError."""
        with pytest.raises(ValueError, match="At least one symbol is required"):
            mock_history.get_latest_bars([])

    def test_get_latest_bars_no_data(self, mock_history, mocker):
        """Test handling when no data is returned."""
        # Mock response with no data
        mock_response = {"bars": {}}

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method and expect exception
        with pytest.raises(Exception, match="No latest bar data found"):
            mock_history.get_latest_bars("AAPL")

    def test_get_latest_bars_with_different_feeds(self, mock_history, mocker):
        """Test getting latest bars with different feed options."""
        # Mock response data
        mock_response = {
            "bars": {
                "AAPL": {
                    "t": "2024-01-10T15:59:00Z",
                    "o": 185.50,
                    "h": 186.00,
                    "l": 185.25,
                    "c": 185.75,
                    "v": 1000000,
                    "n": 5000,
                    "vw": 185.60,
                }
            }
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Test with different feeds
        for feed in ["iex", "sip", "otc"]:
            result = mock_history.get_latest_bars("AAPL", feed=feed)
            assert isinstance(result, pd.DataFrame)

            # Check that the correct feed was passed
            call_args = mock_request.call_args
            assert call_args[1]["params"]["feed"] == feed

    def test_get_latest_bars_currency_parameter(self, mock_history, mocker):
        """Test that currency parameter is passed correctly."""
        # Mock response data
        mock_response = {
            "bars": {
                "AAPL": {
                    "t": "2024-01-10T15:59:00Z",
                    "o": 185.50,
                    "h": 186.00,
                    "l": 185.25,
                    "c": 185.75,
                    "v": 1000000,
                    "n": 5000,
                    "vw": 185.60,
                }
            }
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call with EUR currency
        mock_history.get_latest_bars("AAPL", currency="EUR")

        # Check that currency was passed
        call_args = mock_request.call_args
        assert call_args[1]["params"]["currency"] == "EUR"

    def test_get_latest_bars_column_mapping(self, mock_history, mocker):
        """Test that columns are properly renamed."""
        # Mock response data
        mock_response = {
            "bars": {
                "AAPL": {
                    "t": "2024-01-10T15:59:00Z",
                    "o": 185.50,
                    "h": 186.00,
                    "l": 185.25,
                    "c": 185.75,
                    "v": 1000000,
                    "n": 5000,
                    "vw": 185.60,
                }
            }
        }

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = MagicMock(text=json.dumps(mock_response))

        # Call the method
        result = mock_history.get_latest_bars("AAPL")

        # Check column names
        expected_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "trade_count",
            "vwap",
        ]
        for col in expected_columns:
            assert col in result.columns

        # Original column names should not exist
        original_columns = ["o", "h", "l", "c", "v", "n", "vw"]
        for col in original_columns:
            assert col not in result.columns
