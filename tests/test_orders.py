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
    return alpaca.order.market(symbol="AAPL", notional=2.25, side="buy")


def delete_all_orders(alpaca):
    alpaca.order.cancel_all()


################################################
# Test cases for PyAlpacaApi.cancel_all #
################################################
def test_cancel_all_orders(alpaca):
    delete_all_orders(alpaca)
    test_count = 5
    for i in range(test_count):
        alpaca.order.market(symbol="AAPL", notional=2.00)
    account = alpaca.order.cancel_all()
    assert f"{test_count} orders have been cancelled" in account


#################################################
# Test cases for PyAlpacaApi.get_by_id ####
# Test cases for PyAlpacaApi.cancel_by_id #
#################################################
def test_close_a_order_by_id(alpaca_create_order, alpaca):
    delete_all_orders(alpaca)
    order = alpaca_create_order
    assert order.status == "accepted"
    canceled_order = alpaca.order.cancel_by_id(order.id)
    f"Order {order.id} has been canceled" in canceled_order
    order = alpaca.order.get_by_id(order.id)
    assert order.status == "canceled"
    delete_all_orders(alpaca)


###########################################
# Test cases for PyAlpacaApi.market #
###########################################
def test_qty_market_order(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.market(symbol="AAPL", qty=0.01, side="buy")
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "market"
    assert order.qty == 0.01
    alpaca.order.cancel_all()


def test_notional_market_order(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.market(symbol="AAPL", notional=2.00, side="buy")
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "market"
    assert order.notional == 2.00
    alpaca.order.cancel_all()


def test_fake_value_market_order(alpaca):
    with pytest.raises(Exception):
        alpaca.order.market(symbol="FAKESYM", notional=2.00, side="buy")
    alpaca.order.cancel_all()


def test_no_money_value_market_order(alpaca):
    with pytest.raises(Exception):
        alpaca.order.market(symbol="AAPL", qty=2000.00, side="buy")
    alpaca.order.cancel_all()


def test_market_order_with_take_profit_but_qty_fractional(alpaca):
    with pytest.raises(ValueError):
        alpaca.order.market(symbol="AAPL", qty=0.12, side="buy", take_profit=250.00, stop_loss=150.00)
    alpaca.order.cancel_all()


def test_market_order_with_take_profit_but_notional(alpaca):
    with pytest.raises(ValueError):
        alpaca.order.market(symbol="AAPL", notional=230.23, side="buy", take_profit=250.00, stop_loss=150.00)
    alpaca.order.cancel_all()


def test_market_order_with_take_profit(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.market(symbol="AAPL", qty=1, side="buy", take_profit=250.00, stop_loss=150.00)
    assert isinstance(order, OrderClass)
    assert order.legs is not None
    assert order.legs[0].limit_price == 250.00
    assert order.legs[1].stop_price == 150.00


def test_order_instance(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.market(symbol="AAPL", qty=0.01, side="buy")
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
    alpaca.order.cancel_all()


###########################################
# Test cases for PyAlpacaApi.limit #
###########################################
def test_limit_order_with_qty(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.limit(symbol="AAPL", qty=0.1, side="buy", limit_price=200.00)
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "limit"
    assert order.qty == 0.1
    alpaca.order.cancel_all()


def test_limit_order_with_notional(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.limit(symbol="AAPL", notional=2.00, side="buy", limit_price=200.00)
    assert isinstance(order, OrderClass)
    assert order.status == "accepted"
    assert order.type == "limit"
    assert order.notional == 2.00
    alpaca.order.cancel_all()


def test_limit_order_with_fake_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.order.limit(symbol="FAKESYM", notional=2.00, side="buy", limit_price=200.00)
    alpaca.order.cancel_all()


def test_limit_order_with_no_money(alpaca):
    with pytest.raises(Exception):
        alpaca.order.limit(symbol="AAPL", qty=2000, side="buy", limit_price=200.00)
    alpaca.order.cancel_all()


###########################################
# Test cases for PyAlpacaApi.stop #
###########################################
def test_stop_order_with_qty(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.stop(symbol="AAPL", qty=1, side="buy", stop_price=200.00)
    assert isinstance(order, OrderClass)
    assert order.status == "pending_new" or order.status == "accepted"
    assert order.type == "stop"
    assert order.qty == 1
    alpaca.order.cancel_all()


def test_stop_order_with_fractional_shares(alpaca):
    with pytest.raises(Exception):
        alpaca.order.stop(symbol="AAPL", qty=1.34, side="buy", stop_price=200.00)
    alpaca.order.cancel_all()


def test_stop_order_with_fake_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.order.stop(symbol="FAKESYM", qty=1.0, side="buy", stop_price=200.00)
    alpaca.order.cancel_all()


def test_stop_order_with_no_money(alpaca):
    with pytest.raises(Exception):
        alpaca.order.stop(symbol="AAPL", qty=2000, side="buy", stop_price=200.00)
    alpaca.order.cancel_all()


###########################################
# Test cases for PyAlpacaApi.stop_limit   #
###########################################
def test_stop_limit_order_with_qty(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.stop_limit(symbol="AAPL", qty=1, side="buy", stop_price=200.00, limit_price=200.20)
    assert isinstance(order, OrderClass)
    assert order.status == "pending_new" or order.status == "accepted"
    assert order.type == "stop_limit"
    assert order.qty == 1
    alpaca.order.cancel_all()


def test_stop_limit_order_with_fake_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.order.stop_limit(
            symbol="FAKESYM",
            qty=2.00,
            side="buy",
            stop_price=200.00,
            limit_price=200.20,
        )
    alpaca.order.cancel_all()


def test_stop_limit_order_with_no_money(alpaca):
    with pytest.raises(Exception):
        alpaca.order.stop_limit(
            symbol="AAPL",
            qty=2000,
            side="buy",
            stop_price=200.00,
            limit_price=200.20,
        )
    alpaca.order.cancel_all()


###########################################
# Test cases for PyAlpacaApi.trailing_stop   #
###########################################
def test_trailing_stop_order_with_price(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.trailing_stop(symbol="AAPL", qty=1, side="buy", trail_price=10.00)
    assert isinstance(order, OrderClass)
    assert order.status == "pending_new" or order.status == "accepted" or order.status == "new"
    assert order.type == "trailing_stop"
    assert order.qty == 1
    alpaca.order.cancel_all()


def test_trailing_stop_order_with_percent(alpaca):
    delete_all_orders(alpaca)
    order = alpaca.order.trailing_stop(symbol="AAPL", qty=1, side="buy", trail_percent=2)
    assert isinstance(order, OrderClass)
    assert order.status == "pending_new" or order.status == "accepted" or order.status == "new"
    assert order.type == "trailing_stop"
    assert order.qty == 1
    alpaca.order.cancel_all()


def test_trailing_stop_order_with_both_percent_and_price(alpaca):
    with pytest.raises(Exception):
        alpaca.order.trailing_stop(
            symbol="AAPL",
            qty=2.00,
            side="buy",
            trail_price=10.00,
            trail_percent=2,
        )
    alpaca.order.cancel_all()


def test_trailing_stop_order_with_percent_less_than(alpaca):
    with pytest.raises(Exception):
        alpaca.order.trailing_stop(symbol="AAPL", qty=2.00, side="buy", trail_percent=-2)
    alpaca.order.cancel_all()


def test_trailing_stop_order_with_fake_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.order.trailing_stop(symbol="FAKESYM", notional=2.00, side="buy", trail_price=10.00)
    alpaca.order.cancel_all()


def test_trailing_stop_order_with_no_money(alpaca):
    with pytest.raises(Exception):
        alpaca.order.trailing_stop(symbol="AAPL", qty=2000, side="buy", trail_price=10.00)
    alpaca.order.cancel_all()
