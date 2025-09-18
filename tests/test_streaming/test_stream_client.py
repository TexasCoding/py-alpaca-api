"""Unit tests for StreamClient."""

import json
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api.exceptions import APIRequestError, AuthenticationError
from py_alpaca_api.streaming.stream_client import StreamClient, StreamType
from py_alpaca_api.streaming.stream_models import BarData, QuoteData, TradeData


class TestStreamClient:
    """Test StreamClient functionality."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return StreamClient(
            api_key="test_key",
            api_secret="test_secret",
            feed="iex",
            paper=True,
        )

    def test_init(self, client):
        """Test client initialization."""
        assert client.api_key == "test_key"
        assert client.api_secret == "test_secret"
        assert client.feed == "iex"
        assert client.paper is True
        assert not client.is_connected
        assert not client.is_authenticated
        assert client.url == "wss://stream.data.alpaca.markets/v2/iex"

    def test_production_url(self):
        """Test production URL."""
        client = StreamClient(
            api_key="test_key",
            api_secret="test_secret",
            feed="sip",
            paper=False,
        )
        assert client.url == "wss://stream.data.alpaca.markets/v2/sip"

    @patch("py_alpaca_api.streaming.stream_client.websocket.WebSocketApp")
    def test_connect(self, mock_ws_app, client):
        """Test connection establishment."""
        mock_ws = MagicMock()
        mock_ws_app.return_value = mock_ws

        # Mock authentication flow
        def simulate_auth(*args, **kwargs):
            client.is_connected = True
            client.is_authenticated = True

        with patch.object(client, "_run_forever", side_effect=simulate_auth):
            client.connect()

        assert client.is_authenticated
        mock_ws_app.assert_called_once()

    @patch("py_alpaca_api.streaming.stream_client.websocket.WebSocketApp")
    def test_connect_already_connected(self, mock_ws_app, client):
        """Test connecting when already connected."""
        client.is_connected = True
        client.connect()
        mock_ws_app.assert_not_called()

    def test_on_open(self, client):
        """Test on_open handler."""
        mock_ws = MagicMock()
        client._on_open(mock_ws)

        assert client.is_connected
        assert client.reconnect_attempts == 0

        # Check authentication message was sent
        mock_ws.send.assert_called_once()
        sent_data = json.loads(mock_ws.send.call_args[0][0])
        assert sent_data["action"] == "auth"
        assert sent_data["key"] == "test_key"
        assert sent_data["secret"] == "test_secret"

    def test_on_message_authentication(self, client):
        """Test authentication message handling."""
        mock_ws = MagicMock()
        message = json.dumps([{"T": "success", "msg": "authenticated"}])

        client._on_message(mock_ws, message)
        assert client.is_authenticated

    def test_on_message_error(self, client):
        """Test error message handling."""
        mock_ws = MagicMock()
        message = json.dumps([{"T": "error", "msg": "test error"}])

        client._on_message(mock_ws, message)
        # Should log error but not crash

    def test_on_message_quote(self, client):
        """Test quote message handling."""
        mock_ws = MagicMock()
        handler = MagicMock()
        client.handlers[StreamType.QUOTES].append(handler)

        message = json.dumps(
            [
                {
                    "T": "q",
                    "S": "AAPL",
                    "t": "2024-01-01T10:00:00",
                    "bp": 150.50,
                    "bs": 100,
                    "ap": 150.55,
                    "as": 200,
                    "bx": "Q",
                    "ax": "P",
                    "c": ["R"],
                }
            ]
        )

        client._on_message(mock_ws, message)
        handler.assert_called_once()
        quote = handler.call_args[0][0]
        assert isinstance(quote, QuoteData)
        assert quote.symbol == "AAPL"
        assert quote.bid_price == 150.50

    def test_on_message_trade(self, client):
        """Test trade message handling."""
        mock_ws = MagicMock()
        handler = MagicMock()
        client.handlers[StreamType.TRADES].append(handler)

        message = json.dumps(
            [
                {
                    "T": "t",
                    "S": "AAPL",
                    "t": "2024-01-01T10:00:00",
                    "p": 150.52,
                    "s": 100,
                    "x": "Q",
                    "i": 12345,
                    "c": ["@"],
                }
            ]
        )

        client._on_message(mock_ws, message)
        handler.assert_called_once()
        trade = handler.call_args[0][0]
        assert isinstance(trade, TradeData)
        assert trade.symbol == "AAPL"
        assert trade.price == 150.52

    def test_on_message_bar(self, client):
        """Test bar message handling."""
        mock_ws = MagicMock()
        handler = MagicMock()
        client.handlers[StreamType.BARS].append(handler)

        message = json.dumps(
            [
                {
                    "T": "b",
                    "S": "AAPL",
                    "t": "2024-01-01T10:00:00",
                    "o": 150.00,
                    "h": 151.00,
                    "l": 149.50,
                    "c": 150.75,
                    "v": 1000000,
                    "n": 5000,
                    "vw": 150.45,
                }
            ]
        )

        client._on_message(mock_ws, message)
        handler.assert_called_once()
        bar = handler.call_args[0][0]
        assert isinstance(bar, BarData)
        assert bar.symbol == "AAPL"
        assert bar.close == 150.75

    def test_on_close(self, client):
        """Test on_close handler."""
        mock_ws = MagicMock()
        client.is_connected = True
        client.is_authenticated = True
        client.should_reconnect = False

        client._on_close(mock_ws, 1000, "Normal closure")

        assert not client.is_connected
        assert not client.is_authenticated

    def test_subscribe_quotes(self, client):
        """Test quote subscription."""
        handler = MagicMock()
        client.is_connected = True
        client.ws = MagicMock()

        client.subscribe_quotes(["AAPL", "GOOGL"], handler)

        assert handler in client.handlers[StreamType.QUOTES]
        assert "AAPL" in client.subscriptions[StreamType.QUOTES]
        assert "GOOGL" in client.subscriptions[StreamType.QUOTES]

        # Check subscription message
        client.ws.send.assert_called_once()
        sent_data = json.loads(client.ws.send.call_args[0][0])
        assert sent_data["action"] == "subscribe"
        assert "AAPL" in sent_data["quotes"]
        assert "GOOGL" in sent_data["quotes"]

    def test_subscribe_quotes_single_symbol(self, client):
        """Test quote subscription with single symbol."""
        handler = MagicMock()
        client.is_connected = True
        client.ws = MagicMock()

        client.subscribe_quotes("AAPL", handler)

        assert "AAPL" in client.subscriptions[StreamType.QUOTES]

    def test_subscribe_trades(self, client):
        """Test trade subscription."""
        handler = MagicMock()
        client.is_connected = True
        client.ws = MagicMock()

        client.subscribe_trades(["AAPL"], handler)

        assert handler in client.handlers[StreamType.TRADES]
        assert "AAPL" in client.subscriptions[StreamType.TRADES]

    def test_subscribe_bars(self, client):
        """Test bar subscription."""
        handler = MagicMock()
        client.is_connected = True
        client.ws = MagicMock()

        client.subscribe_bars(["AAPL"], handler)

        assert handler in client.handlers[StreamType.BARS]
        assert "AAPL" in client.subscriptions[StreamType.BARS]

    def test_unsubscribe_quotes(self, client):
        """Test quote unsubscription."""
        client.is_connected = True
        client.ws = MagicMock()
        client.subscriptions[StreamType.QUOTES] = {"AAPL", "GOOGL"}

        client.unsubscribe_quotes("AAPL")

        assert "AAPL" not in client.subscriptions[StreamType.QUOTES]
        assert "GOOGL" in client.subscriptions[StreamType.QUOTES]

        # Check unsubscribe message
        client.ws.send.assert_called_once()
        sent_data = json.loads(client.ws.send.call_args[0][0])
        assert sent_data["action"] == "unsubscribe"
        assert "AAPL" in sent_data["quotes"]

    def test_unsubscribe_trades(self, client):
        """Test trade unsubscription."""
        client.is_connected = True
        client.ws = MagicMock()
        client.subscriptions[StreamType.TRADES] = {"AAPL"}

        client.unsubscribe_trades("AAPL")

        assert "AAPL" not in client.subscriptions[StreamType.TRADES]

    def test_unsubscribe_bars(self, client):
        """Test bar unsubscription."""
        client.is_connected = True
        client.ws = MagicMock()
        client.subscriptions[StreamType.BARS] = {"AAPL"}

        client.unsubscribe_bars("AAPL")

        assert "AAPL" not in client.subscriptions[StreamType.BARS]

    def test_subscribe_not_connected(self, client):
        """Test subscription when not connected."""
        handler = MagicMock()
        client.is_connected = False

        # Should add to subscriptions but not send message
        client.subscribe_quotes("AAPL", handler)
        assert "AAPL" in client.subscriptions[StreamType.QUOTES]

    def test_send_subscription_not_connected(self, client):
        """Test sending subscription when not connected."""
        with pytest.raises(APIRequestError) as exc_info:
            client._send_subscription(StreamType.QUOTES, ["AAPL"])

        assert "Not connected to stream" in str(exc_info.value)

    def test_disconnect(self, client):
        """Test disconnection."""
        mock_ws = MagicMock()
        mock_thread = MagicMock()
        mock_thread.is_alive.return_value = True

        client.ws = mock_ws
        client.ws_thread = mock_thread
        client.is_connected = True
        client.is_authenticated = True

        client.disconnect()

        assert not client.should_reconnect
        assert not client.is_connected
        assert not client.is_authenticated
        assert client.ws is None
        assert client.ws_thread is None
        mock_ws.close.assert_called_once()
        mock_thread.join.assert_called_once()

    def test_context_manager(self):
        """Test context manager usage."""
        with patch.object(StreamClient, "connect") as mock_connect:
            with patch.object(StreamClient, "disconnect") as mock_disconnect:
                with StreamClient("key", "secret") as client:
                    assert client is not None

                mock_connect.assert_called_once()
                mock_disconnect.assert_called_once()

    def test_reconnection_logic(self, client):
        """Test reconnection with exponential backoff."""
        client.reconnect_attempts = 0
        client.max_reconnect_attempts = 1

        with patch.object(client, "connect", side_effect=Exception("Failed")):
            with patch("time.sleep") as mock_sleep:
                client._handle_reconnect()

                # Should attempt reconnection
                assert client.reconnect_attempts == 1
                mock_sleep.assert_called_with(1)

    def test_max_reconnection_attempts(self, client):
        """Test max reconnection attempts."""
        client.reconnect_attempts = 10
        client.max_reconnect_attempts = 10

        client._handle_reconnect()

        assert not client.should_reconnect

    def test_resubscribe(self, client):
        """Test resubscription after reconnection."""
        client.is_connected = True
        client.ws = MagicMock()
        client.subscriptions[StreamType.QUOTES] = {"AAPL", "GOOGL"}
        client.subscriptions[StreamType.TRADES] = {"MSFT"}

        client._resubscribe()

        # Should send 2 subscription messages
        assert client.ws.send.call_count == 2

    def test_dispatch_with_handler_error(self, client):
        """Test dispatch with handler that raises exception."""
        handler1 = MagicMock()
        handler2 = MagicMock(side_effect=Exception("Handler error"))
        handler3 = MagicMock()

        client.handlers[StreamType.QUOTES] = [handler1, handler2, handler3]

        quote = QuoteData.from_dict({"T": "q", "S": "AAPL", "t": "2024-01-01T10:00:00"})

        # Should call all handlers despite error
        client._dispatch_message(StreamType.QUOTES, quote)

        handler1.assert_called_once()
        handler2.assert_called_once()
        handler3.assert_called_once()

    def test_authentication_timeout(self):
        """Test authentication timeout."""
        client = StreamClient("key", "secret")

        with patch.object(client, "_run_forever"):
            with patch("time.time", side_effect=[0, 0.1, 10.1]):
                with pytest.raises(AuthenticationError):
                    client.connect()

    def test_invalid_json_message(self, client):
        """Test handling of invalid JSON message."""
        mock_ws = MagicMock()
        client._on_message(mock_ws, "invalid json")
        # Should log error but not crash

    def test_symbol_case_conversion(self, client):
        """Test symbol case conversion."""
        handler = MagicMock()
        client.is_connected = True
        client.ws = MagicMock()

        client.subscribe_quotes(["aapl", "googl"], handler)

        assert "AAPL" in client.subscriptions[StreamType.QUOTES]
        assert "GOOGL" in client.subscriptions[StreamType.QUOTES]
        assert "aapl" not in client.subscriptions[StreamType.QUOTES]
