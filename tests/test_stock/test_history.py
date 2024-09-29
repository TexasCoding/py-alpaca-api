import pytest
import os


class TestGetStockData:
    @pytest.fixture
    def stock_client(self):
        from py_alpaca_api import PyAlpacaAPI

        api_key = os.environ.get("ALPACA_API_KEY")
        api_secret = os.environ.get("ALPACA_SECRET_KEY")
        stock_client = PyAlpacaAPI(api_key=api_key, api_secret=api_secret).stock.history
        return stock_client

    def test_invalid_timeframe(self, stock_client):
        with pytest.raises(ValueError, match="Invalid timeframe"):
            stock_client.get_stock_data(
                "AAPL", "2022-01-01", "2022-01-31", timeframe="invalid"
            )

    def test_limit_exceeded(self, stock_client):
        with pytest.raises(
            Exception,
            match='Request Error: {"message":"invalid limit: larger than the allowed maximum of 10000"}',
        ):
            stock_client.get_stock_data(
                "AAPL", "2022-01-01", "2022-01-31", limit=100000
            )

    def test_start_date_after_end_date(self, stock_client):
        with pytest.raises(
            Exception,
            match='Request Error: {"message":"end should not be before start"}',
        ):
            stock_client.get_stock_data(
                "AAPL", "2022-01-31", "2022-01-01", timeframe="1d"
            )

    def test_invalid_symbol(self, stock_client):
        with pytest.raises(
            Exception,
            match='Request Error: {"code":40410000,"message":"asset not found for INVALID"}',
        ):
            stock_client.get_stock_data(
                "INVALID", "2022-01-01", "2022-01-31", timeframe="1d"
            )

    def test_data_frame_shape(self, stock_client):
        df = stock_client.get_stock_data(
            "AAPL", "2022-01-01", "2022-01-31", timeframe="1d"
        )
        assert df.shape[0] > 0
        assert df.shape[1] == 9

    def test_data_frame_columns(self, stock_client):
        df = stock_client.get_stock_data(
            "AAPL", "2022-01-01", "2022-01-31", timeframe="1d"
        )
        expected_columns = [
            "symbol",
            "close",
            "high",
            "low",
            "trade_count",
            "open",
            "date",
            "volume",
            "vwap",
        ]
        assert list(df.columns) == expected_columns
