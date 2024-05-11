import pytest
from py_alpaca_api.alpaca import PyAlpacaApi
from py_alpaca_api.src.data_classes import AccountClass, AssetClass, OrderClass

api_key = 'PKVJG5S58PTM6MQEQH9L'
api_secret = 'YmWLk2WnQja1DCOlOGGUdeTRfWUX7k3zB34kobR6'

@pytest.fixture
def alpaca():
    return PyAlpacaApi(api_key=api_key, api_secret=api_secret, api_paper=True)

@pytest.fixture
def alpaca_wrong_keys():
    return PyAlpacaApi(api_key='api_key', api_secret='api_secret', api_paper=True)

#########################################
##### Test cases for PyAlpacaApi ########
#########################################
def test_alpaca_key_exceptions(alpaca):
    with pytest.raises(ValueError):
        alpaca = PyAlpacaApi(api_key='', api_secret=api_secret, api_paper=True)
    with pytest.raises(ValueError):
        alpaca = PyAlpacaApi(api_key=api_key, api_secret='', api_paper=True)

def test_get_account_wrong_keys(alpaca_wrong_keys):
    with pytest.raises(Exception):
        account = alpaca_wrong_keys.get_account()
###########################################
# Test cases for PyAlpacaApi.market_order #
###########################################
def test_qty_market_order(alpaca):
    order = alpaca.market_order(symbol='AAPL', qty=0.01, side='buy')
    assert isinstance(order, OrderClass)
    assert order.status == 'accepted'
    assert order.qty == 0.01

def test_notional_market_order(alpaca):
    order = alpaca.market_order(symbol='AAPL', notional=2.00, side='buy')
    assert isinstance(order, OrderClass)
    assert order.status == 'accepted'
    assert order.notional == 2.00

def test_fake_value_market_order(alpaca):
    with pytest.raises(Exception):
        alpaca.market_order(symbol='FAKESYM', notional=2.00, side='buy')

def test_no_money_value_market_order(alpaca):
    with pytest.raises(Exception):
        alpaca.market_order(symbol='AAPL', qty=200.00, side='buy')
###########################################
# Test cases for PyAlpacaApi.limit_order #
###########################################
def test_cancel_all_orders(alpaca):
    account = alpaca.cancel_all_orders()
    assert 'orders have been cancelled' in account
########################################
# Test cases for PyAlpacaApi.get_asset #
########################################
def test_get_asset_invalid_symbol(alpaca):
    with pytest.raises(ValueError):
        asset = alpaca.get_asset('INVALID')

def test_get_asset(alpaca):
    assert isinstance(alpaca.get_asset('AAPL'), AssetClass)
    assert alpaca.get_asset('AAPL').symbol == 'AAPL'

def test_get_asset_attributes(alpaca):
    asset = alpaca.get_asset('AAPL')
    assert hasattr(asset, 'id')
    assert hasattr(asset, 'asset_class')
    assert hasattr(asset, 'easy_to_borrow')
    assert hasattr(asset, 'exchange')
    assert hasattr(asset, 'fractionable')
    assert hasattr(asset, 'maintenance_margin_requirement')
    assert hasattr(asset, 'marginable')
    assert hasattr(asset, 'name')
    assert hasattr(asset, 'shortable')
    assert hasattr(asset, 'status')
    assert hasattr(asset, 'symbol')
    assert hasattr(asset, 'tradable')
##########################################
# Test cases for PyAlpacaApi.get_account #
##########################################
def test_get_account(alpaca):
    account = alpaca.get_account()
    assert isinstance(account, AccountClass)
    assert account.id != ''
    assert account.account_number != ''
    assert account.status != ''
    assert account.currency != ''

def test_get_account_attributes(alpaca):
    account = alpaca.get_account()
    assert hasattr(account, 'id')
    assert hasattr(account, 'admin_configurations')
    assert hasattr(account, 'user_configurations')
    assert hasattr(account, 'account_number')
    assert hasattr(account, 'status')
    assert hasattr(account, 'crypto_status')
    assert hasattr(account, 'options_approved_level')
    assert hasattr(account, 'options_trading_level')
    assert hasattr(account, 'currency')
    assert hasattr(account, 'buying_power')
    assert hasattr(account, 'regt_buying_power')
    assert hasattr(account, 'daytrading_buying_power')
    assert hasattr(account, 'effective_buying_power')
    assert hasattr(account, 'non_marginable_buying_power')
    assert hasattr(account, 'options_buying_power')
    assert hasattr(account, 'bod_dtbp')
    assert hasattr(account, 'cash')
    assert hasattr(account, 'accrued_fees')
    assert hasattr(account, 'pending_transfer_in')
    assert hasattr(account, 'portfolio_value')
    assert hasattr(account, 'pattern_day_trader')
    assert hasattr(account, 'trading_blocked')
    assert hasattr(account, 'transfers_blocked')
    assert hasattr(account, 'account_blocked')
    assert hasattr(account, 'created_at')
    assert hasattr(account, 'trade_suspended_by_user')
    assert hasattr(account, 'multiplier')
    assert hasattr(account, 'shorting_enabled')
    assert hasattr(account, 'equity')
    assert hasattr(account, 'last_equity')
    assert hasattr(account, 'long_market_value')
    assert hasattr(account, 'short_market_value')
    assert hasattr(account, 'position_market_value')
    assert hasattr(account, 'initial_margin')
    assert hasattr(account, 'maintenance_margin')
    assert hasattr(account, 'last_maintenance_margin')
    assert hasattr(account, 'sma')
    assert hasattr(account, 'daytrade_count')
    assert hasattr(account, 'balance_asof')
    assert hasattr(account, 'crypto_tier')
    assert hasattr(account, 'intraday_adjustments')
    assert hasattr(account, 'pending_reg_taf_fees')



