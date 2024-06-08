import json
from unittest.mock import Mock, patch
import pytest
from py_alpaca_api.trading.account import Account
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.account_model import AccountModel


@pytest.fixture
def account_obj():
    return Account(
        headers={"APCA-API-KEY-ID": "Bearer token", "APCA-API-SECRET-KEY": "secret"},
        base_url="https://example.com",
    )


def test_get_account(account_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = json.dumps(
        {
            "id": "12345678",
            "pattern_day_trader": False,
            "trading_blocked": False,
            "account_blocked": False,
            "transfers_blocked": False,
            "trade_suspended_by_user": False,
            "shorting_enabled": True,
        }
    )
    with patch.object(Requests, "request", return_value=mock_response):
        account = account_obj.get()
        assert isinstance(account, AccountModel)
        assert account.id == "12345678"


def test_get_account_error(account_obj):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Error"
    with patch.object(Requests, "request", return_value=mock_response):
        with pytest.raises(Exception):
            account_obj.get()


def test_get_account_invalid_response(account_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Invalid response"
    with patch.object(Requests, "request", return_value=mock_response):
        with pytest.raises(ValueError):
            account_obj.get()
