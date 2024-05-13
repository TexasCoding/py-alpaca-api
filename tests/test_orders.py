import os
from datetime import datetime, timedelta

import pytest
from pytz import timezone

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import OrderClass

# The following keys are for testing purposes only
# You should never hardcode your keys in your code
# Instead, you should use environment variables
# to store your keys and access them in your code
# Create a .env file in the root directory of the project for the following:
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")

tz = timezone("US/Eastern")
ctime = datetime.now(tz)
previous_day = (ctime - timedelta(days=1)).strftime("%Y-%m-%d")
month_ago = (ctime - timedelta(days=200)).strftime("%Y-%m-%d")


@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)


@pytest.fixture
def alpaca_create_order(alpaca):
    return alpaca.market_order(symbol="AAPL", notional=2.25, side="buy")


################################################
# Test cases for PyAlpacaApi.cancel_all_orders #
################################################
def test_cancel_all_orders(alpaca):
    test_count = 5
    for i in range(test_count):
        alpaca.market_order(symbol="AAPL", notional=2.00)
    account = alpaca.cancel_all_orders()
    assert f"{test_count} orders have been cancelled" in account


#################################################
# Test cases for PyAlpacaApi.get_order_by_id ####
# Test cases for PyAlpacaApi.cancel_order_by_id #
#################################################
def test_close_a_order_by_id(alpaca_create_order, alpaca):
    order = alpaca_create_order
    assert order.status == "accepted"
    canceled_order = alpaca.cancel_order_by_id(order.id)
    f"Order {order.id} has been canceled" in canceled_order
    order = alpaca.get_order_by_id(order.id)
    assert order.status == "canceled"


###########################################
# Test cases for PyAlpacaApi.market_order #
###########################################
def test_qty_market_order(alpaca):
    order = alpaca.market_order(symbol="AAPL", qty=0.01, side="buy")
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "market"
    assert order.qty == 0.01
    alpaca.cancel_all_orders()


def test_notional_market_order(alpaca):
    order = alpaca.market_order(symbol="AAPL", notional=2.00, side="buy")
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "market"
    assert order.notional == 2.00
    alpaca.cancel_all_orders()


def test_fake_value_market_order(alpaca):
    with pytest.raises(Exception):
        alpaca.market_order(symbol="FAKESYM", notional=2.00, side="buy")
    alpaca.cancel_all_orders()


def test_no_money_value_market_order(alpaca):
    with pytest.raises(Exception):
        alpaca.market_order(symbol="AAPL", qty=2000.00, side="buy")
    alpaca.cancel_all_orders()


def test_order_instance(alpaca):
    order = alpaca.market_order(symbol="AAPL", qty=0.01, side="buy")
    assert isinstance(order, OrderClass)
    assert isinstance(order.id, str)
    assert isinstance(order.client_order_id, str)
    assert isinstance(order.created_at, datetime)
    assert isinstance(order.updated_at, datetime)
    assert isinstance(order.submitted_at, datetime)
    assert isinstance(order.filled_at, datetime)
    assert isinstance(order.expired_at, datetime)
    assert isinstance(order.canceled_at, datetime)
    assert isinstance(order.failed_at, datetime)
    assert isinstance(order.replaced_at, datetime)
    assert isinstance(order.replaced_by, str)
    assert isinstance(order.replaces, str)
    assert isinstance(order.asset_id, str)
    assert isinstance(order.symbol, str)
    assert isinstance(order.asset_class, str)
    assert isinstance(order.qty, float)
    assert isinstance(order.filled_qty, float)
    assert isinstance(order.notional, float)
    assert isinstance(order.filled_avg_price, float)
    assert isinstance(order.order_class, str)
    assert isinstance(order.order_type, str)
    assert isinstance(order.type, str)
    assert isinstance(order.side, str)
    assert isinstance(order.time_in_force, str)
    assert isinstance(order.limit_price, float)
    assert isinstance(order.stop_price, float)
    assert isinstance(order.status, str)
    assert isinstance(order.extended_hours, bool)
    assert isinstance(order.legs, object)
    alpaca.cancel_all_orders()


###########################################
# Test cases for PyAlpacaApi.limit_order #
###########################################
def test_limit_order_with_qty(alpaca):
    order = alpaca.limit_order(symbol="AAPL", qty=0.1, side="buy", limit_price=200.00)
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "limit"
    assert order.qty == 0.1
    alpaca.cancel_all_orders()


def test_limit_order_with_notional(alpaca):
    order = alpaca.limit_order(symbol="AAPL", notional=2.00, side="buy", limit_price=200.00)
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "limit"
    assert order.notional == 2.00
    alpaca.cancel_all_orders()


def test_limit_order_with_fake_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.limit_order(symbol="FAKESYM", notional=2.00, side="buy", limit_price=200.00)
    alpaca.cancel_all_orders()


def test_limit_order_with_no_money(alpaca):
    with pytest.raises(Exception):
        alpaca.limit_order(symbol="AAPL", qty=2000, side="buy", limit_price=200.00)
    alpaca.cancel_all_orders()


###########################################
# Test cases for PyAlpacaApi.stop_order #
###########################################
def test_stop_order_with_qty(alpaca):
    order = alpaca.stop_order(symbol="AAPL", qty=1, side="buy", stop_price=200.00)
    assert isinstance(order, OrderClass)
    assert order.status == "pending_new" or order.status == "accepted"
    assert order.type == "stop"
    assert order.qty == 1
    alpaca.cancel_all_orders()


def test_stop_order_with_fake_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.stop_order(symbol="FAKESYM", notional=2.00, side="buy", stop_price=200.00)
    alpaca.cancel_all_orders()


def test_stop_order_with_no_money(alpaca):
    with pytest.raises(Exception):
        alpaca.stop_order(symbol="AAPL", qty=2000, side="buy", stop_price=200.00)
    alpaca.cancel_all_orders()
