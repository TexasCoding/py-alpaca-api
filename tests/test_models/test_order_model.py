import pytest
from py_alpaca_api.models.order_model import order_class_from_dict
import pendulum


class TestOrderClassFromDict:
    def test_order_class_from_dict_with_empty_dict(self):
        data_dict = {}
        with pytest.raises(KeyError):
            order_class_from_dict(data_dict)

    def test_order_class_from_dict_with_missing_required_keys(self):
        data_dict = {"some_key": "some_value"}
        with pytest.raises(KeyError):
            order_class_from_dict(data_dict)

    def test_order_class_from_dict_with_invalid_leg_data(self):
        data_dict = {
            "id": "order_123",
            "client_order_id": "client_order_123",
            "asset_class": "equity",
            "legs": [{"invalid_key": "invalid_value"}],
        }
        with pytest.raises(KeyError):
            order_class_from_dict(data_dict)

    def test_order_class_from_dict_with_valid_data(self):
        data_dict = {
            "id": "order_123",
            "client_order_id": "client_order_123",
            "created_at": "2023-05-01T12:00:00Z",
            "updated_at": "2023-05-01T12:00:01Z",
            "submitted_at": "2023-05-01T12:00:02Z",
            "filled_at": "2023-05-01T12:00:03Z",
            "expired_at": "2023-05-01T12:00:04Z",
            "canceled_at": "2023-05-01T12:00:05Z",
            "failed_at": "2023-05-01T12:00:06Z",
            "replaced_at": "2023-05-01T12:00:07Z",
            "replaced_by": "order_456",
            "replaces": "order_789",
            "asset_id": "asset_123",
            "symbol": "AAPL",
            "asset_class": "equity",
            "notional": 10000.0,
            "qty": 100.0,
            "filled_qty": 50.0,
            "filled_avg_price": 100.0,
            "order_class": "simple",
            "order_type": "market",
            "type": "market",
            "side": "buy",
            "time_in_force": "day",
            "limit_price": 110.0,
            "stop_price": 90.0,
            "status": "partially_filled",
            "extended_hours": False,
            "legs": [
                {
                    "id": "leg_1",
                    "client_order_id": "client_order_leg_1",
                    "created_at": "2023-05-01T12:00:00Z",
                    "updated_at": "2023-05-01T12:00:01Z",
                    "submitted_at": "2023-05-01T12:00:02Z",
                    "filled_at": "2023-05-01T12:00:03Z",
                    "expired_at": "2023-05-01T12:00:04Z",
                    "canceled_at": "2023-05-01T12:00:05Z",
                    "failed_at": "2023-05-01T12:00:06Z",
                    "replaced_at": "2023-05-01T12:00:07Z",
                    "replaced_by": "leg_2",
                    "replaces": "leg_3",
                    "asset_id": "asset_123",
                    "symbol": "AAPL",
                    "asset_class": "equity",
                    "notional": 5000.0,
                    "qty": 50.0,
                    "filled_qty": 25.0,
                    "filled_avg_price": 100.0,
                    "order_class": "simple",
                    "order_type": "market",
                    "type": "market",
                    "side": "buy",
                    "time_in_force": "day",
                    "limit_price": 110.0,
                    "stop_price": 90.0,
                    "status": "partially_filled",
                    "extended_hours": False,
                    "legs": [],
                    "trail_percent": 0.0,
                    "trail_price": 0.0,
                    "hwm": 0.0,
                    "subtag": "",
                    "source": "web",
                }
            ],
            "trail_percent": 0.0,
            "trail_price": 0.0,
            "hwm": 0.0,
            "subtag": "",
            "source": "web",
        }
        order = order_class_from_dict(data_dict)
        assert order.id == "order_123"
        assert order.client_order_id == "client_order_123"
        assert order.created_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 0, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.updated_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 1, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.submitted_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 2, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.filled_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 3, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.expired_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 4, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.canceled_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 5, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.failed_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 6, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.replaced_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 7, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.replaced_by == "order_456"
        assert order.replaces == "order_789"
        assert order.asset_id == "asset_123"
        assert order.symbol == "AAPL"
        assert order.asset_class == "equity"
        assert order.notional == 10000.0
        assert order.qty == 100.0
        assert order.filled_qty == 50.0
        assert order.filled_avg_price == 100.0
        assert order.order_class == "simple"
        assert order.order_type == "market"
        assert order.type == "market"
        assert order.side == "buy"
        assert order.time_in_force == "day"
        assert order.limit_price == 110.0
        assert order.stop_price == 90.0
        assert order.status == "partially_filled"
        assert order.extended_hours is False
        assert len(order.legs) == 1
        assert order.legs[0].id == "leg_1"
        assert order.legs[0].client_order_id == "client_order_leg_1"
        assert order.legs[0].created_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 0, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].updated_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 1, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].submitted_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 2, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].filled_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 3, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].expired_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 4, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].canceled_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 5, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].failed_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 6, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].replaced_at == pendulum.DateTime(
            2023, 5, 1, 12, 0, 7, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S")
        assert order.legs[0].replaced_by == "leg_2"
        assert order.legs[0].replaces == "leg_3"
        assert order.legs[0].asset_id == "asset_123"
        assert order.legs[0].symbol == "AAPL"
        assert order.legs[0].asset_class == "equity"
        assert order.legs[0].notional == 5000.0
        assert order.legs[0].qty == 50.0
        assert order.legs[0].filled_qty == 25.0
        assert order.legs[0].filled_avg_price == 100.0
        assert order.legs[0].order_class == "simple"
        assert order.legs[0].order_type == "market"
        assert order.legs[0].type == "market"
        assert order.legs[0].side == "buy"
        assert order.legs[0].time_in_force == "day"
        assert order.legs[0].limit_price == 110.0
        assert order.legs[0].stop_price == 90.0
        assert order.legs[0].status == "partially_filled"
        assert order.legs[0].extended_hours is False
        assert len(order.legs[0].legs) == 0
        assert order.legs[0].trail_percent == 0.0
        assert order.legs[0].trail_price == 0.0
        assert order.legs[0].hwm == 0.0
        assert order.legs[0].subtag == ""
        assert order.legs[0].source == "web"
        assert order.trail_percent == 0.0
        assert order.trail_price == 0.0
        assert order.hwm == 0.0
        assert order.subtag == ""
        assert order.source == "web"
