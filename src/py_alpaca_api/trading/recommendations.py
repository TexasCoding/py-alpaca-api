import time
from typing import Any, Dict, Union
import pandas as pd
import yfinance as yf


from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(
        RequestRate(2, Duration.SECOND * 5)
    ),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)


class Recommendations:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_recommendations(symbol: str) -> Union[Dict[Any, Any], pd.DataFrame]:
        """
        Retrieves the latest recommendations for a given stock symbol.

        Args:
            symbol (str): The stock symbol for which to retrieve recommendations.

        Returns:
            dict: A dictionary containing the latest recommendations for the stock symbol.
        """
        time.sleep(1)  # To avoid hitting the API rate limit
        ticker = yf.Ticker(symbol, session=session)
        recommendations = ticker.recommendations

        return recommendations.head(2)

    def get_sentiment(self, symbol: str) -> str:
        """
        Retrieves the sentiment for a given stock symbol based on the latest recommendations.

        Args:
            symbol (str): The stock symbol for which to retrieve the sentiment.

        Returns:
            str: The sentiment for the stock symbol, either "BULLISH", "BEARISH", or "NEUTRAL".
        """

        recommendations = self.get_recommendations(symbol)
        if recommendations.empty:
            return "NEUTRAL"
        buy = recommendations["strongBuy"].sum() + recommendations["buy"].sum()
        sell = (
            recommendations["strongSell"].sum()
            + recommendations["sell"].sum()
            + recommendations["hold"].sum()
        )
        return "BULLISH" if (buy / (buy + sell)) > 0.7 else "BEARISH"
