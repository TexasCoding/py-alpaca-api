import logging

import pandas as pd
import pendulum
from prophet import Prophet
from tqdm import tqdm

from py_alpaca_api.stock.history import History
from py_alpaca_api.stock.screener import Screener

yesterday = pendulum.now().subtract(days=1).format("YYYY-MM-DD")
four_years_ago = pendulum.now().subtract(years=2).format("YYYY-MM-DD")

logger = logging.getLogger("cmdstanpy")
logger.disabled = True
logger.propagate = False


class Predictor:
    def __init__(self, history: History, screener: Screener) -> None:
        self.history = history
        self.screener = screener

    def get_stock_data(
        self,
        symbol: str,
        timeframe: str = "1d",
        start: str = four_years_ago,
        end: str = yesterday,
    ) -> pd.DataFrame:
        """
        Retrieves historical stock data for a given symbol within a specified timeframe.

        Args:
            symbol (str): The stock symbol to retrieve data for.
            timeframe (str, optional): The timeframe for the data. Defaults to "1d".
            start (str, optional): The start date for the data. Defaults to four_years_ago.
            end (str, optional): The end date for the data. Defaults to yesterday.

        Returns:
            pd.DataFrame: A DataFrame containing the historical stock data with columns "ds" (date) and "y" (vwap).
        """
        stock_df = self.history.get_stock_data(
            symbol=symbol,
            start=start,
            end=end,
            timeframe=timeframe,
        )
        stock_df.rename(columns={"date": "ds", "vwap": "y"}, inplace=True)

        return stock_df[["ds", "y"]]

    @staticmethod
    def train_prophet_model(data):
        """
        Trains a Prophet model using the provided data.

        Args:
            data: The input data used for training the model.

        Returns:
            The trained Prophet model.
        """
        model = Prophet(
            changepoint_prior_scale=0.05,
            holidays_prior_scale=15,
            seasonality_prior_scale=10,
            weekly_seasonality=True,
            yearly_seasonality=True,
            daily_seasonality=False,
        )
        model.add_country_holidays(country_name="US")
        model.fit(data)
        return model

    @staticmethod
    def generate_forecast(model, future_periods=14):
        """
        Generates a forecast using the specified model for a given number of future periods.

        Args:
            model: The model used for forecasting.
            future_periods: The number of future periods to forecast.

        Returns:
            The forecasted value for the next two weeks.
        """
        future = model.make_future_dataframe(periods=future_periods)
        forecast = model.predict(future)

        two_week_forecast = (
            forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
            .tail(1)
            .reset_index(drop=True)
            .iloc[0]
            .yhat
        )

        return round(two_week_forecast, 2)

    def get_losers_to_gainers(
        self,
        gain_ratio: float = 10.0,
        losers_to_scan: int = 200,
        future_periods: int = 14,
    ) -> list:
        """
        Predicts future gainers based on the previous day's losers using Prophet forecasting.

        Args:
            gain_ratio: The minimum gain ratio required for a stock to be considered a future gainer.
            losers_to_scan: The number of previous day's losers to scan.
            future_periods: The number of future periods to forecast.

        Returns:
            A list of future gainers.

        Raises:
            Exception: If there is an error while predicting future gainers for a stock.
        """
        previous_day_losers = self.screener.losers(total_losers_returned=losers_to_scan)
        losers_list = previous_day_losers["symbol"].tolist()

        future_gainers = []

        for i, ticker in tqdm(
            enumerate(losers_list),
            desc=f"• Predicting {len(losers_list)} future gainers with Prophet: ",
        ):
            try:
                symbol_data = self.get_stock_data(ticker)
                symbol_model = self.train_prophet_model(symbol_data)
                symbol_forecast = self.generate_forecast(
                    symbol_model, future_periods=future_periods
                )
                previous_price = previous_day_losers[
                    previous_day_losers["symbol"] == ticker
                ].iloc[0]["price"]
                gain_prediction = round(
                    ((symbol_forecast - previous_price) / previous_price) * 100, 2
                )
                if gain_prediction >= gain_ratio:
                    future_gainers.append(ticker)
            except Exception as e:
                logger.error(f"Error predicting {ticker}: {e}")
                continue

        return future_gainers
