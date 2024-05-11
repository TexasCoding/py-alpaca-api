import os
from datetime import datetime, timedelta

import numpy as np
import pytest
from pytz import timezone

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import AccountClass, AssetClass, OrderClass

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
def alpaca_wrong_keys():
    return PyAlpacaApi(api_key="api_key", api_secret="api_secret", api_paper=True)


@pytest.fixture
def alpaca_create_order(alpaca):
    return alpaca.market_order(symbol="AAPL", notional=2.25, side="buy")


#########################################
##### Test cases for PyAlpacaApi ########
#########################################
def test_alpaca_key_exceptions(alpaca):
    with pytest.raises(ValueError):
        PyAlpacaApi(api_key="", api_secret=api_secret, api_paper=True)
    with pytest.raises(ValueError):
        PyAlpacaApi(api_key=api_key, api_secret="", api_paper=True)


def test_get_account_wrong_keys(alpaca_wrong_keys):
    with pytest.raises(Exception):
        alpaca_wrong_keys.get_account()


########################################################
# Test cases for PyAlpacaApi.get_stock_historical_data #
########################################################
def test_get_stock_historical_data_1d(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="1d")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_1w(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="1w")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_1m(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="1m")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_5m(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="5m")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_15m(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="15m")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_30m(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="30m")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_1h(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="1h")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


def test_get_stock_historical_data_4h(alpaca):
    stock_data = alpaca.get_stock_historical_data(symbol="AAPL", start=month_ago, end=previous_day, timeframe="4h")
    assert not stock_data.empty
    assert stock_data["symbol"][0] == "AAPL"
    assert isinstance(stock_data["close"][0], float)
    assert isinstance(stock_data["open"][0], float)
    assert isinstance(stock_data["low"][0], float)
    assert isinstance(stock_data["high"][0], float)
    assert isinstance(stock_data["vwap"][0], float)
    assert isinstance(stock_data["trade_count"][0], np.int64)
    assert isinstance(stock_data["volume"][0], np.int64)
    assert isinstance(stock_data["date"][0], datetime)
    assert isinstance(stock_data["symbol"][0], str)


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
    assert order.status == "accepted"
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


########################################
# Test cases for PyAlpacaApi.get_asset #
########################################
def test_get_asset_invalid_symbol(alpaca):
    with pytest.raises(ValueError):
        alpaca.get_asset("INVALID")


def test_get_asset(alpaca):
    assert isinstance(alpaca.get_asset("AAPL"), AssetClass)
    assert alpaca.get_asset("AAPL").symbol == "AAPL"


def test_get_asset_attributes(alpaca):
    asset = alpaca.get_asset("AAPL")
    assert hasattr(asset, "id")
    assert hasattr(asset, "asset_class")
    assert hasattr(asset, "easy_to_borrow")
    assert hasattr(asset, "exchange")
    assert hasattr(asset, "fractionable")
    assert hasattr(asset, "maintenance_margin_requirement")
    assert hasattr(asset, "marginable")
    assert hasattr(asset, "name")
    assert hasattr(asset, "shortable")
    assert hasattr(asset, "status")
    assert hasattr(asset, "symbol")
    assert hasattr(asset, "tradable")


##########################################
# Test cases for PyAlpacaApi.get_account #
##########################################
def test_get_account(alpaca):
    account = alpaca.get_account()
    assert isinstance(account, AccountClass)
    assert account.id != ""
    assert account.account_number != ""
    assert account.status != ""
    assert account.currency != ""


def test_get_account_attributes(alpaca):
    account = alpaca.get_account()
    assert hasattr(account, "id")
    assert hasattr(account, "admin_configurations")
    assert hasattr(account, "user_configurations")
    assert hasattr(account, "account_number")
    assert hasattr(account, "status")
    assert hasattr(account, "crypto_status")
    assert hasattr(account, "options_approved_level")
    assert hasattr(account, "options_trading_level")
    assert hasattr(account, "currency")
    assert hasattr(account, "buying_power")
    assert hasattr(account, "regt_buying_power")
    assert hasattr(account, "daytrading_buying_power")
    assert hasattr(account, "effective_buying_power")
    assert hasattr(account, "non_marginable_buying_power")
    assert hasattr(account, "options_buying_power")
    assert hasattr(account, "bod_dtbp")
    assert hasattr(account, "cash")
    assert hasattr(account, "accrued_fees")
    assert hasattr(account, "pending_transfer_in")
    assert hasattr(account, "portfolio_value")
    assert hasattr(account, "pattern_day_trader")
    assert hasattr(account, "trading_blocked")
    assert hasattr(account, "transfers_blocked")
    assert hasattr(account, "account_blocked")
    assert hasattr(account, "created_at")
    assert hasattr(account, "trade_suspended_by_user")
    assert hasattr(account, "multiplier")
    assert hasattr(account, "shorting_enabled")
    assert hasattr(account, "equity")
    assert hasattr(account, "last_equity")
    assert hasattr(account, "long_market_value")
    assert hasattr(account, "short_market_value")
    assert hasattr(account, "position_market_value")
    assert hasattr(account, "initial_margin")
    assert hasattr(account, "maintenance_margin")
    assert hasattr(account, "last_maintenance_margin")
    assert hasattr(account, "sma")
    assert hasattr(account, "daytrade_count")
    assert hasattr(account, "balance_asof")
    assert hasattr(account, "crypto_tier")
    assert hasattr(account, "intraday_adjustments")
    assert hasattr(account, "pending_reg_taf_fees")
