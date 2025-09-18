"""WebSocket streaming client for real-time market data."""

from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Callable
from enum import Enum
from typing import Any

import websocket

from py_alpaca_api.exceptions import APIRequestError, AuthenticationError
from py_alpaca_api.streaming.stream_models import BarData, QuoteData, TradeData

logger = logging.getLogger(__name__)


class StreamType(Enum):
    """Types of data streams."""

    QUOTES = "quotes"
    TRADES = "trades"
    BARS = "bars"


class StreamClient:
    """WebSocket client for real-time market data streaming."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        feed: str = "iex",
        paper: bool = True,
    ) -> None:
        """Initialize the streaming client.

        Args:
            api_key: Alpaca API key
            api_secret: Alpaca API secret
            feed: Data feed to use (iex, sip, otc)
            paper: Use paper trading endpoint
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.feed = feed
        self.paper = paper

        # WebSocket connection
        self.ws: websocket.WebSocketApp | None = None
        self.ws_thread: threading.Thread | None = None
        self.is_connected = False
        self.is_authenticated = False

        # Subscriptions and handlers
        self.subscriptions: dict[StreamType, set[str]] = {
            StreamType.QUOTES: set(),
            StreamType.TRADES: set(),
            StreamType.BARS: set(),
        }
        self.handlers: dict[StreamType, list[Callable]] = {
            StreamType.QUOTES: [],
            StreamType.TRADES: [],
            StreamType.BARS: [],
        }

        # Reconnection settings
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 1  # seconds
        self.max_reconnect_delay = 30  # seconds
        self.should_reconnect = True

        # WebSocket URL - Note: Data streams use the same URL regardless of paper/live
        # Only trading streams differ between paper and live
        base_url = "wss://stream.data.alpaca.markets/v2"
        self.url = f"{base_url}/{feed}"

    def connect(self) -> None:
        """Connect to the WebSocket stream."""
        if self.is_connected:
            logger.info("Already connected to stream")
            return

        logger.info(f"Connecting to WebSocket: {self.url}")

        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

        # Start WebSocket in a separate thread
        self.ws_thread = threading.Thread(target=self._run_forever, daemon=True)
        self.ws_thread.start()

        # Wait for connection and authentication
        timeout = 10
        start_time = time.time()
        while not self.is_authenticated and time.time() - start_time < timeout:
            time.sleep(0.1)

        if not self.is_authenticated:
            raise AuthenticationError("Failed to authenticate WebSocket connection")

        logger.info("Successfully connected and authenticated")

    def _run_forever(self) -> None:
        """Run the WebSocket connection forever."""
        try:
            if self.ws:
                self.ws.run_forever(ping_interval=30, ping_timeout=10)
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            if self.should_reconnect:
                self._handle_reconnect()

    def _on_open(self, ws: websocket.WebSocketApp) -> None:
        """Handle WebSocket connection open."""
        logger.info("WebSocket connection opened")
        self.is_connected = True
        self.reconnect_attempts = 0

        # Send authentication
        auth_msg = {
            "action": "auth",
            "key": self.api_key,
            "secret": self.api_secret,
        }
        ws.send(json.dumps(auth_msg))

    def _on_message(self, ws: websocket.WebSocketApp, message: str) -> None:
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)

            # Ensure data is a list
            if not isinstance(data, list):
                data = [data]

            # Handle different message types
            for msg in data:
                msg_type = msg.get("T")

                if msg_type == "success":
                    success_msg = msg.get("msg", "")
                    if success_msg == "authenticated":
                        self.is_authenticated = True
                        logger.info("Successfully authenticated")
                        # Resubscribe if we have active subscriptions
                        self._resubscribe()
                    else:
                        logger.info(f"Success message: {success_msg}")

                elif msg_type == "error":
                    error_code = msg.get("code", "")
                    error_msg = msg.get("msg", "")
                    logger.error(
                        f"Stream error - Code: {error_code}, Message: {error_msg}"
                    )
                    if error_code == 402 or "auth" in str(error_msg).lower():
                        logger.error("Authentication failed - check API credentials")
                        # Don't raise here, let timeout handle it

                elif msg_type == "subscription":
                    logger.info(f"Subscription update: {msg}")

                elif msg_type == "q":
                    # Quote message
                    quote = QuoteData.from_dict(msg)
                    self._dispatch_message(StreamType.QUOTES, quote)

                elif msg_type == "t":
                    # Trade message
                    trade = TradeData.from_dict(msg)
                    self._dispatch_message(StreamType.TRADES, trade)

                elif msg_type == "b":
                    # Bar message
                    bar = BarData.from_dict(msg)
                    self._dispatch_message(StreamType.BARS, bar)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse message: {e}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_error(self, ws: websocket.WebSocketApp, error: Exception) -> None:
        """Handle WebSocket errors."""
        logger.error(f"WebSocket error: {error}")

    def _on_close(
        self, ws: websocket.WebSocketApp, close_code: int, close_msg: str
    ) -> None:
        """Handle WebSocket connection close."""
        logger.info(f"WebSocket closed: {close_code} - {close_msg}")
        self.is_connected = False
        self.is_authenticated = False

        if self.should_reconnect:
            self._handle_reconnect()

    def _handle_reconnect(self) -> None:
        """Handle reconnection with exponential backoff."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error("Max reconnection attempts reached")
            self.should_reconnect = False
            return

        self.reconnect_attempts += 1
        delay = min(
            self.reconnect_delay * (2 ** (self.reconnect_attempts - 1)),
            self.max_reconnect_delay,
        )

        logger.info(
            f"Reconnecting in {delay} seconds (attempt {self.reconnect_attempts})"
        )
        time.sleep(delay)

        try:
            self.connect()
        except Exception as e:
            logger.error(f"Reconnection failed: {e}")
            self._handle_reconnect()

    def _resubscribe(self) -> None:
        """Resubscribe to all active subscriptions."""
        for stream_type, symbols in self.subscriptions.items():
            if symbols:
                self._send_subscription(stream_type, list(symbols), "subscribe")

    def _send_subscription(
        self,
        stream_type: StreamType,
        symbols: list[str],
        action: str = "subscribe",
    ) -> None:
        """Send subscription message to WebSocket."""
        if not self.is_connected or not self.ws:
            raise APIRequestError(message="Not connected to stream")

        # Map stream type to message key
        stream_map = {
            StreamType.QUOTES: "quotes",
            StreamType.TRADES: "trades",
            StreamType.BARS: "bars",
        }

        msg = {
            "action": action,
            stream_map[stream_type]: symbols,
        }

        self.ws.send(json.dumps(msg))
        logger.info(f"{action} to {stream_type.value}: {symbols}")

    def _dispatch_message(self, stream_type: StreamType, message: Any) -> None:
        """Dispatch message to registered handlers."""
        for handler in self.handlers[stream_type]:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"Handler error: {e}")

    def subscribe_quotes(
        self,
        symbols: str | list[str],
        handler: Callable[[QuoteData], None],
    ) -> None:
        """Subscribe to quote updates.

        Args:
            symbols: Symbol or list of symbols to subscribe to
            handler: Callback function to handle quote data
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        symbols = [s.upper() for s in symbols]

        # Add handler if not already registered
        if handler not in self.handlers[StreamType.QUOTES]:
            self.handlers[StreamType.QUOTES].append(handler)

        # Add symbols to subscriptions
        new_symbols = set(symbols) - self.subscriptions[StreamType.QUOTES]
        if new_symbols:
            self.subscriptions[StreamType.QUOTES].update(new_symbols)
            if self.is_connected:
                self._send_subscription(StreamType.QUOTES, list(new_symbols))

    def subscribe_trades(
        self,
        symbols: str | list[str],
        handler: Callable[[TradeData], None],
    ) -> None:
        """Subscribe to trade updates.

        Args:
            symbols: Symbol or list of symbols to subscribe to
            handler: Callback function to handle trade data
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        symbols = [s.upper() for s in symbols]

        # Add handler if not already registered
        if handler not in self.handlers[StreamType.TRADES]:
            self.handlers[StreamType.TRADES].append(handler)

        # Add symbols to subscriptions
        new_symbols = set(symbols) - self.subscriptions[StreamType.TRADES]
        if new_symbols:
            self.subscriptions[StreamType.TRADES].update(new_symbols)
            if self.is_connected:
                self._send_subscription(StreamType.TRADES, list(new_symbols))

    def subscribe_bars(
        self,
        symbols: str | list[str],
        handler: Callable[[BarData], None],
    ) -> None:
        """Subscribe to bar updates.

        Args:
            symbols: Symbol or list of symbols to subscribe to
            handler: Callback function to handle bar data
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        symbols = [s.upper() for s in symbols]

        # Add handler if not already registered
        if handler not in self.handlers[StreamType.BARS]:
            self.handlers[StreamType.BARS].append(handler)

        # Add symbols to subscriptions
        new_symbols = set(symbols) - self.subscriptions[StreamType.BARS]
        if new_symbols:
            self.subscriptions[StreamType.BARS].update(new_symbols)
            if self.is_connected:
                self._send_subscription(StreamType.BARS, list(new_symbols))

    def unsubscribe_quotes(self, symbols: str | list[str]) -> None:
        """Unsubscribe from quote updates.

        Args:
            symbols: Symbol or list of symbols to unsubscribe from
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        symbols = [s.upper() for s in symbols]
        symbols_to_remove = set(symbols) & self.subscriptions[StreamType.QUOTES]

        if symbols_to_remove:
            self.subscriptions[StreamType.QUOTES] -= symbols_to_remove
            if self.is_connected:
                self._send_subscription(
                    StreamType.QUOTES, list(symbols_to_remove), "unsubscribe"
                )

    def unsubscribe_trades(self, symbols: str | list[str]) -> None:
        """Unsubscribe from trade updates.

        Args:
            symbols: Symbol or list of symbols to unsubscribe from
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        symbols = [s.upper() for s in symbols]
        symbols_to_remove = set(symbols) & self.subscriptions[StreamType.TRADES]

        if symbols_to_remove:
            self.subscriptions[StreamType.TRADES] -= symbols_to_remove
            if self.is_connected:
                self._send_subscription(
                    StreamType.TRADES, list(symbols_to_remove), "unsubscribe"
                )

    def unsubscribe_bars(self, symbols: str | list[str]) -> None:
        """Unsubscribe from bar updates.

        Args:
            symbols: Symbol or list of symbols to unsubscribe from
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        symbols = [s.upper() for s in symbols]
        symbols_to_remove = set(symbols) & self.subscriptions[StreamType.BARS]

        if symbols_to_remove:
            self.subscriptions[StreamType.BARS] -= symbols_to_remove
            if self.is_connected:
                self._send_subscription(
                    StreamType.BARS, list(symbols_to_remove), "unsubscribe"
                )

    def disconnect(self) -> None:
        """Disconnect from the WebSocket stream."""
        logger.info("Disconnecting from stream")
        self.should_reconnect = False

        if self.ws:
            try:
                self.ws.close()
            except Exception as e:
                logger.debug(f"Error closing WebSocket: {e}")

        if self.ws_thread and self.ws_thread.is_alive():
            self.ws_thread.join(timeout=5)

        self.is_connected = False
        self.is_authenticated = False
        self.ws = None
        self.ws_thread = None
        logger.info("Disconnected from stream")

    def __enter__(self) -> StreamClient:
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.disconnect()
