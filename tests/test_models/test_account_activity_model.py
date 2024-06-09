import pytest
import pendulum
from py_alpaca_api.models.account_activity_model import (
    AccountActivityModel,
    account_activity_class_from_dict,
)


def test_account_activity_class_from_dict_valid_data():
    data_dict = {
        "activity_type": "FILL",
        "id": "12345678",
        "transaction_time": "2023-04-01T12:00:00Z",
        "price": 100.0,
        "qty": 10,
        "side": "buy",
        "leaves_qty": 0,
        "symbol": "AAPL",
        "order_id": "abcdef",
        "type": "market",
        "cum_qty": 10,
        "order_status": "filled",
        "date": "2023-04-01T12:00:00Z",
        "net_amount": 1000.0,
        "per_share_amount": 100.0,
    }
    expected_activity = AccountActivityModel(
        activity_type="FILL",
        id="12345678",
        transaction_time=pendulum.parse("2023-04-01T12:00:00Z").strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        price=100.0,
        qty=10,
        side="buy",
        leaves_qty=0,
        symbol="AAPL",
        order_id="abcdef",
        type="market",
        cum_qty=10,
        order_status="filled",
        date=pendulum.parse("2023-04-01T12:00:00Z").strftime("%Y-%m-%d %H:%M:%S"),
        net_amount=1000.0,
        per_share_amount=100.0,
    )
    assert account_activity_class_from_dict(data_dict) == expected_activity


def test_account_activity_class_from_dict_invalid_data_types():
    data_dict = {
        "activity_type": "FILL",
        "id": 12345678,
        "transaction_time": bool,
        "price": "100.0",
        "qty": 10,
        "side": "buy",
        "leaves_qty": 0,
        "symbol": "AAPL",
        "order_id": "abcdef",
        "misc_fees": 1.0,
        "order_type": "market",
        "cumulative_qty": 10,
        "status": False,
    }
    with pytest.raises(TypeError):
        account_activity_class_from_dict(data_dict)
