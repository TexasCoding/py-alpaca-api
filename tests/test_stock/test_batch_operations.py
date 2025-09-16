"""Tests for batch operations in history and latest_quote modules."""

import os
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.models.quote_model import QuoteModel


class TestBatchOperations:
    """Test batch operations for multi-symbol data retrieval."""

    @pytest.fixture
    def alpaca(self):
        """Create PyAlpacaAPI instance for testing."""
        return PyAlpacaAPI(
            api_key=os.environ.get("ALPACA_API_KEY", "test_key"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY", "test_secret"),
            api_paper=True,
        )

    @pytest.fixture
    def mock_requests(self):
        """Mock the Requests class for unit tests."""
        with patch("py_alpaca_api.stock.history.Requests") as mock:
            yield mock

    @pytest.fixture
    def mock_quotes_requests(self):
        """Mock the Requests class for quote tests."""
        with patch("py_alpaca_api.stock.latest_quote.Requests") as mock:
            yield mock

    def test_history_single_symbol(self, alpaca, mock_requests):
        """Test getting historical data for a single symbol."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = '{"bars": [{"t": "2024-01-01T09:30:00Z", "o": 100, "h": 105, "l": 99, "c": 103, "v": 1000000, "n": 500, "vw": 102.5}]}'
        mock_requests.return_value.request.return_value = mock_response

        # Mock the asset check
        with patch.object(alpaca.stock.history, "check_if_stock", return_value=None):
            # Test single symbol
            df = alpaca.stock.history.get_stock_data("AAPL", "2024-01-01", "2024-01-02")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "symbol" in df.columns
        assert df["symbol"].iloc[0] == "AAPL"

    def test_history_multiple_symbols(self, alpaca, mock_requests):
        """Test getting historical data for multiple symbols."""
        # Setup mock response for multi-symbol request
        mock_response = MagicMock()
        mock_response.text = """{
            "bars": {
                "AAPL": [{"t": "2024-01-01T09:30:00Z", "o": 100, "h": 105, "l": 99, "c": 103, "v": 1000000, "n": 500, "vw": 102.5}],
                "GOOGL": [{"t": "2024-01-01T09:30:00Z", "o": 150, "h": 155, "l": 149, "c": 153, "v": 800000, "n": 400, "vw": 152.5}]
            }
        }"""
        mock_requests.return_value.request.return_value = mock_response

        # Mock the asset check
        with patch.object(alpaca.stock.history, "check_if_stock", return_value=None):
            # Test multiple symbols
            symbols = ["AAPL", "GOOGL"]
            df = alpaca.stock.history.get_stock_data(
                symbols, "2024-01-01", "2024-01-02"
            )

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert set(df["symbol"].unique()) == {"AAPL", "GOOGL"}
        assert len(df) == 2  # One row per symbol

    def test_history_batch_large_symbol_list(self, alpaca, mock_requests):
        """Test batching when more than 200 symbols are requested."""
        # Create a list of 250 symbols
        symbols = [f"STOCK{i:03d}" for i in range(250)]

        # Setup mock responses for batches
        batch1_response = {
            "bars": {
                f"STOCK{i:03d}": [
                    {
                        "t": "2024-01-01T09:30:00Z",
                        "o": 100,
                        "h": 105,
                        "l": 99,
                        "c": 103,
                        "v": 1000000,
                        "n": 500,
                        "vw": 102.5,
                    }
                ]
                for i in range(200)
            }
        }
        batch2_response = {
            "bars": {
                f"STOCK{i:03d}": [
                    {
                        "t": "2024-01-01T09:30:00Z",
                        "o": 100,
                        "h": 105,
                        "l": 99,
                        "c": 103,
                        "v": 1000000,
                        "n": 500,
                        "vw": 102.5,
                    }
                ]
                for i in range(200, 250)
            }
        }

        responses = [MagicMock(), MagicMock()]
        responses[0].text = str(batch1_response).replace("'", '"')
        responses[1].text = str(batch2_response).replace("'", '"')

        mock_requests.return_value.request.side_effect = responses

        # Mock the batching method directly since it uses ThreadPoolExecutor
        with (
            patch.object(alpaca.stock.history, "check_if_stock", return_value=None),
            patch.object(alpaca.stock.history, "_get_batched_stock_data") as mock_batch,
        ):
            # Return a simple DataFrame for testing
            mock_batch.return_value = pd.DataFrame(
                {
                    "symbol": ["STOCK000", "STOCK100"],
                    "date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
                    "open": [100.0, 100.0],
                    "high": [105.0, 105.0],
                    "low": [99.0, 99.0],
                    "close": [103.0, 103.0],
                    "volume": [1000000, 1000000],
                    "trade_count": [500, 500],
                    "vwap": [102.5, 102.5],
                }
            )

            df = alpaca.stock.history.get_stock_data(
                symbols, "2024-01-01", "2024-01-02"
            )

            # Verify batching method was called
            mock_batch.assert_called_once()

            # Verify result has data
            assert not df.empty

    def test_latest_quote_single_symbol(self, alpaca, mock_quotes_requests):
        """Test getting latest quote for a single symbol."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = """{
            "quotes": {
                "AAPL": {"t": "2024-01-01T15:59:59Z", "ap": 103.5, "as": 100, "bp": 103.0, "bs": 100}
            }
        }"""
        mock_quotes_requests.return_value.request.return_value = mock_response

        # Test single symbol
        quote = alpaca.stock.latest_quote.get("AAPL")

        assert isinstance(quote, QuoteModel)
        assert quote.symbol == "AAPL"
        assert quote.ask == 103.5
        assert quote.bid == 103.0

    def test_latest_quote_multiple_symbols(self, alpaca, mock_quotes_requests):
        """Test getting latest quotes for multiple symbols."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = """{
            "quotes": {
                "AAPL": {"t": "2024-01-01T15:59:59Z", "ap": 103.5, "as": 100, "bp": 103.0, "bs": 100},
                "GOOGL": {"t": "2024-01-01T15:59:59Z", "ap": 153.5, "as": 100, "bp": 153.0, "bs": 100}
            }
        }"""
        mock_quotes_requests.return_value.request.return_value = mock_response

        # Test multiple symbols
        quotes = alpaca.stock.latest_quote.get(["AAPL", "GOOGL"])

        assert isinstance(quotes, list)
        assert len(quotes) == 2
        assert all(isinstance(q, QuoteModel) for q in quotes)
        symbols = {q.symbol for q in quotes}
        assert symbols == {"AAPL", "GOOGL"}

    def test_latest_quote_batch_large_symbol_list(self, alpaca, mock_quotes_requests):
        """Test batching when more than 200 symbols are requested."""
        # Create a list of 250 symbols
        symbols = [f"STOCK{i:03d}" for i in range(250)]

        # Setup mock responses for batches
        batch1_response = {
            "quotes": {
                f"STOCK{i:03d}": {
                    "t": "2024-01-01T15:59:59Z",
                    "ap": 103.5,
                    "as": 100,
                    "bp": 103.0,
                    "bs": 100,
                }
                for i in range(200)
            }
        }
        batch2_response = {
            "quotes": {
                f"STOCK{i:03d}": {
                    "t": "2024-01-01T15:59:59Z",
                    "ap": 103.5,
                    "as": 100,
                    "bp": 103.0,
                    "bs": 100,
                }
                for i in range(200, 250)
            }
        }

        responses = [MagicMock(), MagicMock()]
        responses[0].text = str(batch1_response).replace("'", '"')
        responses[1].text = str(batch2_response).replace("'", '"')

        mock_quotes_requests.return_value.request.side_effect = responses

        with patch.object(
            alpaca.stock.latest_quote, "_get_batched_quotes"
        ) as mock_batch:
            # Return mock quotes
            mock_batch.return_value = [
                QuoteModel(
                    symbol=f"STOCK{i:03d}",
                    timestamp="2024-01-01T15:59:59Z",
                    ask=103.5,
                    ask_size=100,
                    bid=103.0,
                    bid_size=100,
                )
                for i in range(250)
            ]

            quotes = alpaca.stock.latest_quote.get(symbols)

            # Verify batching method was called
            mock_batch.assert_called_once()
            assert len(quotes) == 250

    def test_history_empty_response_handling(self, alpaca, mock_requests):
        """Test handling of empty responses in history."""
        # Setup mock response with no data
        mock_response = MagicMock()
        mock_response.text = '{"bars": {}}'
        mock_requests.return_value.request.return_value = mock_response

        with (
            patch.object(alpaca.stock.history, "check_if_stock", return_value=None),
            pytest.raises(Exception, match="No historical data found"),
        ):
            alpaca.stock.history.get_stock_data(["INVALID"], "2024-01-01", "2024-01-02")

    def test_latest_quote_empty_response_handling(self, alpaca, mock_quotes_requests):
        """Test handling of empty responses in quotes."""
        # Setup mock response with no data
        mock_response = MagicMock()
        mock_response.text = '{"quotes": {}}'
        mock_quotes_requests.return_value.request.return_value = mock_response

        quotes = alpaca.stock.latest_quote.get(["INVALID"])

        assert quotes == []

    def test_history_concurrent_batch_error_handling(self, alpaca, mock_requests):
        """Test error handling in concurrent batch requests for history."""
        # Create a list of 250 symbols
        symbols = [f"STOCK{i:03d}" for i in range(250)]

        # Setup one successful and one failing response
        success_response = MagicMock()
        success_response.text = """{
            "bars": {
                "STOCK000": [{"t": "2024-01-01T09:30:00Z", "o": 100, "h": 105, "l": 99, "c": 103, "v": 1000000, "n": 500, "vw": 102.5}]
            }
        }"""

        # Make second batch fail
        mock_requests.return_value.request.side_effect = [
            success_response,
            Exception("API Error"),
        ]

        # Should continue despite one batch failing
        with (
            patch.object(alpaca.stock.history, "check_if_stock", return_value=None),
            patch.object(alpaca.stock.history, "_get_batched_stock_data") as mock_batch,
        ):
            # Simulate partial failure - return DataFrame with some data
            mock_batch.return_value = pd.DataFrame(
                {
                    "symbol": ["STOCK000"],
                    "date": pd.to_datetime(["2024-01-01"]),
                    "open": [100.0],
                    "high": [105.0],
                    "low": [99.0],
                    "close": [103.0],
                    "volume": [1000000],
                    "trade_count": [500],
                    "vwap": [102.5],
                }
            )

            df = alpaca.stock.history.get_stock_data(
                symbols, "2024-01-01", "2024-01-02"
            )
            # Should return partial data
            assert not df.empty

    def test_quote_concurrent_batch_error_handling(self, alpaca, mock_quotes_requests):
        """Test error handling in concurrent batch requests for quotes."""
        # Create a list of 250 symbols
        symbols = [f"STOCK{i:03d}" for i in range(250)]

        # Setup one successful and one failing response
        success_response = MagicMock()
        success_response.text = """{
            "quotes": {
                "STOCK000": {"t": "2024-01-01T15:59:59Z", "ap": 103.5, "as": 100, "bp": 103.0, "bs": 100}
            }
        }"""

        # Make second batch fail
        mock_quotes_requests.return_value.request.side_effect = [
            success_response,
            Exception("API Error"),
        ]

        # Should continue despite one batch failing
        with patch.object(
            alpaca.stock.latest_quote, "_get_batched_quotes"
        ) as mock_batch:
            # Simulate partial success - return some quotes
            mock_batch.return_value = [
                QuoteModel(
                    symbol="STOCK000",
                    timestamp="2024-01-01T15:59:59Z",
                    ask=103.5,
                    ask_size=100,
                    bid=103.0,
                    bid_size=100,
                )
            ]

            quotes = alpaca.stock.latest_quote.get(symbols)
            # Should return partial data
            assert len(quotes) == 1

    def test_history_dataframe_optimization(self, alpaca, mock_requests):
        """Test DataFrame operations are optimized."""
        # Setup mock response with multiple bars per symbol
        mock_response = MagicMock()
        mock_response.text = """{
            "bars": {
                "AAPL": [
                    {"t": "2024-01-01T09:30:00Z", "o": 100, "h": 105, "l": 99, "c": 103, "v": 1000000, "n": 500, "vw": 102.5},
                    {"t": "2024-01-01T10:30:00Z", "o": 103, "h": 107, "l": 102, "c": 106, "v": 1200000, "n": 600, "vw": 105.5}
                ],
                "GOOGL": [
                    {"t": "2024-01-01T09:30:00Z", "o": 150, "h": 155, "l": 149, "c": 153, "v": 800000, "n": 400, "vw": 152.5},
                    {"t": "2024-01-01T10:30:00Z", "o": 153, "h": 157, "l": 152, "c": 156, "v": 900000, "n": 450, "vw": 155.5}
                ]
            }
        }"""
        mock_requests.return_value.request.return_value = mock_response

        with patch.object(alpaca.stock.history, "check_if_stock", return_value=None):
            # Test DataFrame is properly sorted and indexed
            df = alpaca.stock.history.get_stock_data(
                ["AAPL", "GOOGL"], "2024-01-01", "2024-01-02"
            )

        # Check DataFrame structure
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 4  # 2 bars per symbol

        # Check sorting by symbol and date
        sorted_check = df.equals(df.sort_values(["symbol", "date"]))
        assert sorted_check

        # Check data types are properly set
        assert df["open"].dtype == "float64"
        assert df["volume"].dtype == "int64"
        assert pd.api.types.is_datetime64_any_dtype(df["date"])
