import os

import pandas as pd
import pytest

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import PositionClass

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")


@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)


def test_get_positions_and_cash_row_exists(alpaca):
    positions = alpaca.get_positions()
    assert isinstance(positions, pd.DataFrame)
    assert positions[positions["symbol"] == "Cash"].shape[0] == 1
    assert positions[positions["symbol"] == "Cash"].iloc[0]["market_value"] == alpaca.get_account().cash


def test_get_positions_and_position_by_symbol(alpaca):
    positions = alpaca.get_positions()
    assert isinstance(positions, pd.DataFrame)
    for i, position in positions[positions["symbol"] != "Cash"].iterrows():
        cur_position = alpaca.get_position(symbol=position["symbol"])
        assert isinstance(cur_position, PositionClass)
        assert isinstance(cur_position.asset_id, str)
        assert isinstance(cur_position.exchange, str)
        assert isinstance(cur_position.asset_class, str)
        assert isinstance(cur_position.qty, float)
        assert isinstance(cur_position.qty_available, float)
        assert isinstance(cur_position.side, str)
        assert isinstance(cur_position.market_value, float)
        assert isinstance(cur_position.cost_basis, float)
        assert isinstance(cur_position.profit_dol, float)
        assert isinstance(cur_position.profit_pct, float)
        assert isinstance(cur_position.intraday_profit_dol, float)
        assert isinstance(cur_position.intraday_profit_pct, float)
        assert isinstance(cur_position.portfolio_pct, float)
        assert isinstance(cur_position.current_price, float)
        assert isinstance(cur_position.lastday_price, float)
        assert isinstance(cur_position.change_today, float)
        assert isinstance(cur_position.asset_marginable, bool)


def test_get_positions_and_position_by_symbol_dict(alpaca):
    positions = alpaca.get_positions()
    assert isinstance(positions, pd.DataFrame)
    for i, position in positions[positions["symbol"] != "Cash"].iterrows():
        cur_position = alpaca.get_position(symbol_dict=position.squeeze().to_dict())
        assert isinstance(cur_position, PositionClass)
        assert isinstance(cur_position.asset_id, str)
        assert isinstance(cur_position.exchange, str)
        assert isinstance(cur_position.asset_class, str)
        assert isinstance(cur_position.qty, float)
        assert isinstance(cur_position.qty_available, float)
        assert isinstance(cur_position.side, str)
        assert isinstance(cur_position.market_value, float)
        assert isinstance(cur_position.cost_basis, float)
        assert isinstance(cur_position.profit_dol, float)
        assert isinstance(cur_position.profit_pct, float)
        assert isinstance(cur_position.intraday_profit_dol, float)
        assert isinstance(cur_position.intraday_profit_pct, float)
        assert isinstance(cur_position.portfolio_pct, float)
        assert isinstance(cur_position.current_price, float)
        assert isinstance(cur_position.lastday_price, float)
        assert isinstance(cur_position.change_today, float)
        assert isinstance(cur_position.asset_marginable, bool)


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
