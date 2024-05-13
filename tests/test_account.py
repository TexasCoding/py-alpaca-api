import os
from datetime import datetime

import pytest

from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import AccountClass

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")


@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)


@pytest.fixture
def alpaca_wrong_keys():
    return PyAlpacaApi(api_key="api_key", api_secret="api_secret", api_paper=True)


##########################################
# Test cases for PyAlpacaApi.get_account #
##########################################
def test_get_account_wrong_keys(alpaca_wrong_keys):
    with pytest.raises(Exception):
        alpaca_wrong_keys.get_account()


def test_get_account(alpaca):
    account = alpaca.get_account()
    assert isinstance(account, AccountClass)
    assert isinstance(account.id, str)
    assert isinstance(account.account_number, str)
    assert isinstance(account.status, str)
    assert isinstance(account.crypto_status, str)
    assert isinstance(account.options_approved_level, int)
    assert isinstance(account.options_trading_level, int)
    assert isinstance(account.currency, str)
    assert isinstance(account.buying_power, float)
    assert isinstance(account.regt_buying_power, float)
    assert isinstance(account.daytrading_buying_power, float)
    assert isinstance(account.effective_buying_power, float)
    assert isinstance(account.non_marginable_buying_power, float)
    assert isinstance(account.options_buying_power, float)
    assert isinstance(account.bod_dtbp, float)
    assert isinstance(account.cash, float)
    assert isinstance(account.accrued_fees, float)
    assert isinstance(account.pending_transfer_in, float)
    assert isinstance(account.portfolio_value, float)
    assert isinstance(account.pattern_day_trader, bool)
    assert isinstance(account.trading_blocked, bool)
    assert isinstance(account.transfers_blocked, bool)
    assert isinstance(account.account_blocked, bool)
    assert isinstance(account.created_at, datetime)
    assert isinstance(account.trade_suspended_by_user, bool)
    assert isinstance(account.multiplier, int)
    assert isinstance(account.shorting_enabled, bool)
    assert isinstance(account.equity, float)
    assert isinstance(account.last_equity, float)
    assert isinstance(account.long_market_value, float)
    assert isinstance(account.short_market_value, float)
    assert isinstance(account.position_market_value, float)
    assert isinstance(account.initial_margin, float)
    assert isinstance(account.maintenance_margin, float)
    assert isinstance(account.last_maintenance_margin, float)
    assert isinstance(account.sma, float)
    assert isinstance(account.daytrade_count, int)
    assert isinstance(account.balance_asof, str)
    assert isinstance(account.crypto_tier, int)
    assert isinstance(account.intraday_adjustments, int)
    assert isinstance(account.pending_reg_taf_fees, float)


def test_get_account_attributes(alpaca):
    account = alpaca.get_account()
    assert hasattr(account, "id")
    assert hasattr(account, "account_number")
    assert hasattr(account, "status")
