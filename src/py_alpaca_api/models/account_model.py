from dataclasses import dataclass
from datetime import datetime

from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class AccountModel:
    id: str
    account_number: str
    status: str
    crypto_status: str
    options_approved_level: int
    options_trading_level: int
    currency: str
    buying_power: float
    regt_buying_power: float
    daytrading_buying_power: float
    effective_buying_power: float
    non_marginable_buying_power: float
    options_buying_power: float
    bod_dtbp: float
    cash: float
    accrued_fees: float
    pending_transfer_in: float
    portfolio_value: float
    pattern_day_trader: bool
    trading_blocked: bool
    transfers_blocked: bool
    account_blocked: bool
    created_at: datetime
    trade_suspended_by_user: bool
    multiplier: int
    shorting_enabled: bool
    equity: float
    last_equity: float
    long_market_value: float
    short_market_value: float
    position_market_value: float
    initial_margin: float
    maintenance_margin: float
    last_maintenance_margin: float
    sma: float
    daytrade_count: int
    balance_asof: str
    crypto_tier: int
    intraday_adjustments: int
    pending_reg_taf_fees: float


############################################
# Data Class Account Conversion Functions
############################################
def account_class_from_dict(data_dict: dict) -> AccountModel:
    """
    Converts a dictionary into an instance of the `AccountModel`.

    Args:
        data_dict (dict): A dictionary containing the data for the `AccountModel` instance.

    Returns:
        AccountModel: An instance of the `AccountModel` created from the provided dictionary.
    """
    account_data = extract_class_data(data_dict, KEY_PROCESSORS, AccountModel)
    return AccountModel(**account_data)
