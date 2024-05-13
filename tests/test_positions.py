import os

import pytest

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import PositionClass

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")


@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)


# def test_get_position_by_symbol(alpaca):
#     position = alpaca.get_position(symbol="AAPL")
#     assert position.symbol == "AAPL"
#     assert isinstance(position, PositionClass)
#     assert isinstance(position.asset_id, str)
#     assert isinstance(position.exchange, str)
#     assert isinstance(position.asset_class, str)
#     assert isinstance(position.qty, float)
#     assert isinstance(position.qty_available, float)
#     assert isinstance(position.side, str)
#     assert isinstance(position.market_value, float)
#     assert isinstance(position.cost_basis, float)
#     assert isinstance(position.profit_dol, float)
#     assert isinstance(position.profit_pct, float)
#     assert isinstance(position.intraday_profit_dol, float)
#     assert isinstance(position.intraday_profit_pct, float)
#     assert isinstance(position.portfolio_pct, float)
#     assert isinstance(position.current_price, float)
#     assert isinstance(position.lastday_price, float)
#     assert isinstance(position.change_today, float)
#     assert isinstance(position.asset_marginable, bool)


def test_get_position_by_symbol_dict(alpaca):
    position_dict = {
        "asset_id": "ASSET_ID",
        "symbol": "AAPL",
        "exchange": "NASDAQ",
        "asset_class": "us_equity",
        "avg_entry_price": 100.0,
        "qty": 10.0,
        "qty_available": 10.0,
        "side": "long",
        "market_value": 1000.0,
        "cost_basis": 1000.0,
        "profit_dol": 0.0,
        "profit_pct": 0.0,
        "intraday_profit_dol": 0.0,
        "intraday_profit_pct": 0.0,
        "portfolio_pct": 1.0,
        "current_price": 100.0,
        "lastday_price": 100.0,
        "change_today": 0.0,
        "asset_marginable": True,
    }
    position = alpaca.get_position(symbol_dict=position_dict)
    assert position.symbol == "AAPL"
    assert isinstance(position, PositionClass)
    assert isinstance(position.asset_id, str)
    assert isinstance(position.exchange, str)
    assert isinstance(position.asset_class, str)
    assert isinstance(position.qty, float)
    assert isinstance(position.qty_available, float)
    assert isinstance(position.side, str)
    assert isinstance(position.market_value, float)
    assert isinstance(position.cost_basis, float)
    assert isinstance(position.profit_dol, float)
    assert isinstance(position.profit_pct, float)
    assert isinstance(position.intraday_profit_dol, float)
    assert isinstance(position.intraday_profit_pct, float)
    assert isinstance(position.portfolio_pct, float)
    assert isinstance(position.current_price, float)
    assert isinstance(position.lastday_price, float)
    assert isinstance(position.change_today, float)
    assert isinstance(position.asset_marginable, bool)


#######################################
