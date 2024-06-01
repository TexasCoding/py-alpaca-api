import os
from datetime import datetime, time

import pandas as pd
import pytest

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import ClockClass

# The following keys are for testing purposes only
# You should never hardcode your keys in your code
# Instead, you should use environment variables
# to store your keys and access them in your code
# Create a .env file in the root directory of the project for the following:
api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")


@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)


def test_calender(alpaca):
    calender = alpaca.market.calender(start_date="2024-05-25", end_date="2024-06-06")
    assert isinstance(calender, pd.DataFrame)
    assert isinstance(calender.date[0], datetime)
    assert isinstance(calender.settlement_date[0], datetime)
    assert isinstance(calender.open[0], time)
    assert isinstance(calender.close[0], time)


def test_market_clock_success(alpaca):
    clock = alpaca.market.clock()
    assert isinstance(clock, ClockClass)
    assert isinstance(clock.market_time, datetime)
    assert isinstance(clock.next_open, datetime)
    assert isinstance(clock.next_close, datetime)
    assert isinstance(clock.is_open, bool)


########################################
