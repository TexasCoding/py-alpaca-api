import time
from typing import Any

import pandas as pd
import yfinance as yf


class Recommendations:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_recommendations(symbol: str) -> dict[Any, Any] | pd.DataFrame:
        """Retrieves the latest recommendations for a given stock symbol.

        Args:
            symbol (str): The stock symbol for which to retrieve recommendations.

        Returns:
            Union[dict, pd.DataFrame]: A dictionary or DataFrame containing the latest recommendations for the stock symbol.
        """
        time.sleep(1)  # To avoid hitting the API rate limit
        ticker = yf.Ticker(symbol)
        recommendations = ticker.recommendations

        # Handle the case where recommendations could be None or empty
        if recommendations is None or not isinstance(recommendations, pd.DataFrame):
            return {}

        # Ensure we return a DataFrame, not a Series
        result = recommendations.head(2)
        if isinstance(result, pd.Series):
            return result.to_frame()
        return result

    def get_sentiment(self, symbol: str) -> str:
        """Retrieves the sentiment for a given stock symbol based on the latest recommendations.

        Args:
            symbol (str): The stock symbol for which to retrieve the sentiment.

        Returns:
            str: The sentiment for the stock symbol, either "BULLISH", "BEARISH", or "NEUTRAL".
        """
        recommendations = self.get_recommendations(symbol)

        # Type guard: check if recommendations is a DataFrame and not empty
        if isinstance(recommendations, dict) or (
            isinstance(recommendations, pd.DataFrame) and recommendations.empty
        ):
            return "NEUTRAL"

        # At this point we know recommendations is a non-empty DataFrame
        assert isinstance(recommendations, pd.DataFrame)
        buy = recommendations["strongBuy"].sum() + recommendations["buy"].sum()
        sell = (
            recommendations["strongSell"].sum()
            + recommendations["sell"].sum()
            + recommendations["hold"].sum()
        )
        return "BULLISH" if (buy / (buy + sell)) > 0.7 else "BEARISH"
