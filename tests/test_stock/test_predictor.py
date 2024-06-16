# Retrieve historical stock data for a valid symbol and timeframe
import pandas as pd
import pytest
from py_alpaca_api.stock.history import History
from py_alpaca_api.stock.predictor import Predictor
from py_alpaca_api.stock.screener import Screener
import logging

logger = logging.getLogger("cmdstanpy")
logger.disabled = True
logger.propagate = False


# Handles an empty list of previous day losers
def test_handles_empty_list_of_previous_day_losers(mocker):
    # Mock the Screener and History classes
    mock_screener = mocker.Mock()
    mock_history = mocker.Mock()

    # Mock the losers method to return an empty DataFrame
    mock_screener.losers.return_value = pd.DataFrame(columns=["symbol", "price"])

    # Initialize the Predictor class with the mocked Screener and History
    predictor = Predictor(history=mock_history, screener=mock_screener)

    # Call the method under test
    result = predictor.get_losers_to_gainers()

    # Assert that the result is an empty list
    assert result == []


# Retrieves a list of previous day losers correctly with gain ratio condition
def test_retrieves_previous_day_losers_correctly_with_gain_ratio_condition(mocker):
    mock_screener = mocker.Mock()
    mock_history = mocker.Mock()

    mock_screener.losers.return_value = pd.DataFrame(
        {"symbol": ["AAPL", "MSFT"], "price": [150, 250]}
    )

    mock_history.get_stock_data.return_value = pd.DataFrame(
        {"ds": pd.date_range(start="2020-01-01", periods=100), "y": range(100)}
    )

    predictor = Predictor(history=mock_history, screener=mock_screener)

    mock_model = mocker.Mock()
    mocker.patch.object(Predictor, "train_prophet_model", return_value=mock_model)
    mocker.patch.object(Predictor, "generate_forecast", side_effect=[200, 300])

    result = predictor.get_losers_to_gainers()

    assert result == ["AAPL", "MSFT"]


def test_retrieve_historical_stock_data_valid_symbol(mocker):
    # Mock dependencies
    mock_history = mocker.Mock(spec=History)
    mock_screener = mocker.Mock(spec=Screener)

    # Sample data
    sample_data = pd.DataFrame(
        {
            "date": pd.date_range(start="2020-01-01", periods=5, freq="D"),
            "vwap": [100, 101, 102, 103, 104],
        }
    )
    mock_history.get_stock_data.return_value = sample_data

    # Initialize Predictor
    predictor = Predictor(history=mock_history, screener=mock_screener)

    # Call method under test
    result = predictor.get_stock_data(
        symbol="AAPL", start="2020-01-01", end="2020-01-05"
    )

    # Assertions
    assert not result.empty
    assert list(result.columns) == ["ds", "y"]
    assert len(result) == 5
    mock_history.get_stock_data.assert_called_once_with(
        symbol="AAPL", start="2020-01-01", end="2020-01-05", timeframe="1d"
    )


# Handle invalid stock symbols gracefully
def test_handle_invalid_stock_symbols_gracefully(mocker):
    # Mock dependencies
    mock_history = mocker.Mock(spec=History)
    mock_screener = mocker.Mock(spec=Screener)

    # Mock the get_stock_data method to raise a ValueError for invalid symbol
    mock_history.get_stock_data.side_effect = ValueError("Invalid stock symbol")

    # Initialize Predictor
    predictor = Predictor(history=mock_history, screener=mock_screener)

    # Call method under test and assert exception is raised
    with pytest.raises(ValueError, match="Invalid stock symbol"):
        predictor.get_stock_data(symbol="INVALID", start="2020-01-01", end="2020-01-05")

    # Ensure the method was called with the invalid symbol
    mock_history.get_stock_data.assert_called_once_with(
        symbol="INVALID", start="2020-01-01", end="2020-01-05", timeframe="1d"
    )


class TestGetLosersToGainers:
    def test_get_losers_to_gainers_with_no_losers(self, mocker):
        mock_screener = mocker.Mock()
        mock_history = mocker.Mock()
        mock_screener.losers.return_value = pd.DataFrame(columns=["symbol", "price"])
        predictor = Predictor(history=mock_history, screener=mock_screener)
        result = predictor.get_losers_to_gainers()
        assert result == []

    def test_get_losers_to_gainers_with_all_gainers(self, mocker):
        mock_screener = mocker.Mock()
        mock_history = mocker.Mock()
        mock_screener.losers.return_value = pd.DataFrame(
            {"symbol": ["AAPL", "MSFT"], "price": [150, 250]}
        )
        mock_history.get_stock_data.return_value = pd.DataFrame(
            {"ds": pd.date_range(start="2020-01-01", periods=100), "y": range(100, 200)}
        )
        predictor = Predictor(history=mock_history, screener=mock_screener)
        mock_model = mocker.Mock()
        mocker.patch.object(Predictor, "train_prophet_model", return_value=mock_model)
        mocker.patch.object(Predictor, "generate_forecast", side_effect=[300, 400])
        result = predictor.get_losers_to_gainers()
        assert result == ["AAPL", "MSFT"]

    def test_get_losers_to_gainers_with_mixed_gainers_and_losers(self, mocker):
        mock_screener = mocker.Mock()
        mock_history = mocker.Mock()
        mock_screener.losers.return_value = pd.DataFrame(
            {"symbol": ["AAPL", "MSFT", "GOOG"], "price": [150, 250, 350]}
        )
        mock_history.get_stock_data.side_effect = [
            pd.DataFrame(
                {
                    "ds": pd.date_range(start="2020-01-01", periods=100),
                    "y": range(100, 200),
                }
            ),
            pd.DataFrame(
                {
                    "ds": pd.date_range(start="2020-01-01", periods=100),
                    "y": range(200, 100, -1),
                }
            ),
            pd.DataFrame(
                {
                    "ds": pd.date_range(start="2020-01-01", periods=100),
                    "y": range(100, 200),
                }
            ),
        ]
        predictor = Predictor(history=mock_history, screener=mock_screener)
        mock_model = mocker.Mock()
        mocker.patch.object(Predictor, "train_prophet_model", return_value=mock_model)
        mocker.patch.object(Predictor, "generate_forecast", side_effect=[300, 200, 400])
        result = predictor.get_losers_to_gainers()
        assert result == ["AAPL", "GOOG"]
