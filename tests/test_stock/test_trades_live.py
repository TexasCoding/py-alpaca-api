"""Integration tests for Trades API with live data.

These tests require valid Alpaca API credentials and will make real API calls.
Run with: ./test.sh
"""

import os
from datetime import datetime, timedelta

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.models.trade_model import TradeModel, TradesResponse

# Skip all tests if no API credentials
pytestmark = pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_SECRET_KEY"),
    reason="API credentials not available",
)


@pytest.fixture
def alpaca():
    """Create PyAlpacaAPI instance with real credentials."""
    return PyAlpacaAPI(
        api_key=os.environ.get("ALPACA_API_KEY"),
        api_secret=os.environ.get("ALPACA_SECRET_KEY"),
        api_paper=True,
    )


class TestTradesLive:
    """Integration tests for Trades API with live data."""

    def test_get_trades_historical(self, alpaca):
        """Test retrieving historical trades for a symbol."""
        # Use a recent trading day
        end_time = datetime.now()
        # Go back to previous trading day to ensure market was open
        if end_time.weekday() == 0:  # Monday
            start_time = end_time - timedelta(days=3)  # Friday
        elif end_time.weekday() == 6:  # Sunday
            start_time = end_time - timedelta(days=2)  # Friday
        else:
            start_time = end_time - timedelta(days=1)

        # Format times in RFC-3339
        start = start_time.replace(hour=14, minute=0, second=0).isoformat() + "Z"
        end = start_time.replace(hour=14, minute=30, second=0).isoformat() + "Z"

        try:
            result = alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start=start,
                end=end,
                limit=10,
            )

            assert isinstance(result, TradesResponse)
            assert result.symbol == "AAPL"

            if result.trades:
                # Check first trade
                trade = result.trades[0]
                assert isinstance(trade, TradeModel)
                assert trade.symbol == "AAPL"
                assert trade.price > 0
                assert trade.size > 0
                assert trade.exchange
                assert trade.timestamp

                print(f"\nFound {len(result.trades)} trades for AAPL")
                print(
                    f"First trade: ${trade.price} x {trade.size} at {trade.timestamp}"
                )

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_get_latest_trade(self, alpaca):
        """Test retrieving the latest trade for a symbol."""
        try:
            trade = alpaca.stock.trades.get_latest_trade("AAPL")

            assert isinstance(trade, TradeModel)
            assert trade.symbol == "AAPL"
            assert trade.price > 0
            assert trade.size > 0
            assert trade.exchange
            assert trade.timestamp

            print(f"\nLatest AAPL trade: ${trade.price} x {trade.size}")
            print(f"  Exchange: {trade.exchange}")
            print(f"  Time: {trade.timestamp}")

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_get_trades_with_feed(self, alpaca):
        """Test retrieving trades with different feed types."""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)

        start = start_time.isoformat() + "Z"
        end = end_time.isoformat() + "Z"

        # Try IEX feed (usually available for free tier)
        try:
            result = alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start=start,
                end=end,
                limit=5,
                feed="iex",
            )

            assert isinstance(result, TradesResponse)
            print(f"\nIEX feed returned {len(result.trades)} trades")

        except APIRequestError as e:
            if e.status_code == 403:
                print("\nIEX feed not available (subscription required)")
            elif e.status_code == 429:
                pytest.skip("Rate limit reached")
            else:
                raise

    def test_get_trades_multi(self, alpaca):
        """Test retrieving trades for multiple symbols."""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)

        start = start_time.isoformat() + "Z"
        end = end_time.isoformat() + "Z"

        try:
            result = alpaca.stock.trades.get_trades_multi(
                symbols=["AAPL", "MSFT", "GOOGL"],
                start=start,
                end=end,
                limit=5,
            )

            assert isinstance(result, dict)

            for symbol in ["AAPL", "MSFT", "GOOGL"]:
                if symbol in result:
                    assert isinstance(result[symbol], TradesResponse)
                    assert result[symbol].symbol == symbol

                    if result[symbol].trades:
                        print(f"\n{symbol}: {len(result[symbol].trades)} trades")
                        first_trade = result[symbol].trades[0]
                        print(f"  First trade: ${first_trade.price}")

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_get_latest_trades_multi(self, alpaca):
        """Test getting latest trades for multiple symbols."""
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        try:
            result = alpaca.stock.trades.get_latest_trades_multi(symbols)

            assert isinstance(result, dict)

            print("\nLatest trades for multiple symbols:")
            for symbol in symbols:
                if symbol in result:
                    trade = result[symbol]
                    assert isinstance(trade, TradeModel)
                    assert trade.symbol == symbol
                    assert trade.price > 0

                    print(f"  {symbol}: ${trade.price:,.2f} x {trade.size}")

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_pagination(self, alpaca):
        """Test pagination with large result sets."""
        # Use a wider time range to get more trades
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)

        start = start_time.isoformat() + "Z"
        end = end_time.isoformat() + "Z"

        try:
            # First request with small limit
            first_page = alpaca.stock.trades.get_trades(
                symbol="SPY",  # SPY typically has high volume
                start=start,
                end=end,
                limit=100,
            )

            assert isinstance(first_page, TradesResponse)

            if first_page.next_page_token:
                # Get next page
                second_page = alpaca.stock.trades.get_trades(
                    symbol="SPY",
                    start=start,
                    end=end,
                    limit=100,
                    page_token=first_page.next_page_token,
                )

                assert isinstance(second_page, TradesResponse)
                print("\nPagination test:")
                print(f"  First page: {len(first_page.trades)} trades")
                print(f"  Second page: {len(second_page.trades)} trades")
                print(f"  Has more pages: {second_page.next_page_token is not None}")
            else:
                print(f"\nOnly one page of results ({len(first_page.trades)} trades)")

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_get_all_trades(self, alpaca):
        """Test getting all trades with automatic pagination."""
        # Use a short time window to avoid too much data
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=5)

        start = start_time.isoformat() + "Z"
        end = end_time.isoformat() + "Z"

        try:
            all_trades = alpaca.stock.trades.get_all_trades(
                symbol="AAPL",
                start=start,
                end=end,
            )

            assert isinstance(all_trades, list)

            if all_trades:
                assert all(isinstance(trade, TradeModel) for trade in all_trades)
                assert all(trade.symbol == "AAPL" for trade in all_trades)

                print(f"\nRetrieved {len(all_trades)} total trades across all pages")

                # Check trades are in chronological order
                # Parse timestamps to handle different precision levels
                parsed_timestamps = [
                    datetime.fromisoformat(trade.timestamp.replace("Z", "+00:00"))
                    for trade in all_trades
                ]
                assert parsed_timestamps == sorted(
                    parsed_timestamps
                ), "Trades are not in chronological order"
                print("  Trades are in chronological order ✓")

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_error_handling(self, alpaca):
        """Test error handling for invalid requests."""
        # Test with invalid symbol
        with pytest.raises(APIRequestError):
            alpaca.stock.trades.get_latest_trade("INVALID_SYMBOL_XYZ")

        # Test with invalid date range
        with pytest.raises(ValidationError):
            alpaca.stock.trades.get_trades(
                symbol="AAPL",
                start="invalid_date",
                end="2024-01-15T15:00:00Z",
            )

        # Test with too many symbols
        with pytest.raises(ValidationError):
            alpaca.stock.trades.get_trades_multi(
                symbols=["AAPL"] * 101,  # Over 100 symbol limit
                start="2024-01-15T14:00:00Z",
                end="2024-01-15T15:00:00Z",
            )

    def test_trade_conditions(self, alpaca):
        """Test that trade conditions are properly captured."""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)

        start = start_time.isoformat() + "Z"
        end = end_time.isoformat() + "Z"

        try:
            result = alpaca.stock.trades.get_trades(
                symbol="SPY",
                start=start,
                end=end,
                limit=100,
            )

            if result.trades:
                # Check for trades with conditions
                trades_with_conditions = [t for t in result.trades if t.conditions]

                if trades_with_conditions:
                    print(
                        f"\nFound {len(trades_with_conditions)} trades with conditions"
                    )
                    # Print some example conditions
                    unique_conditions = set()
                    for trade in trades_with_conditions:
                        if trade.conditions:
                            unique_conditions.update(trade.conditions)

                    print(f"  Unique conditions seen: {sorted(unique_conditions)}")

        except APIRequestError as e:
            if e.status_code in [403, 429]:
                pytest.skip(f"API rate limit or subscription issue: {e}")
            raise

    def test_asof_parameter(self, alpaca):
        """Test the as-of parameter for historical point-in-time data."""
        # Skip this test as asof requires historical dates and proper subscription
        pytest.skip(
            "As-of parameter requires specific historical dates and subscription"
        )


if __name__ == "__main__":
    # Allow running this file directly for testing
    pytest.main([__file__, "-v"])
