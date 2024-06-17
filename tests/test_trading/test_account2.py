import os
from datetime import datetime

import pandas as pd
import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.models.account_model import AccountModel

api_key = os.environ.get("ALPACA_API_KEY")
api_secret = os.environ.get("ALPACA_SECRET_KEY")


@pytest.fixture
def alpaca():
    return PyAlpacaAPI(api_key=api_key, api_secret=api_secret, api_paper=True)


@pytest.fixture
def alpaca_wrong_keys():
    return PyAlpacaAPI(api_key="api_key", api_secret="api_secret", api_paper=True)


##########################################
# Test cases for PyAlpacaAPI.get_account #
##########################################
def test_get_account_wrong_keys(alpaca_wrong_keys):
    with pytest.raises(Exception):
        alpaca_wrong_keys.trading.account.get()


def test_get_account(alpaca):
    account = alpaca.trading.account.get()
    assert isinstance(account, AccountModel)
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
    assert isinstance(account.created_at, str)
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
    account = alpaca.trading.account.get()
    assert hasattr(account, "id")
    assert hasattr(account, "account_number")
    assert hasattr(account, "status")


def test_get_portfolio_history(alpaca):
    history = alpaca.trading.account.portfolio_history()
    assert isinstance(history, pd.DataFrame)
    assert history.timestamp.dtype == datetime
    assert history.equity.dtype == float
    assert history.profit_loss.dtype == float
    assert history.profit_loss_pct.dtype == float
    assert history.base_value.dtype == float


def test_portfolio_history(alpaca):
    history = alpaca.trading.account.portfolio_history()
    assert isinstance(history, pd.DataFrame)
    assert history.timestamp.dtype == pd.Timestamp
    assert history.equity.dtype == float
    assert history.profit_loss.dtype == float
    assert history.profit_loss_pct.dtype == float
    assert history.base_value.dtype == float
    assert len(history) > 0


def test_portfolio_history_custom_params(alpaca):
    history = alpaca.trading.account.portfolio_history(
        period="2W", timeframe="1H", intraday_reporting="extended_hours"
    )
    assert isinstance(history, pd.DataFrame)
    assert history.timestamp.dtype == pd.Timestamp
    assert history.equity.dtype == float
    assert history.profit_loss.dtype == float
    assert history.profit_loss_pct.dtype == float
    assert history.base_value.dtype == float
    assert len(history) > 0
