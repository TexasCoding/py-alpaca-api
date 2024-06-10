import os
import pandas as pd
import pytest
from py_alpaca_api import PyAlpacaAPI

api_key = os.environ.get("ALPACA_API_KEY")
api_secret = os.environ.get("ALPACA_SECRET_KEY")


@pytest.fixture
def news():
    return PyAlpacaAPI(api_key=api_key, api_secret=api_secret).trading.recommendations


def test_get_recommendations(news):
    recommendations = news.get_recommendations("AAPL")
    assert len(recommendations) > 0
    assert isinstance(recommendations, pd.DataFrame)
    assert "period" in recommendations.columns
    assert "strongBuy" in recommendations.columns
    assert "buy" in recommendations.columns
    assert "hold" in recommendations.columns
    assert "sell" in recommendations.columns
    assert "strongSell" in recommendations.columns


def test_get_sentiment(news):
    sentiment = news.get_sentiment("AAPL")
    assert isinstance(sentiment, str)
    assert sentiment in ["BULLISH", "BEARISH", "NEUTRAL"]
