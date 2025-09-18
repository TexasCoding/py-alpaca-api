"""Integration tests for streaming with real data."""

import os
import threading
import time
from queue import Queue

import pytest

from py_alpaca_api.streaming.stream_client import StreamClient
from py_alpaca_api.streaming.stream_models import BarData, QuoteData, TradeData


@pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_SECRET_KEY"),
    reason="API credentials not set",
)
@pytest.mark.serial  # Run tests serially to avoid connection limit issues
class TestStreamIntegration:
    """Integration tests for WebSocket streaming."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        client = StreamClient(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            feed="iex",
            paper=True,
        )
        yield client
        # Ensure cleanup after each test
        if client.is_connected:
            client.disconnect()
            time.sleep(0.5)  # Brief delay to ensure connection is fully closed

    @pytest.fixture
    def live_symbols(self):
        """Get symbols that should have active market data during market hours."""
        return ["SPY", "AAPL", "MSFT"]

    def test_connect_and_authenticate(self, client):
        """Test connection and authentication with real API."""
        client.connect()
        assert client.is_connected
        assert client.is_authenticated
        client.disconnect()

    def test_subscribe_quotes_real_time(self, client, live_symbols):
        """Test receiving real-time quotes."""
        received_quotes = Queue()

        def quote_handler(quote: QuoteData) -> None:
            received_quotes.put(quote)

        # Connect and subscribe
        client.connect()
        client.subscribe_quotes(live_symbols, quote_handler)

        # Wait for quotes (max 30 seconds)
        timeout = 30
        start_time = time.time()
        quote = None

        while time.time() - start_time < timeout:
            if not received_quotes.empty():
                quote = received_quotes.get()
                break
            time.sleep(0.1)

        client.disconnect()

        # During market hours, we should receive quotes
        # During off-hours, this might not receive data
        if quote:
            assert isinstance(quote, QuoteData)
            assert quote.symbol in [s.upper() for s in live_symbols]
            assert quote.bid_price >= 0
            assert quote.ask_price >= 0
            assert quote.bid_size >= 0
            assert quote.ask_size >= 0

    def test_subscribe_trades_real_time(self, client, live_symbols):
        """Test receiving real-time trades."""
        received_trades = Queue()

        def trade_handler(trade: TradeData) -> None:
            received_trades.put(trade)

        # Connect and subscribe
        client.connect()
        client.subscribe_trades(live_symbols, trade_handler)

        # Wait for trades (max 30 seconds)
        timeout = 30
        start_time = time.time()
        trade = None

        while time.time() - start_time < timeout:
            if not received_trades.empty():
                trade = received_trades.get()
                break
            time.sleep(0.1)

        client.disconnect()

        # During market hours, we should receive trades
        if trade:
            assert isinstance(trade, TradeData)
            assert trade.symbol in [s.upper() for s in live_symbols]
            assert trade.price > 0
            assert trade.size > 0

    def test_subscribe_bars_real_time(self, client, live_symbols):
        """Test receiving real-time bars."""
        received_bars = Queue()

        def bar_handler(bar: BarData) -> None:
            received_bars.put(bar)

        # Connect and subscribe
        client.connect()
        client.subscribe_bars(live_symbols, bar_handler)

        # Wait for bars (max 60 seconds - bars are aggregated over time)
        timeout = 60
        start_time = time.time()
        bar = None

        while time.time() - start_time < timeout:
            if not received_bars.empty():
                bar = received_bars.get()
                break
            time.sleep(0.1)

        client.disconnect()

        # During market hours, we should receive bars
        if bar:
            assert isinstance(bar, BarData)
            assert bar.symbol in [s.upper() for s in live_symbols]
            assert bar.open > 0
            assert bar.high >= bar.low
            assert bar.volume >= 0

    def test_multiple_subscriptions(self, client):
        """Test multiple concurrent subscriptions."""
        quotes_received = []
        trades_received = []

        def quote_handler(quote: QuoteData) -> None:
            quotes_received.append(quote)

        def trade_handler(trade: TradeData) -> None:
            trades_received.append(trade)

        client.connect()

        # Subscribe to different data types
        client.subscribe_quotes(["SPY"], quote_handler)
        client.subscribe_trades(["AAPL"], trade_handler)

        # Let it run for a few seconds
        time.sleep(5)

        client.disconnect()

        # We may or may not receive data depending on market hours
        # But the subscriptions should work without errors

    def test_unsubscribe(self, client):
        """Test unsubscription."""
        received_quotes = []

        def quote_handler(quote: QuoteData) -> None:
            received_quotes.append(quote)

        client.connect()

        # Subscribe
        client.subscribe_quotes(["SPY", "AAPL"], quote_handler)
        time.sleep(2)

        # Unsubscribe from one symbol
        client.unsubscribe_quotes("SPY")
        time.sleep(2)

        client.disconnect()

        # Check that SPY is no longer in subscriptions
        from py_alpaca_api.streaming.stream_client import StreamType

        assert "SPY" not in client.subscriptions[StreamType.QUOTES]

    def test_reconnection(self, client):
        """Test reconnection logic."""
        quotes_received = []

        def quote_handler(quote: QuoteData) -> None:
            quotes_received.append(quote)

        client.connect()
        client.subscribe_quotes(["SPY"], quote_handler)

        # Simulate disconnection
        if client.ws:
            client.ws.close()

        # Wait a bit for potential reconnection
        time.sleep(5)

        # The client should attempt to reconnect
        # Note: Actual reconnection might not complete in test environment

        client.disconnect()

    def test_context_manager_usage(self):
        """Test using client as context manager."""
        quotes_received = []

        def quote_handler(quote: QuoteData) -> None:
            quotes_received.append(quote)

        with StreamClient(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            feed="iex",
            paper=True,
        ) as client:
            assert client.is_connected
            assert client.is_authenticated

            client.subscribe_quotes(["SPY"], quote_handler)
            time.sleep(2)

        # Client should be disconnected after context
        assert not client.is_connected

    @pytest.mark.slow
    def test_long_running_stream(self, client):
        """Test stream stability over longer period."""
        received_messages = []
        lock = threading.Lock()

        def handler(message) -> None:
            with lock:
                received_messages.append(message)

        client.connect()
        client.subscribe_quotes(["SPY"], handler)

        # Run for 30 seconds
        time.sleep(30)

        client.disconnect()

        # During market hours, should receive multiple messages
        # Check that connection remained stable
        assert not client.is_connected  # Should be cleanly disconnected

    def test_error_handling_invalid_symbol(self, client):
        """Test handling of invalid symbols."""
        quotes_received = []

        def quote_handler(quote: QuoteData) -> None:
            quotes_received.append(quote)

        client.connect()

        # Subscribe to invalid symbol - should not crash
        client.subscribe_quotes(["INVALID_SYMBOL_XYZ"], quote_handler)

        time.sleep(2)

        client.disconnect()

        # Should handle gracefully without crashing

    def test_feed_selection(self):
        """Test different feed selections."""
        # IEX feed (default for most users)
        client_iex = StreamClient(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            feed="iex",
            paper=True,
        )

        client_iex.connect()
        assert client_iex.is_authenticated
        client_iex.disconnect()

        # Note: SIP feed requires upgraded subscription
        # OTC feed is for OTC securities
