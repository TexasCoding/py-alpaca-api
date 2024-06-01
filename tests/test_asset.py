import os

import pytest

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import AssetClass

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


########################################
# Test cases for PyAlpacaApi.get_asset #
########################################
def test_get_asset_invalid_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.asset.get("INVALID")


def test_get_asset_attributes(alpaca):
    asset = alpaca.asset.get("AAPL")
    assert asset.symbol == "AAPL"
    assert isinstance(asset, AssetClass)
    assert isinstance(asset.id, str)
    assert isinstance(asset.easy_to_borrow, bool)
    assert isinstance(asset.exchange, str)
    assert isinstance(asset.fractionable, bool)
    assert isinstance(asset.maintenance_margin_requirement, float)
    assert isinstance(asset.marginable, bool)
    assert isinstance(asset.name, str)
    assert isinstance(asset.shortable, bool)
    assert isinstance(asset.status, str)
    assert isinstance(asset.symbol, str)
    assert isinstance(asset.tradable, bool)
