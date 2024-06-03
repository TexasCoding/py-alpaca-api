import sys
from unittest.mock import MagicMock

import pandas as pd
import pytest

from py_alpaca_api.src.predictor import Predictor

sys.path.append("py_alpaca_api/src")


@pytest.fixture(scope="module")
def predictor():
    history = MagicMock()
    screener = MagicMock()
    return Predictor(history, screener)


def test_get_losers_to_gainers_with_exception_handling(predictor):
    predictor.get_stock_data = MagicMock(return_value=pd.DataFrame())
    predictor.train_prophet_model = MagicMock(return_value=MagicMock())
    predictor.generate_forecast = MagicMock(side_effect=Exception("Random error"))
    assert predictor.get_losers_to_gainers() == []


def test_get_losers_to_gainers_when_forecast_price_is_less_than_previous_price(predictor):
    ticker = "AAPL"
    predictor.get_stock_data = MagicMock(return_value=pd.DataFrame())
    predictor.train_prophet_model = MagicMock(return_value=MagicMock())
    predictor.screener.losers = MagicMock(return_value=pd.DataFrame({"symbol": [ticker], "price": [10]}))
    predictor.generate_forecast = MagicMock(return_value=5)
    assert predictor.get_losers_to_gainers() == []


def test_get_losers_to_gainers_when_forecast_price_is_greater_than_previous_price(predictor):
    ticker = "AAPL"
    predictor.get_stock_data = MagicMock(return_value=pd.DataFrame())
    predictor.train_prophet_model = MagicMock(return_value=MagicMock())
    predictor.screener.losers = MagicMock(return_value=pd.DataFrame({"symbol": [ticker], "price": [10.00]}))
    predictor.generate_forecast = MagicMock(return_value=20.00)
    assert predictor.get_losers_to_gainers() == [ticker]
