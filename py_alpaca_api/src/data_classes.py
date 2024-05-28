from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

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
    legs: List[object]
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
    assets: List[object]


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


KEY_PROCESSORS = {
    int: get_dict_int_value,
    str: get_dict_str_value,
    float: get_dict_float_value,
    datetime: parse_date,
    bool: lambda data_dict, key: bool(data_dict[key]),
    List[object]: lambda data_dict, key: (data_dict[key] if data_dict.get(key) else []),
}


############################################
# Data Class Extraction Functions
############################################
def extract_class_data(data_dict: dict, field_processors: Dict, data_class: dataclass):
    """
    Extracts and processes data from a dictionary based on a given data class and field processors.

    Args:
        data_dict (dict): The dictionary containing the data to be processed.
        field_processors (Dict): A dictionary of field processors.
        data_class (dataclass): The data class used to define the fields and types.

    Returns:
        dict: A dictionary containing processed data, with keys corresponding to the fields of the data class.

    Raises:
        KeyError: When a field processor is not found for a specific data type.
    """
    if "class" in data_dict:
        data_dict["asset_class"] = data_dict["class"]
        del data_dict["class"]
    return {
        field: field_processors[data_type](data_dict, field)
        for field, data_type in data_class.__annotations__.items()
        if field_processors.get(data_type, None)
    }


############################################
# Data Class Watchlist Conversion Functions
############################################
def process_assets(assets: List[Dict]) -> List[AssetClass]:
    """Process a list of assets.

    This function takes a list of asset dictionaries and returns a list of AssetClass objects.
    Each asset dictionary should contain the necessary information to create an AssetClass object.

    Args:
        assets (List[Dict]): A list of asset dictionaries.

    Returns:
        List[AssetClass]: A list of AssetClass objects.
    """
    if not assets:
        return []
    return [AssetClass(**extract_class_data(asset, KEY_PROCESSORS, AssetClass)) for asset in assets] if assets else []


def watchlist_class_from_dict(data_dict: dict) -> WatchlistClass:
    """
    Args:
        data_dict: A dictionary containing the data needed to create a WatchlistClass object.

    Returns:
        A new instance of the WatchlistClass created from the data in the input dictionary.
    """
    watchlist_data = extract_class_data(data_dict, KEY_PROCESSORS, WatchlistClass)
    watchlist_data["assets"] = process_assets(data_dict.get("assets", []))
    return WatchlistClass(**watchlist_data)


############################################
# Data Class Clock Conversion Functions
############################################
def clock_class_from_dict(data_dict: dict) -> ClockClass:
    """
    Args:
        data_dict: A dictionary containing data for creating an instance of `ClockClass`.

    Returns:
        An instance of `ClockClass` created using the data from `data_dict`.

    Raises:
        None.
    """
    clock_data = extract_class_data(data_dict, KEY_PROCESSORS, ClockClass)
    return ClockClass(**clock_data)


############################################
# Data Class Position Conversion Functions
############################################
def position_class_from_dict(data_dict: dict) -> PositionClass:
    """
    Returns a PositionClass object created from a given data dictionary.

    Args:
        data_dict: A dictionary containing the data for creating a PositionClass object.

    Returns:
        PositionClass: A PositionClass object created using the data from the dictionary.
    """
    position_data = extract_class_data(data_dict, KEY_PROCESSORS, PositionClass)
    return PositionClass(**position_data)


############################################
# Data Class Account Conversion Functions
############################################
def account_class_from_dict(data_dict: dict) -> AccountClass:
    """
    Converts a dictionary into an instance of the `AccountClass`.

    Args:
        data_dict (dict): A dictionary containing the data for the `AccountClass` instance.

    Returns:
        AccountClass: An instance of the `AccountClass` created from the provided dictionary.
    """
    account_data = extract_class_data(data_dict, KEY_PROCESSORS, AccountClass)
    return AccountClass(**account_data)


############################################
# Data Class Asset Conversion Functions
############################################
def asset_class_from_dict(data_dict: dict) -> AssetClass:
    """
    Args:
        data_dict: A dictionary containing the data for creating an instance of AssetClass.

    Returns:
        An instance of the AssetClass class.

    Raises:
        None
    """
    asset_data = extract_class_data(data_dict, KEY_PROCESSORS, AssetClass)
    return AssetClass(**asset_data)


############################################
# Data Class Order Conversion Functions
############################################
def process_legs(legs: List[Dict]) -> List[OrderClass]:
    """
    Process the legs and create a list of OrderClass objects based on the provided data.

    Args:
        legs (List[Dict]): A list of dictionaries representing the legs.

    Returns:
        List[OrderClass]: A list of OrderClass objects generated from the leg data.

    Note:
        If the legs parameter is empty, an empty list will be returned.
    """
    if not legs:
        return []
    return [OrderClass(**extract_class_data(leg, KEY_PROCESSORS, OrderClass)) for leg in legs] if legs else []


def order_class_from_dict(data_dict: Dict) -> OrderClass:
    """
    Creates an instance of `OrderClass` using the provided dictionary data.

    Args:
        data_dict (Dict): A dictionary containing the data used to create the `OrderClass` instance.

    Returns:
        OrderClass: An instance of `OrderClass` created using the provided data.

    Raises:
        None
    """
    order_data = extract_class_data(data_dict, KEY_PROCESSORS, OrderClass)
    order_data["legs"] = process_legs(data_dict.get("legs", []))
    return OrderClass(**order_data)
