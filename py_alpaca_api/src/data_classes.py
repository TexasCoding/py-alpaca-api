from dataclasses import dataclass
from datetime import datetime


@dataclass
############################################
# Data Class for Clock
############################################
class ClockClass:
    """Clock class data structure.

    Attributes:
    ----------

    timestamp: datetime
    is_open: bool
    next_open: datetime
    next_close: datetime
    """  # noqa

    market_time: datetime
    is_open: bool
    next_open: datetime
    next_close: datetime


@dataclass
############################################
# Data Class for Position
############################################
class PositionClass:
    """Position class data structure.

    Attributes:
    ------------

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
    """  # noqa

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


@dataclass
############################################
# Data Class for Order
############################################
class OrderClass:
    """Order class data structure.

    Attributes:
    ----------

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
    """  # noqa

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


@dataclass
############################################
# Data Class for Asset
############################################
class AssetClass:
    """Asset class data structure.

    Attributes:
    ----------

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
    """  # noqa

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


@dataclass
############################################
# Data Class for Account
############################################
class AccountClass:
    """Account class data structure.

    Attributes:
    ----------

    id: str
    admin_configurations: object
    user_configurations: object
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
    """  # noqa

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


@dataclass
class WatchlistClass:
    id: str
    account_id: str
    created_at: datetime
    updated_at: datetime
    name: str
    assets: object


def watchlist_class_from_dict(data_dict: dict) -> WatchlistClass:
    return WatchlistClass(
        id=str(data_dict["id"] if data_dict["id"] else ""),
        account_id=str(data_dict["account_id"] if data_dict["account_id"] else ""),
        created_at=(
            datetime.strptime(
                data_dict["created_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["created_at"]
            else datetime.date(0, 0, 0)
        ),
        updated_at=(
            datetime.strptime(
                data_dict["updated_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["updated_at"]
            else datetime.date(0, 0, 0)
        ),
        name=str(data_dict["name"] if data_dict["name"] else ""),
        assets=([asset_class_from_dict(sym) for sym in data_dict["assets"] if len(data_dict["assets"]) > 0] if data_dict["assets"] else None),
    )


############################################
# Data Class Clock Conversion Functions
############################################
def clock_class_from_dict(data_dict: dict) -> ClockClass:
    """Converts a dictionary to a ClockClass object.

    Parameters:
    -----------
    data_dict: dict
        A dictionary containing the clock data.

    Returns:
    --------
    ClockClass
        A ClockClass object.
    """  # noqa
    return ClockClass(
        market_time=(
            datetime.strptime(
                data_dict["timestamp"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["timestamp"]
            else datetime.date(0, 0, 0)
        ),
        is_open=bool(data_dict["is_open"]),
        next_open=(
            datetime.strptime(
                data_dict["next_open"].replace("T", " ").replace("-04:00", ""),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["next_open"]
            else datetime.date(0, 0, 0)
        ),
        next_close=(
            datetime.strptime(
                data_dict["next_close"].replace("-04:00", "").replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["next_close"]
            else datetime.date(0, 0, 0)
        ),
    )


############################################
# Data Class Position Conversion Functions
############################################
def position_class_from_dict(data_dict: dict) -> PositionClass:
    """Converts a dictionary to a PositionClass object.

    Parameters:
    -----------
    data_dict: dict
        A dictionary containing the position data.

    Returns:
    --------
    PositionClass
        A PositionClass object.
    """  # noqa

    return PositionClass(
        asset_id=str(data_dict["asset_id"] if data_dict["asset_id"] else ""),
        symbol=str(data_dict["symbol"] if data_dict["symbol"] else ""),
        exchange=str(data_dict["exchange"] if data_dict["exchange"] else ""),
        asset_class=str(data_dict["asset_class"] if data_dict["asset_class"] else ""),
        avg_entry_price=float(data_dict["avg_entry_price"] if data_dict["avg_entry_price"] else 0),
        qty=float(data_dict["qty"] if data_dict["qty"] else 0),
        qty_available=float(data_dict["qty_available"] if data_dict["qty_available"] else 0),
        side=str(data_dict["side"] if data_dict["side"] else ""),
        market_value=float(data_dict["market_value"] if data_dict["market_value"] else 0),
        cost_basis=float(data_dict["cost_basis"] if data_dict["cost_basis"] else 0),
        profit_dol=float(data_dict["profit_dol"] if data_dict["profit_dol"] else 0),
        profit_pct=float(data_dict["profit_pct"] if data_dict["profit_pct"] else 0),
        intraday_profit_dol=float(data_dict["intraday_profit_dol"] if data_dict["intraday_profit_dol"] else 0),
        intraday_profit_pct=float(data_dict["intraday_profit_pct"] if data_dict["intraday_profit_pct"] else 0),
        portfolio_pct=float(data_dict["portfolio_pct"] if data_dict["portfolio_pct"] else 0),
        current_price=float(data_dict["current_price"] if data_dict["current_price"] else 0),
        lastday_price=float(data_dict["lastday_price"] if data_dict["lastday_price"] else 0),
        change_today=float(data_dict["change_today"] if data_dict["change_today"] else 0),
        asset_marginable=bool(data_dict["asset_marginable"]),
    )


############################################
# Data Class Account Conversion Functions
############################################
def account_class_from_dict(data_dict: dict) -> AccountClass:
    """Converts a dictionary to an AccountClass object.

    Parameters:
    -----------
    data_dict: dict
        A dictionary containing the account data.

    Returns:
    --------
    AccountClass
        An AccountClass object.
    """  # noqa
    return AccountClass(
        id=str(data_dict["id"] if data_dict["id"] else ""),
        account_number=str(data_dict["account_number"]),
        status=str(data_dict["status"] if data_dict["status"] else ""),
        crypto_status=str(data_dict["crypto_status"] if data_dict["crypto_status"] else ""),
        options_approved_level=int(data_dict["options_approved_level"] if data_dict["options_approved_level"] else 0),
        options_trading_level=int(data_dict["options_trading_level"] if data_dict["options_trading_level"] else 0),
        currency=str(data_dict["currency"] if data_dict["currency"] else ""),
        buying_power=float(data_dict["buying_power"] if data_dict["buying_power"] else 0),
        regt_buying_power=float(data_dict["regt_buying_power"] if data_dict["regt_buying_power"] else 0),
        daytrading_buying_power=float(data_dict["daytrading_buying_power"] if data_dict["daytrading_buying_power"] else 0),
        effective_buying_power=float(data_dict["effective_buying_power"] if data_dict["effective_buying_power"] else 0),
        non_marginable_buying_power=float(data_dict["non_marginable_buying_power"] if data_dict["non_marginable_buying_power"] else 0),
        options_buying_power=float(data_dict["options_buying_power"] if data_dict["options_buying_power"] else 0),
        bod_dtbp=float(data_dict["bod_dtbp"] if data_dict["bod_dtbp"] else 0),
        cash=float(data_dict["cash"] if data_dict["cash"] else 0),
        accrued_fees=float(data_dict["accrued_fees"] if data_dict["accrued_fees"] else 0),
        pending_transfer_in=float(data_dict["pending_transfer_in"] if data_dict["pending_transfer_in"] else 0),
        portfolio_value=float(data_dict["portfolio_value"] if data_dict["portfolio_value"] else 0),
        pattern_day_trader=bool(data_dict["pattern_day_trader"]),
        trading_blocked=bool(data_dict["trading_blocked"]),
        transfers_blocked=bool(data_dict["transfers_blocked"]),
        account_blocked=bool(data_dict["account_blocked"]),
        created_at=(
            datetime.strptime(
                data_dict["created_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["created_at"]
            else datetime.date(0, 0, 0)
        ),
        trade_suspended_by_user=bool(data_dict["trade_suspended_by_user"]),
        multiplier=int(data_dict["multiplier"] if data_dict["multiplier"] else 0),
        shorting_enabled=bool(data_dict["shorting_enabled"]),
        equity=float(data_dict["equity"] if data_dict["equity"] else 0),
        last_equity=float(data_dict["last_equity"] if data_dict["last_equity"] else 0),
        long_market_value=float(data_dict["long_market_value"] if data_dict["long_market_value"] else 0),
        short_market_value=float(data_dict["short_market_value"] if data_dict["short_market_value"] else 0),
        position_market_value=float(data_dict["position_market_value"] if data_dict["position_market_value"] else 0),
        initial_margin=float(data_dict["initial_margin"] if data_dict["initial_margin"] else 0),
        maintenance_margin=float(data_dict["maintenance_margin"] if data_dict["maintenance_margin"] else 0),
        last_maintenance_margin=float(data_dict["last_maintenance_margin"] if data_dict["last_maintenance_margin"] else 0),
        sma=float(data_dict["sma"] if data_dict["sma"] else 0),
        daytrade_count=int(data_dict["daytrade_count"] if data_dict["daytrade_count"] else 0),
        balance_asof=str(data_dict["balance_asof"] if data_dict["balance_asof"] else ""),
        crypto_tier=int(data_dict["crypto_tier"] if data_dict["crypto_tier"] else 0),
        intraday_adjustments=int(data_dict["intraday_adjustments"] if data_dict["intraday_adjustments"] else 0),
        pending_reg_taf_fees=float(data_dict["pending_reg_taf_fees"] if data_dict["pending_reg_taf_fees"] else 0),
    )


############################################
# Data Class Asset Conversion Functions
############################################
def asset_class_from_dict(data_dict: dict) -> AssetClass:
    """Converts a dictionary to an AssetClass object.

    Parameters:
    -----------
    data_dict: dict
        A dictionary containing the asset data.

    Returns:
    --------
    AssetClass
        An AssetClass object.
    """  # noqa
    return AssetClass(
        id=str(data_dict["id"]) if data_dict["id"] else "",
        asset_class=str(data_dict["class"]) if data_dict["class"] else "",
        easy_to_borrow=bool(data_dict["easy_to_borrow"]),
        exchange=str(data_dict["exchange"]) if data_dict["exchange"] else "",
        fractionable=bool(data_dict["fractionable"]),
        maintenance_margin_requirement=(float(data_dict["maintenance_margin_requirement"]) if data_dict["maintenance_margin_requirement"] else 0),
        marginable=bool(data_dict["marginable"]),
        name=str(data_dict["name"]) if data_dict["name"] else "",
        shortable=bool(data_dict["shortable"]),
        status=str(data_dict["status"]) if data_dict["status"] else "",
        symbol=str(data_dict["symbol"]) if data_dict["symbol"] else "",
        tradable=bool(data_dict["tradable"]),
    )


############################################
# Data Class Order Conversion Functions
############################################
def order_class_from_dict(data_dict: dict) -> OrderClass:
    """Converts a dictionary to an OrderClass object.

    Parameters:
    -----------
    data_dict: dict
        A dictionary containing the order data.

    Returns:
    --------
    OrderClass
        An OrderClass object.
    """  # noqa
    return OrderClass(
        id=str(data_dict["id"] if data_dict["id"] else ""),
        client_order_id=str(data_dict["client_order_id"]),
        created_at=(
            datetime.strptime(
                data_dict["created_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["created_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        updated_at=(
            datetime.strptime(
                data_dict["updated_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["updated_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        submitted_at=(
            datetime.strptime(
                data_dict["submitted_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["submitted_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        filled_at=(
            datetime.strptime(
                data_dict["filled_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["filled_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        expired_at=(
            datetime.strptime(
                data_dict["expired_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["expired_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        canceled_at=(
            datetime.strptime(
                data_dict["canceled_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["canceled_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        failed_at=(
            datetime.strptime(
                data_dict["failed_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["failed_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        replaced_at=(
            datetime.strptime(
                data_dict["replaced_at"].split(".")[0].replace("T", " "),
                "%Y-%m-%d %H:%M:%S",
            )
            if data_dict["replaced_at"]
            else datetime(1, 1, 1, 0, 0)
        ),
        replaced_by=str(data_dict["replaced_by"] if data_dict["replaced_by"] else ""),
        replaces=str(data_dict["replaces"] if data_dict["replaces"] else ""),
        asset_id=str(data_dict["asset_id"] if data_dict["asset_id"] else ""),
        symbol=str(data_dict["symbol"] if data_dict["symbol"] else ""),
        asset_class=str(data_dict["asset_class"] if data_dict["asset_class"] else ""),
        notional=float(data_dict["notional"] if data_dict["notional"] else 0),
        qty=float(data_dict["qty"] if data_dict["qty"] else 0),
        filled_qty=float(data_dict["filled_qty"] if data_dict["filled_qty"] else 0),
        filled_avg_price=float(data_dict["filled_avg_price"] if data_dict["filled_avg_price"] else 0),
        order_class=str(data_dict["order_class"] if data_dict["order_class"] else ""),
        order_type=str(data_dict["order_type"] if data_dict["order_type"] else ""),
        type=str(data_dict["type"] if data_dict["type"] else ""),
        side=str(data_dict["side"] if data_dict["side"] else ""),
        time_in_force=str(data_dict["time_in_force"] if data_dict["time_in_force"] else ""),
        limit_price=float(data_dict["limit_price"] if data_dict["limit_price"] else 0),
        stop_price=float(data_dict["stop_price"] if data_dict["stop_price"] else 0),
        status=str(data_dict["status"] if data_dict["status"] else ""),
        extended_hours=bool(data_dict["extended_hours"]),
        legs=data_dict["legs"] if data_dict["legs"] else {},
        trail_percent=float(data_dict["trail_percent"] if data_dict["trail_percent"] else 0),
        trail_price=float(data_dict["trail_price"] if data_dict["trail_price"] else 0),
        hwm=float(data_dict["hwm"] if data_dict["hwm"] else 0),
        subtag=str(data_dict["subtag"] if data_dict["subtag"] else ""),
        source=str(data_dict["source"] if data_dict["source"] else ""),
    )
