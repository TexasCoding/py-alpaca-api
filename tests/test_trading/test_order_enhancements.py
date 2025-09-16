import json
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.models.order_model import OrderModel
from py_alpaca_api.trading.orders import Orders


class TestOrderEnhancements:
    @pytest.fixture
    def orders(self):
        base_url = "https://paper-api.alpaca.markets/v2"
        headers = {
            "APCA-API-KEY-ID": "test_key",
            "APCA-API-SECRET-KEY": "test_secret",
        }
        return Orders(base_url=base_url, headers=headers)

    @pytest.fixture
    def mock_order_response(self):
        return {
            "id": "order-123",
            "client_order_id": "client-123",
            "created_at": "2024-01-15T10:00:00Z",
            "updated_at": "2024-01-15T10:00:00Z",
            "submitted_at": "2024-01-15T10:00:00Z",
            "filled_at": None,
            "expired_at": None,
            "canceled_at": None,
            "failed_at": None,
            "replaced_at": None,
            "replaced_by": None,
            "replaces": None,
            "asset_id": "asset-123",
            "symbol": "AAPL",
            "asset_class": "us_equity",
            "notional": None,
            "qty": "10",
            "filled_qty": "0",
            "filled_avg_price": None,
            "order_class": "simple",
            "order_type": "market",
            "type": "market",
            "side": "buy",
            "time_in_force": "day",
            "limit_price": None,
            "stop_price": None,
            "status": "new",
            "extended_hours": False,
            "legs": None,
            "trail_percent": None,
            "trail_price": None,
            "hwm": None,
            "subtag": None,
            "source": None,
        }

    def test_replace_order(self, orders, mock_order_response):
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.replace_order(
                order_id="order-123",
                qty=20,
                limit_price=150.00,
                time_in_force="gtc",
                client_order_id="new-client-123",
            )

            assert isinstance(result, OrderModel)
            assert result.id == "order-123"
            assert result.symbol == "AAPL"

            # Verify the API call
            mock_requests.return_value.request.assert_called_once()
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["method"] == "PATCH"
            assert "order-123" in call_args.kwargs["url"]
            assert call_args.kwargs["json"]["qty"] == 20
            assert call_args.kwargs["json"]["limit_price"] == 150.00
            assert call_args.kwargs["json"]["time_in_force"] == "gtc"
            assert call_args.kwargs["json"]["client_order_id"] == "new-client-123"

    def test_replace_order_no_params(self, orders):
        with pytest.raises(ValidationError, match="At least one parameter"):
            orders.replace_order(order_id="order-123")

    def test_get_by_client_order_id(self, orders, mock_order_response):
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            # Return a list of orders for the filtering to work
            mock_response.text = json.dumps([mock_order_response])
            mock_requests.return_value.request.return_value = mock_response

            result = orders.get_by_client_order_id("client-123")

            assert isinstance(result, OrderModel)
            assert result.client_order_id == "client-123"

            # Verify the API call - it should query all orders
            mock_requests.return_value.request.assert_called_once_with(
                method="GET",
                url=f"{orders.base_url}/orders",
                headers=orders.headers,
                params={"status": "all", "limit": 500},
            )

    def test_cancel_by_client_order_id(self, orders, mock_order_response):
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            # First call: get_by_client_order_id to find the order
            get_response = MagicMock()
            get_response.text = json.dumps([mock_order_response])
            # Second call: cancel_by_id
            cancel_response = MagicMock()
            cancel_response.text = "{}"

            mock_requests.return_value.request.side_effect = [
                get_response,
                cancel_response,
            ]

            result = orders.cancel_by_client_order_id("client-123")

            assert "cancelled" in result

            # Verify the API calls
            assert mock_requests.return_value.request.call_count == 2
            # First call should be to get all orders
            first_call = mock_requests.return_value.request.call_args_list[0]
            assert first_call.kwargs["method"] == "GET"
            assert first_call.kwargs["url"] == f"{orders.base_url}/orders"
            # Second call should be to cancel by ID
            second_call = mock_requests.return_value.request.call_args_list[1]
            assert second_call.kwargs["method"] == "DELETE"
            assert "order-123" in second_call.kwargs["url"]

    def test_market_order_with_client_id(self, orders, mock_order_response):
        mock_order_response["client_order_id"] = "my-custom-id"

        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.market(
                symbol="AAPL",
                qty=10,
                side="buy",
                client_order_id="my-custom-id",
            )

            assert isinstance(result, OrderModel)
            assert result.client_order_id == "my-custom-id"

            # Verify the API call includes client_order_id
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["client_order_id"] == "my-custom-id"

    def test_market_order_with_order_class(self, orders, mock_order_response):
        mock_order_response["order_class"] = "oto"

        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.market(
                symbol="AAPL",
                qty=10,
                side="buy",
                order_class="oto",
            )

            assert isinstance(result, OrderModel)
            assert result.order_class == "oto"

            # Verify the API call includes order_class
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["order_class"] == "oto"

    def test_limit_order_with_enhancements(self, orders, mock_order_response):
        mock_order_response["order_class"] = "oco"
        mock_order_response["client_order_id"] = "limit-custom-id"
        mock_order_response["extended_hours"] = True

        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.limit(
                symbol="AAPL",
                limit_price=150.00,
                qty=10,
                side="buy",
                extended_hours=True,
                client_order_id="limit-custom-id",
                order_class="oco",
            )

            assert isinstance(result, OrderModel)
            assert result.order_class == "oco"
            assert result.client_order_id == "limit-custom-id"
            assert result.extended_hours is True

            # Verify the API call
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["order_class"] == "oco"
            assert call_args.kwargs["json"]["client_order_id"] == "limit-custom-id"
            assert call_args.kwargs["json"]["extended_hours"] is True

    def test_stop_order_with_enhancements(self, orders, mock_order_response):
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.stop(
                symbol="AAPL",
                stop_price=145.00,
                qty=10,
                side="sell",
                client_order_id="stop-custom-id",
                order_class="simple",
            )

            assert isinstance(result, OrderModel)

            # Verify the API call
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["client_order_id"] == "stop-custom-id"
            assert call_args.kwargs["json"]["order_class"] == "simple"

    def test_stop_limit_order_with_enhancements(self, orders, mock_order_response):
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.stop_limit(
                symbol="AAPL",
                stop_price=145.00,
                limit_price=144.50,
                qty=10,
                side="sell",
                client_order_id="stop-limit-custom-id",
                order_class="simple",
            )

            assert isinstance(result, OrderModel)

            # Verify the API call
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["client_order_id"] == "stop-limit-custom-id"
            assert call_args.kwargs["json"]["order_class"] == "simple"

    def test_trailing_stop_order_with_enhancements(self, orders, mock_order_response):
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            result = orders.trailing_stop(
                symbol="AAPL",
                qty=10,
                trail_percent=2.5,
                side="sell",
                client_order_id="trail-custom-id",
                order_class="simple",
            )

            assert isinstance(result, OrderModel)

            # Verify the API call
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["client_order_id"] == "trail-custom-id"
            assert call_args.kwargs["json"]["order_class"] == "simple"

    def test_order_class_priority(self, orders, mock_order_response):
        """Test that explicit order_class overrides bracket detection."""
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            # With both take_profit and stop_loss, but explicit order_class should be used
            orders.market(
                symbol="AAPL",
                qty=10,
                take_profit=160.00,
                stop_loss=140.00,  # Add stop_loss to avoid validation error
                order_class="oco",  # Explicitly set to oco
            )

            # Verify the API call uses oco, not bracket
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["order_class"] == "oco"

    def test_extended_hours_all_order_types(self, orders, mock_order_response):
        """Test that extended_hours parameter works for all order types."""
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            # Test market order
            orders.market(symbol="AAPL", qty=10, extended_hours=True)
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["extended_hours"] is True

            # Test limit order
            orders.limit(symbol="AAPL", limit_price=150.00, qty=10, extended_hours=True)
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["extended_hours"] is True

            # Test stop order
            orders.stop(symbol="AAPL", stop_price=145.00, qty=10, extended_hours=True)
            call_args = mock_requests.return_value.request.call_args
            assert call_args.kwargs["json"]["extended_hours"] is True

    def test_replace_order_partial_update(self, orders, mock_order_response):
        """Test that replace_order can update individual fields."""
        with patch("py_alpaca_api.trading.orders.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_order_response)
            mock_requests.return_value.request.return_value = mock_response

            # Only update quantity
            orders.replace_order(order_id="order-123", qty=50)

            call_args = mock_requests.return_value.request.call_args
            body = call_args.kwargs["json"]
            assert body["qty"] == 50
            assert "limit_price" not in body
            assert "stop_price" not in body
            assert "time_in_force" not in body

            # Only update time_in_force
            orders.replace_order(order_id="order-123", time_in_force="ioc")

            call_args = mock_requests.return_value.request.call_args
            body = call_args.kwargs["json"]
            assert body["time_in_force"] == "ioc"
            assert "qty" not in body
