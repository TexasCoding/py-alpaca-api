from __future__ import annotations

import os
from unittest.mock import Mock

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError
from py_alpaca_api.http.feed_manager import (
    FeedConfig,
    FeedManager,
    FeedType,
    SubscriptionLevel,
)


@pytest.fixture
def alpaca():
    """Create PyAlpacaAPI client for testing."""
    api_key = os.getenv("ALPACA_API_KEY")
    api_secret = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not api_secret:
        pytest.skip("No API credentials found")

    return PyAlpacaAPI(
        api_key=api_key,
        api_secret=api_secret,
        api_paper=True,
    )


@pytest.fixture
def feed_manager():
    """Create a feed manager for testing."""
    return FeedManager()


@pytest.mark.rate_limited
class TestFeedManagerIntegration:
    """Integration tests for feed manager with live API."""

    def test_detect_subscription_level_with_live_api(self, alpaca, feed_manager):
        """Test detecting subscription level with live API."""
        # Create a mock client that wraps the real client
        mock_client = Mock()

        # Try to get a quote with SIP feed to test subscription
        try:
            _ = alpaca.stock.latest_quote.get("AAPL", feed="sip")
            # If we got here, SIP is available
            mock_client._make_request.return_value = Mock(status_code=200)
        except APIRequestError as e:
            # SIP not available
            if "subscription" in str(e).lower() or "feed" in str(e).lower():
                mock_client._make_request.side_effect = e
            else:
                # Different error, skip test
                pytest.skip(f"Unexpected error: {e}")

        # Detect subscription level
        level = feed_manager.detect_subscription_level(mock_client)

        assert level in [SubscriptionLevel.BASIC, SubscriptionLevel.UNLIMITED]
        assert feed_manager._detected_subscription_level == level

    def test_feed_fallback_with_live_api(self, alpaca):
        """Test feed fallback behavior with live API."""
        # Try to get quotes with different feeds
        feeds_tested = []
        successful_feed = None

        for feed_type in [FeedType.SIP, FeedType.IEX]:
            try:
                _ = alpaca.stock.latest_quote.get("AAPL", feed=feed_type.value)
                feeds_tested.append((feed_type, True))
                successful_feed = feed_type
                break
            except APIRequestError:
                feeds_tested.append((feed_type, False))
                continue

        # At least one feed should work
        assert successful_feed is not None, f"No feeds worked: {feeds_tested}"

    @pytest.mark.ci_skip  # Skip in CI due to heavy rate limiting
    def test_feed_manager_with_bars_endpoint(self, alpaca):
        """Test feed manager with bars endpoint."""
        manager = FeedManager()

        # Test with bars endpoint
        feed = manager.get_feed("bars")
        assert feed in ["sip", "iex", "otc"]

        # Try to fetch bars with the suggested feed
        try:
            bars = alpaca.stock.history.get_stock_data(
                symbol="AAPL",
                start="2024-01-01",
                end="2024-12-31",
                timeframe="1d",
                limit=10,
                feed=feed,
            )
            # If successful, feed is appropriate
            assert bars is not None
        except APIRequestError as e:
            # Feed not available, manager should handle this
            alternative = manager.handle_feed_error("bars", feed, e, symbol="AAPL")
            if alternative:
                # Try with alternative feed
                bars = alpaca.stock.history.get_stock_data(
                    symbol="AAPL",
                    start="2024-01-01",
                    end="2024-12-31",
                    timeframe="1d",
                    limit=10,
                    feed=alternative,
                )
                assert bars is not None

    def test_feed_manager_with_quotes_endpoint(self, alpaca):
        """Test feed manager with quotes endpoint."""
        manager = FeedManager()

        # Test with quotes endpoint
        feed = manager.get_feed("latest/quotes")
        assert feed in ["sip", "iex", "otc"]

        # Try to fetch quote with the suggested feed
        try:
            quote = alpaca.stock.latest_quote.get("AAPL", feed=feed)
            assert quote is not None
        except APIRequestError as e:
            # Feed not available, manager should handle this
            alternative = manager.handle_feed_error(
                "latest/quotes", feed, e, symbol="AAPL"
            )
            if alternative:
                # Try with alternative feed
                quote = alpaca.stock.latest_quote.get("AAPL", feed=alternative)
                assert quote is not None

    def test_feed_manager_with_trades_endpoint(self, alpaca):
        """Test feed manager with trades endpoint."""
        manager = FeedManager()

        # Test with trades endpoint
        feed = manager.get_feed("trades")
        assert feed in ["sip", "iex", "otc"]

        # Try to fetch trades with the suggested feed
        try:
            trades = alpaca.stock.trades.get_latest_trade("AAPL", feed=feed)
            assert trades is not None
        except APIRequestError as e:
            # Feed not available, manager should handle this
            alternative = manager.handle_feed_error("trades", feed, e, symbol="AAPL")
            if alternative:
                # Try with alternative feed
                trades = alpaca.stock.trades.get_latest_trade("AAPL", feed=alternative)
                assert trades is not None

    def test_feed_validation_with_live_data(self, alpaca):
        """Test feed validation based on actual API access."""
        manager = FeedManager()

        # Test validation for bars endpoint
        assert manager.validate_feed("bars", "iex") is True
        assert manager.validate_feed("bars", "invalid_feed") is False

        # Test validation for non-feed endpoint
        assert manager.validate_feed("account", "iex") is False

    @pytest.mark.ci_skip  # Skip in CI due to heavy rate limiting
    def test_feed_manager_caching_behavior(self, alpaca):
        """Test that feed manager caches failed feeds appropriately."""
        manager = FeedManager(
            FeedConfig(
                preferred_feed=FeedType.SIP,
                fallback_feeds=[FeedType.IEX],
            )
        )

        # First request
        feed1 = manager.get_feed("bars", symbol="AAPL")

        # Simulate a failure if using SIP
        if feed1 == "sip":
            try:
                _ = alpaca.stock.history.get_stock_data(
                    symbol="AAPL",
                    start="2024-01-01",
                    end="2024-12-31",
                    timeframe="1d",
                    limit=1,
                    feed=feed1,
                )
            except APIRequestError as e:
                # Handle the error
                alternative = manager.handle_feed_error("bars", feed1, e, symbol="AAPL")

                # Second request should return alternative directly
                feed2 = manager.get_feed("bars", symbol="AAPL")
                assert feed2 in {alternative, "iex"}

    def test_feed_manager_reset_failures(self):
        """Test resetting feed failures."""
        manager = FeedManager()

        # Add some failures
        error = APIRequestError(403, "Access denied")
        manager.handle_feed_error("bars", "sip", error, symbol="AAPL")
        manager.handle_feed_error("quotes", "sip", error)

        assert len(manager._failed_feeds) > 0

        # Reset all failures
        manager.reset_failures()
        assert len(manager._failed_feeds) == 0

    def test_multiple_symbols_with_feed_manager(self, alpaca):
        """Test feed manager with multiple symbols."""
        manager = FeedManager()

        symbols = ["AAPL", "GOOGL", "MSFT"]
        successful_fetches = []

        for symbol in symbols:
            feed = manager.get_feed("latest/quotes", symbol=symbol)

            try:
                _ = alpaca.stock.latest_quote.get(symbol, feed=feed)
                successful_fetches.append((symbol, feed, True))
            except APIRequestError as e:
                # Try fallback
                alternative = manager.handle_feed_error(
                    "latest/quotes", feed, e, symbol=symbol
                )
                if alternative:
                    try:
                        _ = alpaca.stock.latest_quote.get(symbol, feed=alternative)
                        successful_fetches.append((symbol, alternative, True))
                    except APIRequestError:
                        successful_fetches.append((symbol, alternative, False))
                else:
                    successful_fetches.append((symbol, feed, False))

        # At least some symbols should succeed
        successful_count = sum(1 for _, _, success in successful_fetches if success)
        assert (
            successful_count > 0
        ), f"Failed to fetch any symbols: {successful_fetches}"

    def test_feed_config_endpoint_specific(self, alpaca):
        """Test endpoint-specific feed configuration."""
        config = FeedConfig(
            preferred_feed=FeedType.SIP,
            endpoint_feeds={
                "latest/quotes": FeedType.IEX,
                "bars": FeedType.SIP,
            },
        )
        manager = FeedManager(config)

        # Check that endpoint-specific config is used
        assert manager.get_feed("latest/quotes") == "iex"
        assert manager.get_feed("bars") == "sip"
        assert manager.get_feed("trades") == "sip"  # Uses default

    def test_subscription_level_affects_available_feeds(self):
        """Test that subscription level affects available feeds."""
        # Test with BASIC subscription
        config_basic = FeedConfig(subscription_level=SubscriptionLevel.BASIC)
        manager_basic = FeedManager(config_basic)

        available_basic = manager_basic.get_available_feeds()
        assert available_basic == [FeedType.IEX]

        # Test with UNLIMITED subscription
        config_unlimited = FeedConfig(subscription_level=SubscriptionLevel.UNLIMITED)
        manager_unlimited = FeedManager(config_unlimited)

        available_unlimited = manager_unlimited.get_available_feeds()
        assert set(available_unlimited) == {FeedType.SIP, FeedType.IEX, FeedType.OTC}
