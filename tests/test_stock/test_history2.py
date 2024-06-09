import os
from datetime import datetime

import numpy as np
import pendulum
import pytest

from py_alpaca_api import PyAlpacaAPI

# The following keys are for testing purposes only
# You should never hardcode your keys in your code
# Instead, you should use environment variables
# to store your keys and access them in your code
# Create a .env file in the root directory of the project for the following:
api_key = os.environ.get("ALPACA_API_KEY")
api_secret = os.environ.get("ALPACA_SECRET_KEY")

today = pendulum.now(tz="America/New_York")

previous_day = today.subtract(days=2).format("YYYY-MM-DD")
month_ago = today.subtract(months=1).format("YYYY-MM-DD")


@pytest.fixture
def alpaca():
    return PyAlpacaAPI(api_key=api_key, api_secret=api_secret, api_paper=True)


########################################################
# Test cases for PyAlpacaAPI.get_stock_data #
########################################################
def test_get_stock_data_1d(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="1d"
    )
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


def test_get_stock_data_1w(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="1w"
    )
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


def test_get_stock_data_1m(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="1m"
    )
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


def test_get_stock_data_5m(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="5m"
    )
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


def test_get_stock_data_15m(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="15m"
    )
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


def test_get_stock_data_30m(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="30m"
    )
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


def test_get_stock_data_1h(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="1h"
    )
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


def test_get_stock_data_4h(alpaca):
    stock_data = alpaca.stock.history.get_stock_data(
        symbol="AAPL", start=month_ago, end=previous_day, timeframe="4h"
    )
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
