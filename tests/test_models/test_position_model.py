import pytest
from py_alpaca_api.models.position_model import PositionModel, position_class_from_dict


def test_position_class_from_dict_valid_data():
    data_dict = {
        "asset_id": "12345678",
        "symbol": "AAPL",
        "exchange": "NYSE",
        "asset_class": "equity",
        "avg_entry_price": 100.0,
        "qty": 100,
        "qty_available": 100,
        "side": "long",
        "market_value": 10000.0,
        "cost_basis": 10000.0,
        "profit_dol": 0.0,
        "profit_pct": 0.0,
        "intraday_profit_dol": 0.0,
        "intraday_profit_pct": 0.0,
        "portfolio_pct": 0.0,
        "current_price": 100.0,
        "lastday_price": 100.0,
        "change_today": 0.0,
        "asset_marginable": True,
    }
    expected_position = PositionModel(
        asset_id="12345678",
        symbol="AAPL",
        exchange="NYSE",
        asset_class="equity",
        avg_entry_price=100.0,
        qty=100,
        qty_available=100,
        side="long",
        market_value=10000.0,
        cost_basis=10000.0,
        profit_dol=0.0,
        profit_pct=0.0,
        intraday_profit_dol=0.0,
        intraday_profit_pct=0.0,
        portfolio_pct=0.0,
        current_price=100.0,
        lastday_price=100.0,
        change_today=0.0,
        asset_marginable=True,
    )
    assert position_class_from_dict(data_dict) == expected_position


def test_position_class_from_dict_missing_keys():
    data_dict = {
        "asset_id": "12345678",
        "symbol": "AAPL",
        "exchange": "NYSE",
        "asset_class": "equity",
        "avg_entry_price": 100.0,
        "qty": 100,
        "side": "long",
    }
    with pytest.raises(Exception):
        position_class_from_dict(data_dict)


def test_position_class_from_dict_invalid_data_types():
    data_dict = {
        "asset_id": 12345678,
        "symbol": "AAPL",
        "exchange": "NYSE",
        "asset_class": "equity",
        "avg_entry_price": 100.0,
        "qty": "100",
        "qty_available": 100,
        "side": "long",
        "market_value": str,
        "cost_basis": 10000.0,
        "profit_dol": 0.0,
        "profit_pct": 0.0,
        "intraday_profit_dol": 0.0,
        "intraday_profit_pct": 0.0,
        "portfolio_pct": 0.0,
        "current_price": 100.0,
        "lastday_price": True,
        "change_today": 0.0,
        "asset_marginable": "True",
    }
    with pytest.raises(Exception):
        position_class_from_dict(data_dict)
