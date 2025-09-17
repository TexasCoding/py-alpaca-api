"""Integration tests for Corporate Actions API with live data.

These tests require valid Alpaca API credentials and will make real API calls.
Run with: ./test.sh
"""

import os
from datetime import datetime, timedelta

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.models.corporate_action_model import (
    CorporateActionModel,
    DividendModel,
    MergerModel,
    SpinoffModel,
    SplitModel,
)

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


class TestCorporateActionsLive:
    """Integration tests for Corporate Actions API with live data."""

    def test_get_recent_dividends(self, alpaca):
        """Test retrieving recent dividend announcements."""
        # Use a recent 30-day window
        today = datetime.now()
        since = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            dividends = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend"],
            )

            # Check the response structure
            assert isinstance(dividends, list)

            # If we have dividends, verify their structure
            if dividends:
                dividend = dividends[0]
                assert isinstance(dividend, CorporateActionModel | DividendModel)
                assert hasattr(dividend, "id")
                assert hasattr(dividend, "corporate_action_id")
                assert hasattr(dividend, "ca_type")
                assert dividend.ca_type == "dividend"

                if isinstance(dividend, DividendModel):
                    # Check dividend-specific fields
                    assert hasattr(dividend, "cash_amount")
                    assert hasattr(dividend, "dividend_type")

                print(f"Found {len(dividends)} dividend announcements")
                for div in dividends[:5]:  # Print first 5
                    print(
                        f"  {div.initiating_symbol}: ${getattr(div, 'cash_amount', div.cash)} on {div.payable_date}"
                    )

        except APIRequestError as e:
            # If endpoint not available (404) or auth issues, skip
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available or auth issue: {e}")
            raise

    def test_get_recent_splits(self, alpaca):
        """Test retrieving recent stock split announcements."""
        # Use a 60-day window for better chance of finding splits
        today = datetime.now()
        since = (today - timedelta(days=60)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            splits = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["split"],
            )

            assert isinstance(splits, list)

            if splits:
                split = splits[0]
                assert isinstance(split, CorporateActionModel | SplitModel)
                assert split.ca_type == "split"

                if isinstance(split, SplitModel):
                    assert hasattr(split, "split_from")
                    assert hasattr(split, "split_to")

                print(f"Found {len(splits)} split announcements")
                for s in splits[:5]:
                    if hasattr(s, "split_from") and hasattr(s, "split_to"):
                        print(f"  {s.initiating_symbol}: {s.split_from}:{s.split_to}")

        except APIRequestError as e:
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available or auth issue: {e}")
            raise

    def test_get_specific_symbol_actions(self, alpaca):
        """Test retrieving corporate actions for specific symbols."""
        # Use popular stocks likely to have dividends
        test_symbols = ["AAPL", "MSFT", "JNJ", "KO"]

        today = datetime.now()
        since = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        for symbol in test_symbols:
            try:
                actions = alpaca.trading.corporate_actions.get_announcements(
                    since=since,
                    until=until,
                    ca_types=["dividend", "split"],
                    symbol=symbol,
                )

                assert isinstance(actions, list)

                if actions:
                    print(f"\n{symbol} corporate actions ({len(actions)} found):")
                    for action in actions:
                        # Check that action is related to the symbol
                        symbols = {action.initiating_symbol, action.target_symbol}
                        assert symbol in symbols
                        print(f"  Type: {action.ca_type}, Date: {action.ex_date}")
                    break  # Found data, test successful

            except APIRequestError as e:
                if e.status_code in [404, 401, 403]:
                    pytest.skip(f"API endpoint not available: {e}")
                # Continue to next symbol if current one fails
                continue

    def test_get_all_action_types(self, alpaca):
        """Test retrieving all types of corporate actions."""
        today = datetime.now()
        since = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            all_actions = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend", "split", "merger", "spinoff"],
            )

            assert isinstance(all_actions, list)

            # Count different types
            action_counts = {}
            for action in all_actions:
                ca_type = action.ca_type
                action_counts[ca_type] = action_counts.get(ca_type, 0) + 1

            print("\nCorporate actions summary (last 30 days):")
            print(f"  Total: {len(all_actions)}")
            for ca_type, count in action_counts.items():
                print(f"  {ca_type.capitalize()}: {count}")

        except APIRequestError as e:
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available: {e}")
            raise

    def test_date_filtering(self, alpaca):
        """Test different date filtering options."""
        # Test with ex_dividend date filtering
        today = datetime.now()
        since = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            # Filter by ex-dividend date
            ex_date_actions = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend"],
                date_type="ex_date",
            )

            # Filter by payable date
            payable_date_actions = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend"],
                date_type="payable_date",
            )

            assert isinstance(ex_date_actions, list)
            assert isinstance(payable_date_actions, list)

            print("\nDate filtering results:")
            print(f"  Ex-dividend date filter: {len(ex_date_actions)} results")
            print(f"  Payable date filter: {len(payable_date_actions)} results")

        except APIRequestError as e:
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available: {e}")
            raise

    def test_pagination_handling(self, alpaca):
        """Test that API returns all results within date range."""
        # Note: The API currently returns all results regardless of page_limit
        # This test documents the actual behavior

        # Use a shorter date range to limit results
        today = datetime.now()
        since = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            # Request with page_limit parameter (API ignores it but we include it)
            results_with_limit = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend"],
                page_limit=10,
            )

            # Request without page_limit
            results_without_limit = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend"],
            )

            assert isinstance(results_with_limit, list)
            assert isinstance(results_without_limit, list)

            # API returns all results regardless of page_limit
            assert len(results_with_limit) == len(results_without_limit)

            print("\nPagination behavior test:")
            print(f"  Results with page_limit=10: {len(results_with_limit)}")
            print(f"  Results without page_limit: {len(results_without_limit)}")
            print("  Note: API currently returns all results within date range")

        except APIRequestError as e:
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available: {e}")
            raise

    def test_get_announcement_by_id(self, alpaca):
        """Test retrieving a specific announcement by ID."""
        # First, get some announcements to have valid IDs
        today = datetime.now()
        since = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            announcements = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend", "split"],
                page_limit=5,
            )

            if not announcements:
                pytest.skip("No announcements found to test get_by_id")

            # Get the first announcement's ID
            announcement_id = announcements[0].id

            # Retrieve it by ID
            single_announcement = (
                alpaca.trading.corporate_actions.get_announcement_by_id(announcement_id)
            )

            assert isinstance(single_announcement, CorporateActionModel)
            assert single_announcement.id == announcement_id
            assert single_announcement.ca_type in [
                "dividend",
                "split",
                "merger",
                "spinoff",
            ]

            print("\nRetrieved announcement by ID:")
            print(f"  ID: {single_announcement.id}")
            print(f"  Type: {single_announcement.ca_type}")
            print(f"  Symbol: {single_announcement.initiating_symbol}")

        except APIRequestError as e:
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available: {e}")
            raise

    def test_error_handling(self, alpaca):
        """Test error handling for invalid requests."""
        # Test with invalid announcement ID
        with pytest.raises(APIRequestError) as exc_info:
            alpaca.trading.corporate_actions.get_announcement_by_id("invalid_id_12345")

        # Should get 404 for non-existent ID
        assert exc_info.value.status_code == 404

        # Test with date range exceeding 90 days
        with pytest.raises(ValidationError, match="Date range cannot exceed 90 days"):
            alpaca.trading.corporate_actions.get_announcements(
                since="2024-01-01",
                until="2024-06-01",
                ca_types=["dividend"],
            )

        # Test with invalid date format
        with pytest.raises(ValidationError, match="Invalid date format"):
            alpaca.trading.corporate_actions.get_announcements(
                since="01/01/2024",
                until="01/31/2024",
                ca_types=["dividend"],
            )

        # Test with invalid corporate action type
        with pytest.raises(ValidationError, match="Invalid corporate action type"):
            alpaca.trading.corporate_actions.get_announcements(
                since="2024-01-01",
                until="2024-01-31",
                ca_types=["invalid_type"],
            )

    def test_mergers_and_spinoffs(self, alpaca):
        """Test retrieving merger and spinoff announcements."""
        # Use wider date range as these are less common
        today = datetime.now()
        since = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            # Get mergers
            mergers = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["merger"],
            )

            # Get spinoffs
            spinoffs = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["spinoff"],
            )

            assert isinstance(mergers, list)
            assert isinstance(spinoffs, list)

            print("\nMergers and Spinoffs (last 90 days):")
            print(f"  Mergers: {len(mergers)}")
            print(f"  Spinoffs: {len(spinoffs)}")

            if mergers:
                merger = mergers[0]
                if isinstance(merger, MergerModel):
                    assert hasattr(merger, "acquirer_symbol")
                    print(
                        f"  Example merger: {merger.target_symbol} acquired by {merger.acquirer_symbol}"
                    )

            if spinoffs:
                spinoff = spinoffs[0]
                if isinstance(spinoff, SpinoffModel):
                    assert hasattr(spinoff, "new_symbol")
                    print(
                        f"  Example spinoff: {spinoff.initiating_symbol} spinning off {spinoff.new_symbol}"
                    )

        except APIRequestError as e:
            if e.status_code in [404, 401, 403]:
                pytest.skip(f"API endpoint not available: {e}")
            raise


if __name__ == "__main__":
    # Allow running this file directly for testing
    pytest.main([__file__, "-v"])
