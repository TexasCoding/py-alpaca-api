# Converts a valid dictionary to a PositionModel object successfully
from py_alpaca_api.models.position_model import position_class_from_dict


# Handles missing optional field 'asset_marginable' by setting it to default value
def test_handles_missing_optional_fields_with_default_value():
    data_dict = {
        "asset_id": "123",
        "symbol": "AAPL",
        "exchange": "NASDAQ",
        "class": "equity",
        "avg_entry_price": 150.0,
        "qty": 10.0,
        "qty_available": 10.0,
        "side": "long",
        "market_value": 1500.0,
        "cost_basis": 1500.0,
        "profit_dol": 100.0,
        "profit_pct": 0.0667,
        "intraday_profit_dol": 10.0,
        "intraday_profit_pct": 0.0067,
        "portfolio_pct": 0.1,
        "current_price": 155.0,
        "lastday_price": 150.0,
        "change_today": 0.0333,
        "asset_marginable": False,
    }
    position = position_class_from_dict(data_dict)
    assert position.asset_id == "123"
    assert position.symbol == "AAPL"
    assert position.exchange == "NASDAQ"
    assert position.asset_class == "equity"
    assert position.avg_entry_price == 150.0
    assert position.qty == 10.0
    assert position.qty_available == 10.0
    assert position.side == "long"
    assert position.market_value == 1500.0
    assert position.cost_basis == 1500.0
    assert position.profit_dol == 100.0
    assert position.profit_pct == 0.0667
    assert position.intraday_profit_dol == 10.0
    assert position.intraday_profit_pct == 0.0067
    assert position.portfolio_pct == 0.1
    assert position.current_price == 155.0
    assert position.lastday_price == 150.0
    assert position.change_today == 0.0333
    assert position.asset_marginable is False


def test_converts_valid_dict_to_position_model():
    data_dict = {
        "asset_id": "123",
        "symbol": "AAPL",
        "exchange": "NASDAQ",
        "class": "equity",
        "avg_entry_price": 150.0,
        "qty": 10.0,
        "qty_available": 10.0,
        "side": "long",
        "market_value": 1500.0,
        "cost_basis": 1500.0,
        "profit_dol": 100.0,
        "profit_pct": 0.0667,
        "intraday_profit_dol": 10.0,
        "intraday_profit_pct": 0.0067,
        "portfolio_pct": 0.1,
        "current_price": 155.0,
        "lastday_price": 150.0,
        "change_today": 0.0333,
        "asset_marginable": True,
    }
    position = position_class_from_dict(data_dict)
    assert position.asset_id == "123"
    assert position.symbol == "AAPL"
    assert position.exchange == "NASDAQ"
    assert position.asset_class == "equity"
    assert position.avg_entry_price == 150.0
    assert position.qty == 10.0
    assert position.qty_available == 10.0
    assert position.side == "long"
    assert position.market_value == 1500.0
    assert position.cost_basis == 1500.0
    assert position.profit_dol == 100.0
    assert position.profit_pct == 0.0667
    assert position.intraday_profit_dol == 10.0
    assert position.intraday_profit_pct == 0.0067
    assert position.portfolio_pct == 0.1
    assert position.current_price == 155.0
    assert position.lastday_price == 150.0
    assert position.change_today == 0.0333
    assert position.asset_marginable is True
