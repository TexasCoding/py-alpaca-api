from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar

from py_alpaca_api.exceptions import APIRequestError, ValidationError

logger = logging.getLogger(__name__)


class FeedType(Enum):
    """Available data feed types."""

    SIP = "sip"
    IEX = "iex"
    OTC = "otc"

    @classmethod
    def from_string(cls, value: str) -> FeedType:
        """Create FeedType from string value."""
        try:
            return cls(value.lower())
        except ValueError as e:
            raise ValidationError(
                f"Invalid feed type: {value}. Must be one of {[f.value for f in cls]}"
            ) from e


class SubscriptionLevel(Enum):
    """User subscription levels."""

    BASIC = "basic"
    UNLIMITED = "unlimited"
    BUSINESS = "business"

    @classmethod
    def from_error(cls, error_message: str) -> SubscriptionLevel | None:
        """Detect subscription level from error message."""
        error_lower = error_message.lower()

        if "subscription" in error_lower:
            if "unlimited" in error_lower or "business" in error_lower:
                return cls.UNLIMITED
            return cls.BASIC
        return None


@dataclass
class FeedConfig:
    """Configuration for feed management."""

    preferred_feed: FeedType = FeedType.SIP
    fallback_feeds: list[FeedType] = field(default_factory=lambda: [FeedType.IEX])
    auto_fallback: bool = True
    subscription_level: SubscriptionLevel | None = None
    endpoint_feeds: dict[str, FeedType] = field(default_factory=dict)

    def get_feed_for_endpoint(self, endpoint: str) -> FeedType:
        """Get the configured feed for a specific endpoint."""
        return self.endpoint_feeds.get(endpoint, self.preferred_feed)


class FeedManager:
    """Manages data feed selection and fallback logic."""

    # Endpoints that support feed parameter
    FEED_SUPPORTED_ENDPOINTS: ClassVar[set[str]] = {
        "bars",
        "quotes",
        "trades",
        "snapshots",
        "latest/bars",
        "latest/quotes",
        "latest/trades",
    }

    # Feed availability by subscription level
    SUBSCRIPTION_FEEDS: ClassVar[dict[SubscriptionLevel, list[FeedType]]] = {
        SubscriptionLevel.BASIC: [FeedType.IEX],
        SubscriptionLevel.UNLIMITED: [FeedType.SIP, FeedType.IEX, FeedType.OTC],
        SubscriptionLevel.BUSINESS: [FeedType.SIP, FeedType.IEX, FeedType.OTC],
    }

    def __init__(self, config: FeedConfig | None = None):
        """Initialize the feed manager.

        Args:
            config: Feed configuration. If None, uses defaults.
        """
        self.config = config or FeedConfig()
        self._failed_feeds: dict[str, set[FeedType]] = {}
        self._detected_subscription_level: SubscriptionLevel | None = None

    def get_feed(self, endpoint: str, symbol: str | None = None) -> str | None:
        """Get the appropriate feed for an endpoint.

        Args:
            endpoint: The API endpoint being called
            symbol: Optional symbol for endpoint-specific logic

        Returns:
            Feed parameter value or None if endpoint doesn't support feeds
        """
        if not self._supports_feed(endpoint):
            return None

        feed = self.config.get_feed_for_endpoint(endpoint)

        # Check if this feed has previously failed
        endpoint_key = f"{endpoint}:{symbol}" if symbol else endpoint
        if (
            endpoint_key in self._failed_feeds
            and feed in self._failed_feeds[endpoint_key]
        ):
            # Try to use fallback
            for fallback in self.config.fallback_feeds:
                if fallback not in self._failed_feeds.get(endpoint_key, set()):
                    logger.info(f"Using fallback feed {fallback.value} for {endpoint}")
                    return fallback.value

        return feed.value

    def handle_feed_error(
        self,
        endpoint: str,
        feed: str,
        error: APIRequestError,
        symbol: str | None = None,
    ) -> str | None:
        """Handle feed-related errors and return alternative feed if available.

        Args:
            endpoint: The API endpoint that failed
            feed: The feed that caused the error
            error: The API error
            symbol: Optional symbol for endpoint-specific tracking

        Returns:
            Alternative feed to try, or None if no alternatives available
        """
        if not self.config.auto_fallback:
            return None

        # Try to detect subscription level from error
        error_msg = str(error)
        detected_level = SubscriptionLevel.from_error(error_msg)
        if detected_level and not self._detected_subscription_level:
            self._detected_subscription_level = detected_level
            logger.info(f"Detected subscription level: {detected_level.value}")

        # Track failed feed
        endpoint_key = f"{endpoint}:{symbol}" if symbol else endpoint
        if endpoint_key not in self._failed_feeds:
            self._failed_feeds[endpoint_key] = set()

        try:
            feed_type = FeedType.from_string(feed)
            self._failed_feeds[endpoint_key].add(feed_type)
            logger.warning(f"Feed {feed} failed for {endpoint_key}: {error_msg}")
        except ValidationError:
            logger.exception(f"Invalid feed type in error handling: {feed}")
            return None

        # Find alternative feed
        for fallback in self.config.fallback_feeds:
            if fallback not in self._failed_feeds[
                endpoint_key
            ] and self._is_feed_available(fallback):
                logger.info(f"Falling back to {fallback.value} feed for {endpoint_key}")
                return fallback.value

        logger.error(f"No alternative feeds available for {endpoint_key}")
        return None

    def detect_subscription_level(self, api_client: Any) -> SubscriptionLevel:
        """Detect user's subscription level by testing API access.

        Args:
            api_client: API client instance to test with

        Returns:
            Detected subscription level
        """
        # Try SIP feed first (requires Unlimited/Business)
        try:
            # Make a test request with SIP feed
            test_endpoint = "latest/quotes"
            test_params = {"symbols": "AAPL", "feed": FeedType.SIP.value}

            api_client._make_request(
                "GET", f"/stocks/{test_endpoint}", params=test_params
            )

            # If successful, user has at least Unlimited
            self._detected_subscription_level = SubscriptionLevel.UNLIMITED
            logger.info("Detected Unlimited/Business subscription level")

        except APIRequestError as e:
            # SIP failed, user likely has Basic subscription
            if "subscription" in str(e).lower() or "unauthorized" in str(e).lower():
                self._detected_subscription_level = SubscriptionLevel.BASIC
                logger.info("Detected Basic subscription level")
            else:
                # Unexpected error, default to Basic for safety
                self._detected_subscription_level = SubscriptionLevel.BASIC
                logger.warning(
                    f"Could not detect subscription level: {e}. Defaulting to Basic."
                )

        self.config.subscription_level = self._detected_subscription_level
        return self._detected_subscription_level

    def validate_feed(self, endpoint: str, feed: str) -> bool:
        """Validate if a feed is appropriate for an endpoint.

        Args:
            endpoint: The API endpoint
            feed: The feed to validate

        Returns:
            True if feed is valid for endpoint
        """
        if not self._supports_feed(endpoint):
            return False

        try:
            feed_type = FeedType.from_string(feed)
        except ValidationError:
            return False

        return self._is_feed_available(feed_type)

    def reset_failures(self, endpoint: str | None = None) -> None:
        """Reset tracked feed failures.

        Args:
            endpoint: Optional endpoint to reset. If None, resets all.
        """
        if endpoint:
            keys_to_remove = [
                k for k in self._failed_feeds if k.startswith(f"{endpoint}:")
            ]
            for key in keys_to_remove:
                del self._failed_feeds[key]
            if endpoint in self._failed_feeds:
                del self._failed_feeds[endpoint]
        else:
            self._failed_feeds.clear()

        logger.info(f"Reset feed failures for {endpoint or 'all endpoints'}")

    def _supports_feed(self, endpoint: str) -> bool:
        """Check if an endpoint supports feed parameter.

        Args:
            endpoint: The API endpoint

        Returns:
            True if endpoint supports feed parameter
        """
        # Check if any supported endpoint pattern matches
        return any(supported in endpoint for supported in self.FEED_SUPPORTED_ENDPOINTS)

    def _is_feed_available(self, feed: FeedType) -> bool:
        """Check if a feed is available based on subscription level.

        Args:
            feed: The feed to check

        Returns:
            True if feed is available
        """
        if not self._detected_subscription_level and not self.config.subscription_level:
            # If we don't know subscription level, assume all feeds available
            return True

        level = self._detected_subscription_level or self.config.subscription_level
        if level is None:
            return True
        available_feeds = self.SUBSCRIPTION_FEEDS.get(level, [])
        return feed in available_feeds

    def get_available_feeds(self) -> list[FeedType]:
        """Get list of available feeds based on subscription level.

        Returns:
            List of available feed types
        """
        if not self._detected_subscription_level and not self.config.subscription_level:
            # If unknown, return all feeds
            return list(FeedType)

        level = self._detected_subscription_level or self.config.subscription_level
        if level is None:
            return list(FeedType)
        return self.SUBSCRIPTION_FEEDS.get(level, [FeedType.IEX])
