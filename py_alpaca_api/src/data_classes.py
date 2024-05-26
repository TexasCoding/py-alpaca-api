from dataclasses import dataclass
from datetime import datetime

import pendulum


############################################
# Data Class for Clock
############################################
@dataclass
class ClockClass:
    market_time: datetime
    is_open: bool
    next_open: datetime
    next_close: datetime


############################################
# Data Class for Position
############################################
@dataclass
class PositionClass:
    asset_id: str
    symbol: str
    exchange: str
    asset_class: str
    avg_entry_price: float
    qty: float
    qty_available: float
    side: str
    market_value: float
    cost_basis: float
    profit_dol: float
    profit_pct: float
    intraday_profit_dol: float
    intraday_profit_pct: float
    portfolio_pct: float
    current_price: float
    lastday_price: float
    change_today: float
    asset_marginable: bool


############################################
# Data Class for Order
############################################
@dataclass
class OrderClass:
    id: str
    client_order_id: str
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime
    filled_at: datetime
    expired_at: datetime
    canceled_at: datetime
    failed_at: datetime
    replaced_at: datetime
    replaced_by: str
    replaces: str
    asset_id: str
    symbol: str
    asset_class: str
    notional: float
    qty: float
    filled_qty: float
    filled_avg_price: float
    order_class: str
    order_type: str
    type: str
    side: str
    time_in_force: str
    limit_price: float
    stop_price: float
    status: str
    extended_hours: bool
    legs: object
    trail_percent: float
    trail_price: float
    hwm: float
    subtag: str
    source: str


############################################
# Data Class for Asset
############################################
@dataclass
class AssetClass:
    id: str
    asset_class: str
    easy_to_borrow: bool
    exchange: str
    fractionable: bool
    maintenance_margin_requirement: float
    marginable: bool
    name: str
    shortable: bool
    status: str
    symbol: str
    tradable: bool


############################################
# Data Class for Account
############################################
@dataclass
class AccountClass:
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
# Data Class for Watchlist
############################################
@dataclass
class WatchlistClass:
    id: str
    account_id: str
    created_at: datetime
    updated_at: datetime
    name: str
    assets: object


def get_dict_str_value(data_dict: dict, key: str) -> str:
    """
    Returns the string value of a specific key within a dictionary.

    Args:
        data_dict (dict): The dictionary containing the data.
        key (str): The key to retrieve the value from.

    Returns:
        str: The string value associated with the specified key. If the key does not exist in the dictionary or
        its value is None, an empty string will be returned.
    """
    return str(data_dict[key]) if data_dict.get(key) else ""


def parse_date(data_dict: dict, key: str) -> datetime:
    """
    Parses a date value from a dictionary using a specified key.

    Args:
        data_dict (dict): The dictionary from which to extract the date value.
        key (str): The key in the dictionary representing the date value.

    Returns:
        datetime: The parsed date value as a `datetime` object.

    """
    return pendulum.parse(data_dict[key], tz="America/New_York") if data_dict.get(key) else pendulum.DateTime.min


def get_dict_float_value(data_dict: dict, key: str) -> float:
    """
    Args:
        data_dict (dict): A dictionary containing the data.
        key (str): The key to look for in the data_dict.

    Returns:
        float: The value associated with the specified key in the data_dict as a float. If the key is not found or
        if the value is not of float type, returns 0.0.
    """
    return float(data_dict.get(key, 0.0)) if data_dict.get(key) else 0.0


def get_dict_int_value(data_dict: dict, key: str) -> int:
    """
    Args:
        data_dict: A dictionary containing key-value pairs.
        key: The key whose corresponding value is to be returned.

    Returns:
        int: The integer value associated with the given key in the data_dict. If the key is not present or
        the corresponding value is not an integer, 0 is returned.
    """
    return int(data_dict.get(key, 0)) if data_dict.get(key) else 0


def watchlist_class_from_dict(data_dict: dict) -> WatchlistClass:
    """
    Constructs a WatchlistClass object from a given dictionary.

    Args:
        data_dict (dict): A dictionary containing the data to construct the WatchlistClass.

    Returns:
        WatchlistClass: The constructed WatchlistClass object.

    """
    return WatchlistClass(
        id=get_dict_str_value(data_dict, "id"),
        account_id=get_dict_str_value(data_dict, "account_id"),
        created_at=parse_date(data_dict, "created_at"),
        updated_at=parse_date(data_dict, "updated_at"),
        name=get_dict_str_value(data_dict, "name"),
        assets=list(map(asset_class_from_dict, data_dict["assets"])) if data_dict.get("assets") else None,
    )


############################################
# Data Class Clock Conversion Functions
############################################
def clock_class_from_dict(data_dict: dict) -> ClockClass:
    """
    Args:
        data_dict (dict): A dictionary containing the relevant data for creating a ClockClass object.

    Returns:
        ClockClass: An instance of the ClockClass class.

    """
    return ClockClass(
        market_time=parse_date(data_dict, "timestamp"),
        is_open=bool(data_dict["is_open"]),
        next_open=parse_date(data_dict, "next_open"),
        next_close=parse_date(data_dict, "next_close"),
    )


############################################
# Data Class Position Conversion Functions
############################################
def position_class_from_dict(data_dict: dict) -> PositionClass:
    """
    Args:
        data_dict: A dictionary containing the data for creating a PositionClass object.

    Returns:
        A PositionClass object created using the data from the provided dictionary.

    """
    return PositionClass(
        asset_id=get_dict_str_value(data_dict, "asset_id"),
        symbol=get_dict_str_value(data_dict, "symbol"),
        exchange=get_dict_str_value(data_dict, "exchange"),
        asset_class=get_dict_str_value(data_dict, "asset_class"),
        avg_entry_price=get_dict_float_value(data_dict, "avg_entry_price"),
        qty=get_dict_float_value(data_dict, "qty"),
        qty_available=get_dict_float_value(data_dict, "qty_available"),
        side=get_dict_str_value(data_dict, "side"),
        market_value=get_dict_float_value(data_dict, "market_value"),
        cost_basis=get_dict_float_value(data_dict, "cost_basis"),
        profit_dol=get_dict_float_value(data_dict, "profit_dol"),
        profit_pct=get_dict_float_value(data_dict, "profit_pct"),
        intraday_profit_dol=get_dict_float_value(data_dict, "intraday_profit_dol"),
        intraday_profit_pct=get_dict_float_value(data_dict, "intraday_profit_pct"),
        portfolio_pct=get_dict_float_value(data_dict, "portfolio_pct"),
        current_price=get_dict_float_value(data_dict, "current_price"),
        lastday_price=get_dict_float_value(data_dict, "lastday_price"),
        change_today=get_dict_float_value(data_dict, "change_today"),
        asset_marginable=bool(data_dict["asset_marginable"]),
    )


############################################
# Data Class Account Conversion Functions
############################################
def account_class_from_dict(data_dict: dict) -> AccountClass:
    """
    This function converts a dictionary into an instance of the AccountClass.

    Args:
        data_dict (dict): A dictionary containing the account data.

    Returns:
        AccountClass: An instance of the AccountClass with the attributes populated with the values from the dictionary.

    Note:
        The function uses various helper functions (`get_dict_str_value`, `get_dict_int_value`, `get_dict_float_value`,
        and `parse_date`) to extract the values from the dictionary and convert them to the appropriate types.
    """
    return AccountClass(
        id=get_dict_str_value(data_dict, "id"),
        account_number=get_dict_str_value(data_dict, "account_number"),
        status=get_dict_str_value(data_dict, "status"),
        crypto_status=get_dict_str_value(data_dict, "crypto_status"),
        options_approved_level=get_dict_int_value(data_dict, "options_approved_level"),
        options_trading_level=get_dict_int_value(data_dict, "options_trading_level"),
        currency=get_dict_str_value(data_dict, "currency"),
        buying_power=get_dict_float_value(data_dict, "buying_power"),
        regt_buying_power=get_dict_float_value(data_dict, "regt_buying_power"),
        daytrading_buying_power=get_dict_float_value(data_dict, "daytrading_buying_power"),
        effective_buying_power=get_dict_float_value(data_dict, "effective_buying_power"),
        non_marginable_buying_power=get_dict_float_value(data_dict, "non_marginable_buying_power"),
        options_buying_power=get_dict_float_value(data_dict, "options_buying_power"),
        bod_dtbp=get_dict_float_value(data_dict, "bod_dtbp"),
        cash=get_dict_float_value(data_dict, "cash"),
        accrued_fees=get_dict_float_value(data_dict, "accrued_fees"),
        pending_transfer_in=get_dict_float_value(data_dict, "pending_transfer_in"),
        portfolio_value=get_dict_float_value(data_dict, "portfolio_value"),
        pattern_day_trader=bool(data_dict["pattern_day_trader"]),
        trading_blocked=bool(data_dict["trading_blocked"]),
        transfers_blocked=bool(data_dict["transfers_blocked"]),
        account_blocked=bool(data_dict["account_blocked"]),
        created_at=parse_date(data_dict, "created_at"),
        trade_suspended_by_user=bool(data_dict["trade_suspended_by_user"]),
        multiplier=get_dict_int_value(data_dict, "multiplier"),
        shorting_enabled=bool(data_dict["shorting_enabled"]),
        equity=get_dict_float_value(data_dict, "equity"),
        last_equity=get_dict_float_value(data_dict, "last_equity"),
        long_market_value=get_dict_float_value(data_dict, "long_market_value"),
        short_market_value=get_dict_float_value(data_dict, "short_market_value"),
        position_market_value=get_dict_float_value(data_dict, "position_market_value"),
        initial_margin=get_dict_float_value(data_dict, "initial_margin"),
        maintenance_margin=get_dict_float_value(data_dict, "maintenance_margin"),
        last_maintenance_margin=get_dict_float_value(data_dict, "last_maintenance_margin"),
        sma=get_dict_float_value(data_dict, "sma"),
        daytrade_count=get_dict_int_value(data_dict, "daytrade_count"),
        balance_asof=get_dict_str_value(data_dict, "balance_asof"),
        crypto_tier=get_dict_int_value(data_dict, "crypto_tier"),
        intraday_adjustments=get_dict_int_value(data_dict, "intraday_adjustments"),
        pending_reg_taf_fees=get_dict_float_value(data_dict, "pending_reg_taf_fees"),
    )


############################################
# Data Class Asset Conversion Functions
############################################
def asset_class_from_dict(data_dict: dict) -> AssetClass:
    """
    Args:
        data_dict: A dictionary containing the data for an asset class.

    Returns:
        An AssetClass object initialized with the values from the data_dict.

    """
    return AssetClass(
        id=get_dict_str_value(data_dict, "id"),
        asset_class=get_dict_str_value(data_dict, "class"),
        easy_to_borrow=bool(data_dict["easy_to_borrow"]),
        exchange=get_dict_str_value(data_dict, "exchange"),
        fractionable=bool(data_dict["fractionable"]),
        maintenance_margin_requirement=get_dict_float_value(data_dict, "maintenance_margin_requirement"),
        marginable=bool(data_dict["marginable"]),
        name=get_dict_str_value(data_dict, "name"),
        shortable=bool(data_dict["shortable"]),
        status=get_dict_str_value(data_dict, "status"),
        symbol=get_dict_str_value(data_dict, "symbol"),
        tradable=bool(data_dict["tradable"]),
    )


############################################
# Data Class Order Conversion Functions
############################################
def order_class_from_dict(data_dict: dict) -> OrderClass:
    """
    Args:
        data_dict: A dictionary containing data for creating an OrderClass object.

    Returns:
        An instance of the OrderClass class.

    Raises:
        KeyError: If any of the required keys are missing in the data_dict.

    """
    return OrderClass(
        id=get_dict_str_value(data_dict, "id"),
        client_order_id=get_dict_str_value(data_dict, "client_order_id"),
        created_at=parse_date(data_dict, "created_at"),
        updated_at=parse_date(data_dict, "updated_at"),
        submitted_at=parse_date(data_dict, "submitted_at"),
        filled_at=parse_date(data_dict, "filled_at"),
        expired_at=parse_date(data_dict, "expired_at"),
        canceled_at=parse_date(data_dict, "canceled_at"),
        failed_at=parse_date(data_dict, "failed_at"),
        replaced_at=parse_date(data_dict, "replaced_at"),
        replaced_by=get_dict_str_value(data_dict, "replaced_by"),
        replaces=get_dict_str_value(data_dict, "replaces"),
        asset_id=get_dict_str_value(data_dict, "asset_id"),
        symbol=get_dict_str_value(data_dict, "symbol"),
        asset_class=get_dict_str_value(data_dict, "asset_class"),
        notional=get_dict_float_value(data_dict, "notional"),
        qty=get_dict_float_value(data_dict, "qty"),
        filled_qty=get_dict_float_value(data_dict, "filled_qty"),
        filled_avg_price=get_dict_float_value(data_dict, "filled_avg_price"),
        order_class=get_dict_str_value(data_dict, "order_class"),
        order_type=get_dict_str_value(data_dict, "order_type"),
        type=get_dict_str_value(data_dict, "type"),
        side=get_dict_str_value(data_dict, "side"),
        time_in_force=get_dict_str_value(data_dict, "time_in_force"),
        limit_price=get_dict_float_value(data_dict, "limit_price"),
        stop_price=get_dict_float_value(data_dict, "stop_price"),
        status=get_dict_str_value(data_dict, "status"),
        extended_hours=bool(data_dict["extended_hours"]),
        legs=data_dict["legs"] if data_dict["legs"] else {},
        trail_percent=get_dict_float_value(data_dict, "trail_percent"),
        trail_price=get_dict_float_value(data_dict, "trail_price"),
        hwm=get_dict_float_value(data_dict, "hwm"),
        subtag=get_dict_str_value(data_dict, "subtag"),
        source=get_dict_str_value(data_dict, "source"),
    )
