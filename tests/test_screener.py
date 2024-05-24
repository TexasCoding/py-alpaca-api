import os
from datetime import datetime, timedelta

import numpy as np
import pytest
from pytz import timezone

from py_alpaca_api.alpaca import PyAlpacaApi

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


def test_get_top_50_gainers(alpaca):
    gainers = alpaca.screener.gainers(total_gainers_returned=50)
    assert not gainers.empty
    assert len(gainers) == 50
    assert isinstance(gainers["symbol"][0], str)
    assert isinstance(gainers["price"][0], float)
    assert isinstance(gainers["change"][0], float)
    assert isinstance(gainers["volume"][0], np.int64)
    assert isinstance(gainers["trades"][0], np.int64)
    assert gainers["price"][0] > 5.0
    assert gainers["change"][0] > 2.0
    assert gainers["volume"][0] > 20000
    assert gainers["trades"][0] > 2000


def test_get_top_50_losers(alpaca):
    losers = alpaca.screener.losers(total_losers_returned=50)
    assert not losers.empty
    assert len(losers) == 50
    assert isinstance(losers["symbol"][0], str)
    assert isinstance(losers["price"][0], float)
    assert isinstance(losers["change"][0], float)
    assert isinstance(losers["volume"][0], np.int64)
    assert isinstance(losers["trades"][0], np.int64)
    assert losers["price"][0] > 5.0
    assert losers["change"][0] < -2.0
    assert losers["volume"][0] > 20000
    assert losers["trades"][0] > 2000


def test_losers_by_volume(alpaca):
    losers = alpaca.screener.losers(
        total_losers_returned=10, volume_greater_than=50000
    )
    assert not losers.empty
    assert losers["volume"][0] > 50000


def test_gainers_by_volume(alpaca):
    gainers = alpaca.screener.gainers(
        total_gainers_returned=10, volume_greater_than=50000
    )
    assert not gainers.empty
    assert gainers["volume"][0] > 50000
