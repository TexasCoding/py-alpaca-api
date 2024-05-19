import os

import pytest

from py_alpaca_api.alpaca import PyAlpacaApi

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


#########################################
##### Test cases for PyAlpacaApi ########
#########################################
def test_alpaca_key_exceptions(alpaca):
    with pytest.raises(ValueError):
        PyAlpacaApi(api_key="", api_secret=api_secret, api_paper=True)
    with pytest.raises(ValueError):
        PyAlpacaApi(api_key=api_key, api_secret="", api_paper=True)
