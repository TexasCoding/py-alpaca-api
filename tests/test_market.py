import os
from datetime import datetime

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


def test_market_clock_success(alpaca):
    clock = alpaca.market.clock()
    assert isinstance(clock, ClockClass)
    assert isinstance(clock.market_time, datetime)
    assert isinstance(clock.next_open, datetime)
    assert isinstance(clock.next_close, datetime)
    assert isinstance(clock.is_open, bool)


########################################
