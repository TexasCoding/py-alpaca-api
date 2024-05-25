# Import needed packages
# Import some mocks
from unittest.mock import patch

import pytest

from py_alpaca_api.src.data_classes import PositionClass
from py_alpaca_api.src.position import Position

# Create sample data
sample_response = {
    "asset_class": "us_equity",
    "asset_id": "375f6b6e-3b5f-4b2b-8f6b-2e6b2a6b2e6b",
    "avg_entry_price": "100.0",
    "change_today": "0.0",
    "cost_basis": "1000.0",
    "current_price": "100.0",
    "exchange": "NASDAQ",
    "unrealized_intraday_pl": "0.0",
    "unrealized_intraday_plpc": "0.0",
    "lastday_price": "100.0",
    "market_value": "1000.0",
    "unrealized_pl": "0.0",
    "unrealized_plpc": "0.0",
    "qty": "10.0",
    "qty_available": "10.0",
    "side": "long",
    "symbol": "AAPL",
    "asset_marginable": True,
}


# Sta


def test_get_position_by_dict():
    position = Position("url", {"header": "headervalue"}, "account")
    result = position.get(symbol_dict=sample_response)
    assert isinstance(result, PositionClass)
    assert result.symbol == "AAPL"


def test_get_position_no_identifier():
    position = Position("url", {"header": "headervalue"}, "account")
    with pytest.raises(ValueError):
        position.get()


def test_get_position_both_identifiers():
    position = Position("url", {"header": "headervalue"}, "account")
    with pytest.raises(ValueError):
        position.get(symbol="AAPL", symbol_dict=sample_response)


def test_get_position_fail_to_fetch():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        position = Position("url", {"header": "headervalue"}, "account")
        with pytest.raises(ValueError):
            position.get("AAPL")
