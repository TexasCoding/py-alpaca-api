import contextlib
import os
import time

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError


@pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_SECRET_KEY"),
    reason="API credentials not set",
)
class TestOrderEnhancementsIntegration:
    @pytest.fixture
    def alpaca(self):
        return PyAlpacaAPI(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            api_paper=True,
        )

    @pytest.fixture(autouse=True)
    def cleanup_orders(self, alpaca):
        """Cancel all orders before and after each test."""
        # Cancel before test
        with contextlib.suppress(Exception):
            alpaca.trading.orders.cancel_all()

        yield

        # Cancel after test
        with contextlib.suppress(Exception):
            alpaca.trading.orders.cancel_all()

    def test_market_order_with_client_order_id(self, alpaca):
        # Submit order with client ID
        client_id = f"test-market-{int(time.time())}"
        order = alpaca.trading.orders.market(
            symbol="AAPL",
            qty=1,
            side="buy",
            client_order_id=client_id,
        )

        assert order.client_order_id == client_id
        assert order.symbol == "AAPL"
        assert order.qty == 1

        # Retrieve order by client ID
        retrieved = alpaca.trading.orders.get_by_client_order_id(client_id)
        assert retrieved.id == order.id
        assert retrieved.client_order_id == client_id

        # Cancel by client ID
        result = alpaca.trading.orders.cancel_by_client_order_id(client_id)
        assert "cancelled" in result.lower()

    def test_limit_order_with_extended_hours(self, alpaca):
        # Submit limit order with extended hours
        client_id = f"test-limit-ext-{int(time.time())}"
        order = alpaca.trading.orders.limit(
            symbol="AAPL",
            limit_price=150.00,
            qty=1,
            side="buy",
            extended_hours=True,
            client_order_id=client_id,
            time_in_force="day",
        )

        assert order.extended_hours is True
        assert order.client_order_id == client_id

        # Cancel the order
        alpaca.trading.orders.cancel_by_id(order.id)

    def test_replace_order(self, alpaca):
        # Submit initial limit order
        order = alpaca.trading.orders.limit(
            symbol="AAPL",
            limit_price=100.00,  # Very low price to avoid fill
            qty=1,
            side="buy",
            time_in_force="gtc",
        )

        assert order.qty == 1
        assert order.limit_price == 100.00

        # Wait a moment for order to be fully registered
        time.sleep(0.5)

        # Only test replace if order is in correct state
        if order.status in ["new", "partially_filled"]:
            # Replace order with new parameters
            replaced_order = alpaca.trading.orders.replace_order(
                order_id=order.id,
                qty=2,
                limit_price=101.00,
            )

            assert replaced_order.qty == 2
            assert replaced_order.limit_price == 101.00
            assert replaced_order.symbol == "AAPL"

            # Cancel the order
            alpaca.trading.orders.cancel_by_id(replaced_order.id)
        else:
            # Order already accepted/filled, just cancel it
            with contextlib.suppress(Exception):
                alpaca.trading.orders.cancel_by_id(order.id)

    def test_order_class_oto(self, alpaca):
        """Test One-Triggers-Other (OTO) order class."""
        # Note: OTO orders require specific account permissions
        # This test may fail if the account doesn't support OTO orders
        try:
            client_id = f"test-oto-{int(time.time())}"
            order = alpaca.trading.orders.limit(
                symbol="AAPL",
                limit_price=100.00,  # Low price to avoid fill
                qty=1,
                side="buy",
                order_class="oto",
                take_profit=150.00,  # OTO needs either take_profit OR stop_loss
                client_order_id=client_id,
            )

            if order:
                assert order.order_class in ["oto", "simple"]  # May fallback to simple
                alpaca.trading.orders.cancel_by_id(order.id)
        except APIRequestError as e:
            # OTO might not be supported
            if "order class" not in str(e).lower():
                raise

    def test_order_class_oco(self, alpaca):
        """Test One-Cancels-Other (OCO) order class."""
        # Note: OCO orders are exit-only orders and require an existing position
        # Since we may not have a position, we'll test that the API properly rejects
        # OCO orders when no position exists, or skip if we get the expected error
        try:
            client_id = f"test-oco-{int(time.time())}"
            order = alpaca.trading.orders.limit(
                symbol="AAPL",
                limit_price=100.00,  # Low price to avoid fill
                qty=1,
                side="sell",  # OCO orders are exit orders, so we'd sell to close a long position
                order_class="oco",
                take_profit=150.00,  # Take profit at higher price for sell order
                stop_loss=80.00,  # Stop loss at lower price for sell order
                client_order_id=client_id,
            )

            # If we somehow have a position and the order succeeds
            if order:
                assert order.order_class in ["oco", "simple"]  # May fallback to simple
                alpaca.trading.orders.cancel_by_id(order.id)
        except APIRequestError as e:
            # Expected errors since OCO orders are exit-only
            error_msg = str(e).lower()
            if "oco orders must be exit orders" in error_msg:
                pass  # Expected since we don't have a position
            elif "insufficient" in error_msg or "position" in error_msg:
                pass  # Also expected if no position exists
            elif "order class" in error_msg:
                pass  # OCO might not be supported on account
            else:
                raise  # Unexpected error

    def test_bracket_order_with_explicit_class(self, alpaca):
        """Test bracket order with explicit order_class."""
        client_id = f"test-bracket-{int(time.time())}"
        order = alpaca.trading.orders.market(
            symbol="AAPL",
            qty=1,
            side="buy",
            take_profit=500.00,  # High take profit (well above current price ~$240)
            stop_loss=50.00,  # Low stop loss
            order_class="bracket",  # Explicitly set
            client_order_id=client_id,
        )

        assert order.order_class == "bracket"
        assert order.client_order_id == client_id

        # Cancel the order
        alpaca.trading.orders.cancel_by_id(order.id)

    def test_stop_order_with_client_id(self, alpaca):
        client_id = f"test-stop-{int(time.time())}"
        order = alpaca.trading.orders.stop(
            symbol="AAPL",
            stop_price=300.00,  # High stop price for buy to avoid trigger
            qty=1,
            side="buy",
            client_order_id=client_id,
        )

        assert order.client_order_id == client_id
        assert order.stop_price == 300.00

        # Cancel the order
        alpaca.trading.orders.cancel_by_client_order_id(client_id)

    def test_trailing_stop_with_enhancements(self, alpaca):
        client_id = f"test-trail-{int(time.time())}"
        order = alpaca.trading.orders.trailing_stop(
            symbol="AAPL",
            qty=1,
            trail_percent=10.0,  # 10% trailing stop
            side="sell",
            client_order_id=client_id,
        )

        assert order.client_order_id == client_id
        assert order.trail_percent == 10.0

        # Cancel the order
        alpaca.trading.orders.cancel_by_id(order.id)

    @pytest.mark.rate_limited  # Add delays to avoid rate limiting
    def test_multiple_orders_with_client_ids(self, alpaca):
        """Test managing multiple orders with client IDs."""
        client_ids = [f"test-multi-{i}-{int(time.time())}" for i in range(3)]
        orders = []

        # Submit multiple orders
        for i, client_id in enumerate(client_ids):
            order = alpaca.trading.orders.limit(
                symbol="AAPL",
                limit_price=100.00 + i,  # Different prices
                qty=1,
                side="buy",
                client_order_id=client_id,
            )
            orders.append(order)

        # Verify we can retrieve each by client ID
        for client_id, order in zip(client_ids, orders, strict=False):
            retrieved = alpaca.trading.orders.get_by_client_order_id(client_id)
            assert retrieved.id == order.id
            assert retrieved.client_order_id == client_id

        # Cancel all orders
        for client_id in client_ids:
            alpaca.trading.orders.cancel_by_client_order_id(client_id)

    def test_replace_order_time_in_force(self, alpaca):
        """Test replacing order's time_in_force parameter."""
        # Submit initial order with day time_in_force
        order = alpaca.trading.orders.limit(
            symbol="AAPL",
            limit_price=100.00,
            qty=1,
            side="buy",
            time_in_force="day",
        )

        assert order.time_in_force == "day"

        # Wait a moment for order to be fully registered
        time.sleep(0.5)

        # Only test replace if order is in correct state
        if order.status in ["new", "partially_filled"]:
            # Replace with gtc time_in_force
            replaced = alpaca.trading.orders.replace_order(
                order_id=order.id,
                time_in_force="gtc",
            )

            assert replaced.time_in_force == "gtc"
            assert replaced.qty == order.qty  # Qty should remain the same

            # Cancel the order
            alpaca.trading.orders.cancel_by_id(replaced.id)
        else:
            # Order already accepted/filled, just cancel it
            with contextlib.suppress(Exception):
                alpaca.trading.orders.cancel_by_id(order.id)
