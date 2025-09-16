from __future__ import annotations

from unittest.mock import Mock

import pytest

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.http.feed_manager import (
    FeedConfig,
    FeedManager,
    FeedType,
    SubscriptionLevel,
)


class TestFeedType:
    """Test FeedType enum functionality."""

    def test_feed_type_values(self):
        """Test feed type enum values."""
        assert FeedType.SIP.value == "sip"
        assert FeedType.IEX.value == "iex"
        assert FeedType.OTC.value == "otc"

    def test_from_string_valid(self):
        """Test creating FeedType from valid string."""
        assert FeedType.from_string("sip") == FeedType.SIP
        assert FeedType.from_string("SIP") == FeedType.SIP
        assert FeedType.from_string("iex") == FeedType.IEX
        assert FeedType.from_string("otc") == FeedType.OTC

    def test_from_string_invalid(self):
        """Test creating FeedType from invalid string."""
        with pytest.raises(ValidationError) as exc_info:
            FeedType.from_string("invalid")
        assert "Invalid feed type: invalid" in str(exc_info.value)


class TestSubscriptionLevel:
    """Test SubscriptionLevel enum functionality."""

    def test_subscription_level_values(self):
        """Test subscription level enum values."""
        assert SubscriptionLevel.BASIC.value == "basic"
        assert SubscriptionLevel.UNLIMITED.value == "unlimited"
        assert SubscriptionLevel.BUSINESS.value == "business"

    def test_from_error_basic(self):
        """Test detecting basic subscription from error."""
        error = "subscription does not permit SIP feed"
        assert SubscriptionLevel.from_error(error) == SubscriptionLevel.BASIC

    def test_from_error_unlimited(self):
        """Test detecting unlimited subscription from error."""
        error = "requires unlimited subscription"
        assert SubscriptionLevel.from_error(error) == SubscriptionLevel.UNLIMITED

    def test_from_error_business(self):
        """Test detecting business subscription from error."""
        error = "business subscription required"
        assert SubscriptionLevel.from_error(error) == SubscriptionLevel.UNLIMITED

    def test_from_error_no_match(self):
        """Test no subscription level detected from error."""
        error = "generic error message"
        assert SubscriptionLevel.from_error(error) is None


class TestFeedConfig:
    """Test FeedConfig dataclass."""

    def test_default_config(self):
        """Test default feed configuration."""
        config = FeedConfig()
        assert config.preferred_feed == FeedType.SIP
        assert config.fallback_feeds == [FeedType.IEX]
        assert config.auto_fallback is True
        assert config.subscription_level is None
        assert config.endpoint_feeds == {}

    def test_custom_config(self):
        """Test custom feed configuration."""
        config = FeedConfig(
            preferred_feed=FeedType.IEX,
            fallback_feeds=[FeedType.OTC, FeedType.SIP],
            auto_fallback=False,
            subscription_level=SubscriptionLevel.UNLIMITED,
        )
        assert config.preferred_feed == FeedType.IEX
        assert config.fallback_feeds == [FeedType.OTC, FeedType.SIP]
        assert config.auto_fallback is False
        assert config.subscription_level == SubscriptionLevel.UNLIMITED

    def test_get_feed_for_endpoint(self):
        """Test getting feed for specific endpoint."""
        config = FeedConfig(
            preferred_feed=FeedType.SIP,
            endpoint_feeds={"quotes": FeedType.IEX, "trades": FeedType.OTC},
        )
        assert config.get_feed_for_endpoint("quotes") == FeedType.IEX
        assert config.get_feed_for_endpoint("trades") == FeedType.OTC
        assert config.get_feed_for_endpoint("bars") == FeedType.SIP


class TestFeedManager:
    """Test FeedManager class."""

    def test_init_default(self):
        """Test default initialization."""
        manager = FeedManager()
        assert manager.config.preferred_feed == FeedType.SIP
        assert manager._failed_feeds == {}
        assert manager._detected_subscription_level is None

    def test_init_with_config(self):
        """Test initialization with custom config."""
        config = FeedConfig(preferred_feed=FeedType.IEX)
        manager = FeedManager(config)
        assert manager.config.preferred_feed == FeedType.IEX

    def test_get_feed_supported_endpoint(self):
        """Test getting feed for supported endpoint."""
        manager = FeedManager()

        # Test supported endpoints
        assert manager.get_feed("bars") == "sip"
        assert manager.get_feed("latest/quotes") == "sip"
        assert manager.get_feed("trades") == "sip"
        assert manager.get_feed("snapshots") == "sip"

    def test_get_feed_unsupported_endpoint(self):
        """Test getting feed for unsupported endpoint."""
        manager = FeedManager()

        # Unsupported endpoints should return None
        assert manager.get_feed("account") is None
        assert manager.get_feed("positions") is None
        assert manager.get_feed("orders") is None

    def test_get_feed_with_endpoint_config(self):
        """Test getting feed with endpoint-specific configuration."""
        config = FeedConfig(
            preferred_feed=FeedType.SIP,
            endpoint_feeds={"quotes": FeedType.IEX},
        )
        manager = FeedManager(config)

        assert manager.get_feed("quotes") == "iex"
        assert manager.get_feed("bars") == "sip"

    def test_get_feed_with_failed_feed(self):
        """Test getting feed when preferred feed has failed."""
        config = FeedConfig(
            preferred_feed=FeedType.SIP,
            fallback_feeds=[FeedType.IEX, FeedType.OTC],
        )
        manager = FeedManager(config)

        # Mark SIP as failed for bars endpoint
        manager._failed_feeds["bars"] = {FeedType.SIP}

        # Should fallback to IEX
        assert manager.get_feed("bars") == "iex"

        # Mark IEX as also failed
        manager._failed_feeds["bars"].add(FeedType.IEX)

        # Should fallback to OTC
        assert manager.get_feed("bars") == "otc"

    def test_handle_feed_error_no_auto_fallback(self):
        """Test handling feed error with auto_fallback disabled."""
        config = FeedConfig(auto_fallback=False)
        manager = FeedManager(config)

        error = APIRequestError(403, "Access denied")
        result = manager.handle_feed_error("bars", "sip", error)

        assert result is None
        assert "bars" not in manager._failed_feeds

    def test_handle_feed_error_with_fallback(self):
        """Test handling feed error with fallback."""
        config = FeedConfig(
            preferred_feed=FeedType.SIP,
            fallback_feeds=[FeedType.IEX, FeedType.OTC],
        )
        manager = FeedManager(config)

        error = APIRequestError(403, "subscription does not permit SIP")
        result = manager.handle_feed_error("bars", "sip", error)

        # Should return IEX as fallback
        assert result == "iex"
        assert FeedType.SIP in manager._failed_feeds["bars"]
        assert manager._detected_subscription_level == SubscriptionLevel.BASIC

    def test_handle_feed_error_with_symbol(self):
        """Test handling feed error with symbol tracking."""
        manager = FeedManager()

        error = APIRequestError(403, "Access denied")
        result = manager.handle_feed_error("bars", "sip", error, symbol="AAPL")

        # Should track failure with symbol
        assert result == "iex"
        assert FeedType.SIP in manager._failed_feeds["bars:AAPL"]

    def test_handle_feed_error_no_alternatives(self):
        """Test handling feed error with no alternatives."""
        config = FeedConfig(
            preferred_feed=FeedType.SIP,
            fallback_feeds=[FeedType.IEX],
        )
        manager = FeedManager(config)

        # Mark all feeds as failed
        manager._failed_feeds["bars"] = {FeedType.SIP, FeedType.IEX}

        error = APIRequestError(403, "Access denied")
        result = manager.handle_feed_error("bars", "sip", error)

        assert result is None

    def test_detect_subscription_level_unlimited(self):
        """Test detecting unlimited subscription level."""
        manager = FeedManager()

        # Mock successful API response
        mock_client = Mock()
        mock_client._make_request.return_value = Mock(status_code=200)

        level = manager.detect_subscription_level(mock_client)

        assert level == SubscriptionLevel.UNLIMITED
        assert manager._detected_subscription_level == SubscriptionLevel.UNLIMITED
        assert manager.config.subscription_level == SubscriptionLevel.UNLIMITED

    def test_detect_subscription_level_basic(self):
        """Test detecting basic subscription level."""
        manager = FeedManager()

        # Mock failed API response
        mock_client = Mock()
        mock_client._make_request.side_effect = APIRequestError(
            403, "subscription does not permit SIP"
        )

        level = manager.detect_subscription_level(mock_client)

        assert level == SubscriptionLevel.BASIC
        assert manager._detected_subscription_level == SubscriptionLevel.BASIC
        assert manager.config.subscription_level == SubscriptionLevel.BASIC

    def test_detect_subscription_level_unknown_error(self):
        """Test detecting subscription level with unknown error."""
        manager = FeedManager()

        # Mock unexpected error
        mock_client = Mock()
        mock_client._make_request.side_effect = APIRequestError(500, "Server error")

        level = manager.detect_subscription_level(mock_client)

        # Should default to BASIC for safety
        assert level == SubscriptionLevel.BASIC
        assert manager._detected_subscription_level == SubscriptionLevel.BASIC

    def test_validate_feed_supported_endpoint(self):
        """Test validating feed for supported endpoint."""
        manager = FeedManager()

        assert manager.validate_feed("bars", "sip") is True
        assert manager.validate_feed("bars", "iex") is True
        assert manager.validate_feed("bars", "invalid") is False

    def test_validate_feed_unsupported_endpoint(self):
        """Test validating feed for unsupported endpoint."""
        manager = FeedManager()

        assert manager.validate_feed("account", "sip") is False
        assert manager.validate_feed("positions", "iex") is False

    def test_validate_feed_with_subscription_level(self):
        """Test validating feed with subscription level."""
        config = FeedConfig(subscription_level=SubscriptionLevel.BASIC)
        manager = FeedManager(config)

        # Basic can only use IEX
        assert manager.validate_feed("bars", "iex") is True
        assert manager.validate_feed("bars", "sip") is False
        assert manager.validate_feed("bars", "otc") is False

    def test_reset_failures_all(self):
        """Test resetting all feed failures."""
        manager = FeedManager()

        # Add some failures
        manager._failed_feeds = {
            "bars": {FeedType.SIP},
            "bars:AAPL": {FeedType.IEX},
            "quotes": {FeedType.OTC},
        }

        manager.reset_failures()

        assert manager._failed_feeds == {}

    def test_reset_failures_specific_endpoint(self):
        """Test resetting failures for specific endpoint."""
        manager = FeedManager()

        # Add some failures
        manager._failed_feeds = {
            "bars": {FeedType.SIP},
            "bars:AAPL": {FeedType.IEX},
            "bars:MSFT": {FeedType.SIP},
            "quotes": {FeedType.OTC},
        }

        manager.reset_failures("bars")

        # Only bars-related failures should be reset
        assert "bars" not in manager._failed_feeds
        assert "bars:AAPL" not in manager._failed_feeds
        assert "bars:MSFT" not in manager._failed_feeds
        assert "quotes" in manager._failed_feeds

    def test_get_available_feeds_unknown_subscription(self):
        """Test getting available feeds with unknown subscription."""
        manager = FeedManager()

        feeds = manager.get_available_feeds()

        # Should return all feeds when subscription unknown
        assert set(feeds) == {FeedType.SIP, FeedType.IEX, FeedType.OTC}

    def test_get_available_feeds_basic_subscription(self):
        """Test getting available feeds with basic subscription."""
        config = FeedConfig(subscription_level=SubscriptionLevel.BASIC)
        manager = FeedManager(config)

        feeds = manager.get_available_feeds()

        assert feeds == [FeedType.IEX]

    def test_get_available_feeds_unlimited_subscription(self):
        """Test getting available feeds with unlimited subscription."""
        config = FeedConfig(subscription_level=SubscriptionLevel.UNLIMITED)
        manager = FeedManager(config)

        feeds = manager.get_available_feeds()

        assert set(feeds) == {FeedType.SIP, FeedType.IEX, FeedType.OTC}

    def test_get_available_feeds_detected_subscription(self):
        """Test getting available feeds with detected subscription."""
        manager = FeedManager()
        manager._detected_subscription_level = SubscriptionLevel.BASIC

        feeds = manager.get_available_feeds()

        assert feeds == [FeedType.IEX]

    def test_is_feed_available_unknown_subscription(self):
        """Test checking feed availability with unknown subscription."""
        manager = FeedManager()

        # All feeds should be available when subscription unknown
        assert manager._is_feed_available(FeedType.SIP) is True
        assert manager._is_feed_available(FeedType.IEX) is True
        assert manager._is_feed_available(FeedType.OTC) is True

    def test_is_feed_available_basic_subscription(self):
        """Test checking feed availability with basic subscription."""
        config = FeedConfig(subscription_level=SubscriptionLevel.BASIC)
        manager = FeedManager(config)

        assert manager._is_feed_available(FeedType.IEX) is True
        assert manager._is_feed_available(FeedType.SIP) is False
        assert manager._is_feed_available(FeedType.OTC) is False

    def test_supports_feed_endpoint(self):
        """Test checking if endpoint supports feed parameter."""
        manager = FeedManager()

        # Supported endpoints
        assert manager._supports_feed("bars") is True
        assert manager._supports_feed("/v2/stocks/bars") is True
        assert manager._supports_feed("latest/quotes") is True
        assert manager._supports_feed("trades") is True
        assert manager._supports_feed("snapshots") is True

        # Unsupported endpoints
        assert manager._supports_feed("account") is False
        assert manager._supports_feed("positions") is False
        assert manager._supports_feed("orders") is False
