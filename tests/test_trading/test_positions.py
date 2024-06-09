# Retrieves all positions successfully with correct sorting by profit_pct in descending order
import json
from py_alpaca_api.trading.positions import Positions


# Retrieves position successfully when valid symbol is provided
def test_retrieves_position_successfully_with_valid_symbol(mocker):
    mock_response = [
        {
            "asset_id": "1",
            "symbol": "AAPL",
            "exchange": "NASDAQ",
            "asset_class": "stock",
            "avg_entry_price": 150.0,
            "qty": 10,
            "qty_available": 10,
            "side": "long",
            "market_value": 1600.0,
            "cost_basis": 1500.0,
            "unrealized_pl": 100.0,
            "unrealized_plpc": 0.0667,
            "unrealized_intraday_pl": 10.0,
            "unrealized_intraday_plpc": 0.0067,
            "current_price": 160.0,
            "lastday_price": 159.0,
            "change_today": 0.0063,
            "asset_marginable": True,
        }
    ]
    mocker.patch(
        "py_alpaca_api.http.requests.Requests.request",
        return_value=mocker.Mock(text=json.dumps(mock_response)),
    )
    mock_account = mocker.Mock()
    mock_account.get.return_value.cash = 1000.0
    positions = Positions(
        "https://api.alpaca.markets",
        {"Authorization": "Bearer YOUR_API_KEY"},
        mock_account,
    )
    result = positions.get("AAPL")
    assert result.symbol == "AAPL"


def test_retrieves_all_positions_successfully_with_default_sorting(mocker):
    mock_response = [
        {
            "asset_id": "1",
            "symbol": "AAPL",
            "exchange": "NASDAQ",
            "asset_class": "stock",
            "avg_entry_price": 150.0,
            "qty": 10,
            "qty_available": 10,
            "side": "long",
            "market_value": 1600.0,
            "cost_basis": 1500.0,
            "unrealized_pl": 100.0,
            "unrealized_plpc": 0.0667,
            "unrealized_intraday_pl": 10.0,
            "unrealized_intraday_plpc": 0.0067,
            "current_price": 160.0,
            "lastday_price": 159.0,
            "change_today": 0.0063,
            "asset_marginable": True,
        }
    ]
    mocker.patch(
        "py_alpaca_api.http.requests.Requests.request",
        return_value=mocker.Mock(text=json.dumps(mock_response)),
    )
    mock_account = mocker.Mock()
    mock_account.get.return_value.cash = 1000.0
    positions = Positions(
        "https://api.alpaca.markets",
        {"Authorization": "Bearer YOUR_API_KEY"},
        mock_account,
    )
    result = positions.get_all(order_by="profit_pct", order_asc=False)
    assert not result.empty
    assert result.iloc[0]["symbol"] == "AAPL"
    assert result.iloc[1]["symbol"] == "Cash"


def test_raises_value_error_when_symbol_not_provided_with_mock_account():
    import pytest

    class MockAccount:
        def get(self):
            return type("obj", (object,), {"cash": 1000})()

    positions = Positions(
        "https://api.alpaca.markets",
        {"Authorization": "Bearer YOUR_API_KEY"},
        MockAccount(),
    )
    with pytest.raises(ValueError, match="Symbol is required."):
        positions.get("")


def test_retrieves_all_positions_successfully_with_correct_sorting(mocker):
    mock_response = [
        {
            "asset_id": "1",
            "symbol": "AAPL",
            "exchange": "NASDAQ",
            "asset_class": "stock",
            "avg_entry_price": 150.0,
            "qty": 10,
            "qty_available": 10,
            "side": "long",
            "market_value": 1600.0,
            "cost_basis": 1500.0,
            "unrealized_pl": 100.0,
            "unrealized_plpc": 0.0667,
            "unrealized_intraday_pl": 10.0,
            "unrealized_intraday_plpc": 0.0067,
            "current_price": 160.0,
            "lastday_price": 159.0,
            "change_today": 0.0063,
            "asset_marginable": True,
        }
    ]
    mocker.patch(
        "py_alpaca_api.http.requests.Requests.request",
        return_value=mocker.Mock(text=json.dumps(mock_response)),
    )
    mock_account = mocker.Mock()
    mock_account.get.return_value.cash = 1000.0
    positions = Positions(
        "https://api.alpaca.markets",
        {"Authorization": "Bearer YOUR_API_KEY"},
        mock_account,
    )
    result = positions.get_all(order_by="profit_pct", order_asc=False)
    assert not result.empty
    assert result.iloc[0]["symbol"] == "AAPL"
    assert result.iloc[1]["symbol"] == "Cash"


def test_retrieves_all_positions_successfully_with_correct_sorting_ascending_fixed(
    mocker,
):
    mock_response = [
        {
            "asset_id": "1",
            "symbol": "AAPL",
            "exchange": "NASDAQ",
            "asset_class": "stock",
            "avg_entry_price": 150.0,
            "qty": 10,
            "qty_available": 10,
            "side": "long",
            "market_value": 1600.0,
            "cost_basis": 1500.0,
            "unrealized_pl": 100.0,
            "unrealized_plpc": 0.0667,
            "unrealized_intraday_pl": 10.0,
            "unrealized_intraday_plpc": 0.0067,
            "current_price": 160.0,
            "lastday_price": 159.0,
            "change_today": 0.0063,
            "asset_marginable": True,
        }
    ]
    mocker.patch(
        "py_alpaca_api.http.requests.Requests.request",
        return_value=mocker.Mock(text=json.dumps(mock_response)),
    )
    mock_account = mocker.Mock()
    mock_account.get.return_value.cash = 1000.0
    positions = Positions(
        "https://api.alpaca.markets",
        {"Authorization": "Bearer YOUR_API_KEY"},
        mock_account,
    )
    result = positions.get_all(order_by="profit_pct", order_asc=True)
    assert not result.empty
    assert result.iloc[0]["symbol"] == "Cash"
    assert result.iloc[1]["symbol"] == "AAPL"
