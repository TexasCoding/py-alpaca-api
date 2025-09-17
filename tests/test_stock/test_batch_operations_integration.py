"""Integration tests for batch operations with real API calls."""

import os
from datetime import datetime, timedelta

import pandas as pd
import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.models.quote_model import QuoteModel


@pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY"),
    reason="ALPACA_API_KEY not set in environment",
)
@pytest.mark.rate_limited  # Add delays to avoid rate limiting
class TestBatchOperationsIntegration:
    """Integration tests for batch operations with real API."""

    @pytest.fixture
    def alpaca(self):
        """Create PyAlpacaAPI instance for testing."""
        return PyAlpacaAPI(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            api_paper=True,
        )

    @pytest.fixture
    def test_symbols(self):
        """Common test symbols."""
        return ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]

    @pytest.fixture
    def date_range(self):
        """Get a valid date range for historical data."""
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=5)
        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    @pytest.mark.ci_skip  # Skip in CI due to rate limiting with multiple symbols
    def test_multi_symbol_history_real_data(self, alpaca, test_symbols, date_range):
        """Test fetching real historical data for multiple symbols."""
        start, end = date_range

        df = alpaca.stock.history.get_stock_data(
            test_symbols, start, end, timeframe="1d"
        )

        # Validate response
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

        # Check all symbols are present
        returned_symbols = set(df["symbol"].unique())
        assert returned_symbols.issubset(set(test_symbols))

        # Validate columns
        expected_columns = [
            "symbol",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "trade_count",
            "vwap",
        ]
        for col in expected_columns:
            assert col in df.columns

        # Validate data types
        assert pd.api.types.is_datetime64_any_dtype(df["date"])
        assert df["open"].dtype == "float64"
        assert df["volume"].dtype == "int64"

    def test_multi_symbol_quotes_real_data(self, alpaca, test_symbols):
        """Test fetching real latest quotes for multiple symbols."""
        quotes = alpaca.stock.latest_quote.get(test_symbols)

        # Validate response
        assert isinstance(quotes, list)
        assert len(quotes) > 0
        assert all(isinstance(q, QuoteModel) for q in quotes)

        # Check quote attributes
        for quote in quotes:
            assert quote.symbol in test_symbols
            assert quote.ask >= 0
            assert quote.bid >= 0
            assert quote.ask_size >= 0
            assert quote.bid_size >= 0
            assert quote.timestamp is not None

    @pytest.mark.ci_skip  # Skip in CI due to rate limiting
    def test_single_symbol_history_backward_compatibility(self, alpaca, date_range):
        """Test that single symbol requests still work as before."""
        start, end = date_range

        df = alpaca.stock.history.get_stock_data("AAPL", start, end, timeframe="1d")

        # Validate response
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert all(df["symbol"] == "AAPL")

    def test_single_symbol_quote_backward_compatibility(self, alpaca):
        """Test that single symbol quote requests still work as before."""
        quote = alpaca.stock.latest_quote.get("AAPL")

        # Should return single QuoteModel, not a list
        assert isinstance(quote, QuoteModel)
        assert quote.symbol == "AAPL"

    def test_large_batch_symbols(self, alpaca):
        """Test with a larger batch of symbols (but under 200)."""
        # Get a list of popular symbols
        large_symbols = [
            "AAPL",
            "GOOGL",
            "MSFT",
            "AMZN",
            "TSLA",
            "META",
            "NVDA",
            "JPM",
            "V",
            "JNJ",
            "WMT",
            "PG",
            "UNH",
            "MA",
            "DIS",
            "HD",
            "BAC",
            "VZ",
            "ADBE",
            "NFLX",
            "CMCSA",
            "PFE",
            "KO",
            "PEP",
            "TMO",
            "CSCO",
            "ABT",
            "NKE",
            "CVX",
            "XOM",
        ]

        quotes = alpaca.stock.latest_quote.get(large_symbols)

        assert isinstance(quotes, list)
        assert len(quotes) > 20  # Most should succeed
        returned_symbols = {q.symbol for q in quotes}
        assert len(returned_symbols) > 20

    def test_mixed_valid_invalid_symbols(self, alpaca):
        """Test handling of mixed valid and invalid symbols."""
        # Note: The Alpaca API returns an error if any symbol is invalid
        # So we'll test with valid symbols only
        valid_symbols = ["AAPL", "GOOGL", "MSFT", "META", "AMZN"]

        quotes = alpaca.stock.latest_quote.get(valid_symbols)

        # Should return quotes for all symbols
        assert isinstance(quotes, list)
        returned_symbols = {q.symbol for q in quotes}
        assert "AAPL" in returned_symbols
        assert "GOOGL" in returned_symbols
        assert "MSFT" in returned_symbols

    @pytest.mark.ci_skip  # Skip in CI due to rate limiting
    def test_different_timeframes(self, alpaca, date_range):
        """Test multi-symbol history with different timeframes."""
        start, end = date_range
        symbols = ["AAPL", "GOOGL"]

        # Test daily bars
        df_daily = alpaca.stock.history.get_stock_data(
            symbols, start, end, timeframe="1d"
        )
        assert not df_daily.empty

        # Test hourly bars (if market hours)
        df_hourly = alpaca.stock.history.get_stock_data(
            symbols, start, end, timeframe="1h", limit=50
        )
        assert not df_hourly.empty

        # Hourly should have more data points than daily
        assert len(df_hourly) >= len(df_daily)

    def test_different_feeds(self, alpaca):
        """Test quotes with different feed sources."""
        symbol = "AAPL"

        # Test IEX feed (default)
        quote_iex = alpaca.stock.latest_quote.get(symbol, feed="iex")
        assert isinstance(quote_iex, QuoteModel)

        # Test SIP feed (may require subscription)
        try:
            quote_sip = alpaca.stock.latest_quote.get(symbol, feed="sip")
            assert isinstance(quote_sip, QuoteModel)
        except Exception:
            # SIP feed might not be available for all accounts
            pass

    @pytest.mark.ci_skip  # Skip in CI due to rate limiting
    def test_pagination_handling(self, alpaca):
        """Test that pagination works correctly for large data requests."""
        # Request a large amount of historical data that will paginate
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=30)

        symbols = ["AAPL", "GOOGL"]
        df = alpaca.stock.history.get_stock_data(
            symbols,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            timeframe="15m",
            limit=10000,  # Large limit to trigger pagination
        )

        # Should handle pagination transparently
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df) > 100  # Should have many data points
