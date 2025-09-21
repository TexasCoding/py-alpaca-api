import datetime
import os

import pytest
from pytz import timezone

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.models.order_model import OrderModel

# The following keys are for testing purposes only
# You should never hardcode your keys in your code
# Instead, you should use environment variables
# to store your keys and access them in your code
# Create a .env file in the root directory of the project for the following:
api_key = os.environ.get("ALPACA_API_KEY")
api_secret = os.environ.get("ALPACA_SECRET_KEY")

tz = timezone("US/Eastern")
ctime = datetime.datetime.now(tz)
previous_day = (ctime - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
month_ago = (ctime - datetime.timedelta(days=200)).strftime("%Y-%m-%d")


@pytest.fixture
def alpaca():
    return PyAlpacaAPI(api_key=api_key, api_secret=api_secret, api_paper=True)


@pytest.fixture
def alpaca_create_order(alpaca):
    return alpaca.trading.orders.market(symbol="AAPL", notional=2.25, side="buy")


################################################
# Test cases for PyAlpacaAPI.cancel_all #
################################################
@pytest.mark.rate_limited
def test_cancel_all_orders(alpaca):
    alpaca.trading.orders.cancel_all()
    test_count = 5
    for _i in range(test_count):
        alpaca.trading.orders.market(symbol="AAPL", notional=2.00)
    account = alpaca.trading.orders.cancel_all()
    assert "5 orders have been cancelled" in account


#################################################
# Test cases for PyAlpacaAPI.get_by_id ####
# Test cases for PyAlpacaAPI.cancel_by_id #
#################################################
def test_close_a_order_by_id(alpaca_create_order, alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca_create_order
    assert order.status == "accepted"
    try:
        canceled_order = alpaca.trading.orders.cancel_by_id(order.id)
        assert f"Order {order.id} has been cancelled" in canceled_order
        order = alpaca.trading.orders.get_by_id(order.id)
        assert order.status == "canceled"
    except Exception as e:
        assert 'order is already in "filled" state' in str(
            e
        ) or 'order is already in \\"filled\\" state' in str(e)
    alpaca.trading.orders.cancel_all()


###########################################
# Test cases for PyAlpacaAPI.market #
###########################################
def test_qty_market_order(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.market(symbol="AAPL", qty=0.01, side="buy")
    assert isinstance(order, OrderModel)
    assert order.status == "accepted"
    assert order.type == "market"
    assert order.qty == 0.01
    alpaca.trading.orders.cancel_all()


def test_notional_market_order(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.market(symbol="AAPL", notional=2.00, side="buy")
    assert isinstance(order, OrderModel)
    assert order.status == "accepted"
    assert order.type == "market"
    assert order.notional == 2.00
    alpaca.trading.orders.cancel_all()


def test_fake_value_market_order(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.market(symbol="FAKESYM", notional=2.00, side="buy")
    alpaca.trading.orders.cancel_all()


def test_no_money_value_market_order(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.market(symbol="AAPL", qty=2000.00, side="buy")
    alpaca.trading.orders.cancel_all()


def test_market_order_with_take_profit_but_qty_fractional(alpaca):
    with pytest.raises(ValidationError):
        alpaca.trading.orders.market(
            symbol="AAPL", qty=0.12, side="buy", take_profit=250.00, stop_loss=150.00
        )
    alpaca.trading.orders.cancel_all()


def test_market_order_with_take_profit_but_notional(alpaca):
    with pytest.raises(ValidationError):
        alpaca.trading.orders.market(
            symbol="AAPL",
            notional=230.23,
            side="buy",
            take_profit=250.00,
            stop_loss=150.00,
        )
    alpaca.trading.orders.cancel_all()


def test_market_order_with_take_profit(alpaca):
    alpaca.trading.orders.cancel_all()
    try:
        order = alpaca.trading.orders.market(
            symbol="AAPL", qty=1, side="buy", take_profit=250.00, stop_loss=150.00
        )
        assert isinstance(order, OrderModel)
        assert order.legs is not None
        assert order.legs[0].limit_price == 250.00
        assert order.legs[1].stop_price == 150.00
    except Exception as e:
        assert "pattern day trading protection" in str(e)


###########################################
# Test cases for PyAlpacaAPI.limit #
###########################################
def test_limit_order_with_qty(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.limit(
        symbol="AAPL", qty=0.1, side="buy", limit_price=200.00
    )
    assert isinstance(order, OrderModel)
    assert order.status == "accepted"
    assert order.type == "limit"
    assert order.qty == 0.1
    alpaca.trading.orders.cancel_all()


def test_limit_order_with_notional(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.limit(
        symbol="AAPL", notional=2.00, side="buy", limit_price=200.00
    )
    assert isinstance(order, OrderModel)
    assert order.status == "accepted"
    assert order.type == "limit"
    assert order.notional == 2.00
    alpaca.trading.orders.cancel_all()


def test_limit_order_with_fake_symbol(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.limit(
            symbol="FAKESYM", notional=2.00, side="buy", limit_price=200.00
        )
    alpaca.trading.orders.cancel_all()


def test_limit_order_with_no_money(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.limit(
            symbol="AAPL", qty=2000, side="buy", limit_price=200.00
        )
    alpaca.trading.orders.cancel_all()


###########################################
# Test cases for PyAlpacaAPI.stop #
###########################################
@pytest.mark.rate_limited
def test_stop_order_with_qty(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.stop(
        symbol="AAPL", qty=1, side="buy", stop_price=200.00
    )
    assert isinstance(order, OrderModel)
    assert order.status in {"accepted", "pending_new"}
    assert order.type == "stop"
    assert order.qty == 1
    alpaca.trading.orders.cancel_all()


def test_stop_order_with_fake_symbol(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.stop(
            symbol="FAKESYM", qty=1.0, side="buy", stop_price=200.00
        )
    alpaca.trading.orders.cancel_all()


def test_stop_order_with_no_money(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.stop(
            symbol="AAPL", qty=2000, side="buy", stop_price=200.00
        )
    alpaca.trading.orders.cancel_all()


###########################################
# Test cases for PyAlpacaAPI.stop_limit   #
###########################################
def test_stop_limit_order_with_qty(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.stop_limit(
        symbol="AAPL", qty=1, side="buy", stop_price=200.00, limit_price=200.20
    )
    assert isinstance(order, OrderModel)
    assert order.status in {"accepted", "pending_new"}
    assert order.type == "stop_limit"
    assert order.qty == 1
    alpaca.trading.orders.cancel_all()


def test_stop_limit_order_with_fake_symbol(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.stop_limit(
            symbol="FAKESYM",
            qty=2.00,
            side="buy",
            stop_price=200.00,
            limit_price=200.20,
        )
    alpaca.trading.orders.cancel_all()


def test_stop_limit_order_with_no_money(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.stop_limit(
            symbol="AAPL",
            qty=2000,
            side="buy",
            stop_price=200.00,
            limit_price=200.20,
        )
    alpaca.trading.orders.cancel_all()


###########################################
# Test cases for PyAlpacaAPI.trailing_stop   #
###########################################
def test_trailing_stop_order_with_price(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.trailing_stop(
        symbol="AAPL", qty=1, side="buy", trail_price=10.00
    )
    assert isinstance(order, OrderModel)
    assert order.status in {"pending_new", "accepted", "new"}
    assert order.type == "trailing_stop"
    assert order.qty == 1
    alpaca.trading.orders.cancel_all()


def test_trailing_stop_order_with_percent(alpaca):
    alpaca.trading.orders.cancel_all()
    order = alpaca.trading.orders.trailing_stop(
        symbol="AAPL", qty=1, side="buy", trail_percent=2
    )
    assert isinstance(order, OrderModel)
    assert order.status in {"pending_new", "accepted", "new"}
    assert order.type == "trailing_stop"
    assert order.qty == 1
    alpaca.trading.orders.cancel_all()


def test_trailing_stop_order_with_both_percent_and_price(alpaca):
    with pytest.raises(ValidationError):
        alpaca.trading.orders.trailing_stop(
            symbol="AAPL",
            qty=2.00,
            side="buy",
            trail_price=10.00,
            trail_percent=2,
        )
    alpaca.trading.orders.cancel_all()


def test_trailing_stop_order_with_percent_less_than(alpaca):
    with pytest.raises(ValidationError):
        alpaca.trading.orders.trailing_stop(
            symbol="AAPL", qty=2.00, side="buy", trail_percent=-2
        )
    alpaca.trading.orders.cancel_all()


def test_trailing_stop_order_with_fake_symbol(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.trailing_stop(
            symbol="FAKESYM", qty=2.00, side="buy", trail_price=10.00
        )
    alpaca.trading.orders.cancel_all()


def test_trailing_stop_order_with_no_money(alpaca):
    with pytest.raises(APIRequestError):
        alpaca.trading.orders.trailing_stop(
            symbol="AAPL", qty=2000, side="buy", trail_price=10.00
        )
    alpaca.trading.orders.cancel_all()


#################################################
# Test cases for PyAlpacaAPI.get_all_orders #
#################################################
def test_get_all_orders_default(alpaca):
    alpaca.trading.orders.cancel_all()
    # Create a few test orders
    alpaca.trading.orders.market(symbol="AAPL", notional=2.00, side="buy")
    alpaca.trading.orders.market(symbol="MSFT", notional=2.00, side="buy")

    # Get all open orders (default)
    orders = alpaca.trading.orders.get_all_orders()
    assert isinstance(orders, list)
    assert len(orders) >= 2
    assert all(isinstance(order, OrderModel) for order in orders)

    alpaca.trading.orders.cancel_all()


def test_get_all_orders_with_status(alpaca):
    alpaca.trading.orders.cancel_all()
    # Create a test order
    order = alpaca.trading.orders.market(symbol="AAPL", notional=2.00, side="buy")

    # Get open orders
    open_orders = alpaca.trading.orders.get_all_orders(status="open")
    assert isinstance(open_orders, list)
    assert len(open_orders) >= 1

    # Cancel the order
    alpaca.trading.orders.cancel_by_id(order.id)

    # Get all orders including closed
    all_orders = alpaca.trading.orders.get_all_orders(status="all", limit=100)
    assert isinstance(all_orders, list)
    assert any(o.id == order.id for o in all_orders)

    alpaca.trading.orders.cancel_all()


def test_get_all_orders_with_symbols(alpaca):
    alpaca.trading.orders.cancel_all()
    # Create orders for different symbols
    alpaca.trading.orders.market(symbol="AAPL", notional=2.00, side="buy")
    alpaca.trading.orders.market(symbol="MSFT", notional=2.00, side="buy")
    alpaca.trading.orders.market(symbol="GOOGL", notional=2.00, side="buy")

    # Get orders for specific symbols
    filtered_orders = alpaca.trading.orders.get_all_orders(symbols="AAPL,MSFT")
    assert isinstance(filtered_orders, list)
    symbols_in_response = [order.symbol for order in filtered_orders]
    assert all(symbol in ["AAPL", "MSFT"] for symbol in symbols_in_response)

    alpaca.trading.orders.cancel_all()


def test_get_all_orders_with_limit_and_direction(alpaca):
    alpaca.trading.orders.cancel_all()
    # Create multiple orders
    for _i in range(5):
        alpaca.trading.orders.market(symbol="AAPL", notional=2.00, side="buy")

    # Test with limit
    limited_orders = alpaca.trading.orders.get_all_orders(limit=3)
    assert isinstance(limited_orders, list)
    assert len(limited_orders) <= 3

    # Test with ascending direction
    asc_orders = alpaca.trading.orders.get_all_orders(direction="asc")
    assert isinstance(asc_orders, list)

    alpaca.trading.orders.cancel_all()


def test_get_all_orders_invalid_params(alpaca):
    # Test invalid status
    with pytest.raises(ValidationError):
        alpaca.trading.orders.get_all_orders(status="invalid")

    # Test invalid direction
    with pytest.raises(ValidationError):
        alpaca.trading.orders.get_all_orders(direction="invalid")

    # Test invalid limit
    with pytest.raises(ValidationError):
        alpaca.trading.orders.get_all_orders(limit=501)

    with pytest.raises(ValidationError):
        alpaca.trading.orders.get_all_orders(limit=0)
