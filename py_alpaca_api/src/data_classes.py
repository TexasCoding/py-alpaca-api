from dataclasses import dataclass
from datetime import datetime


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


@dataclass
class AccountClass:
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


def account_class_from_dict(data_dict):
    return AccountClass(
        id=str(data_dict["id"]) if data_dict["id"] else "",
        admin_configurations=(object(data_dict["admin_configurations"]) if data_dict["admin_configurations"] else {}),
        user_configurations=(object(data_dict["user_configurations"]) if data_dict["user_configurations"] else {}),
        account_number=str(data_dict["account_number"]),
        status=str(data_dict["status"]) if data_dict["status"] else "",
        crypto_status=(str(data_dict["crypto_status"]) if data_dict["crypto_status"] else ""),
        options_approved_level=(int(data_dict["options_approved_level"]) if data_dict["options_approved_level"] else None),
        options_trading_level=(int(data_dict["options_trading_level"]) if data_dict["options_trading_level"] else None),
        currency=str(data_dict["currency"]) if data_dict["currency"] else "",
        buying_power=(float(data_dict["buying_power"]) if data_dict["buying_power"] else None),
        regt_buying_power=(float(data_dict["regt_buying_power"]) if data_dict["regt_buying_power"] else None),
        daytrading_buying_power=(float(data_dict["daytrading_buying_power"]) if data_dict["daytrading_buying_power"] else None),
        effective_buying_power=(float(data_dict["effective_buying_power"]) if data_dict["effective_buying_power"] else None),
        non_marginable_buying_power=(float(data_dict["non_marginable_buying_power"]) if data_dict["non_marginable_buying_power"] else None),
        options_buying_power=(float(data_dict["options_buying_power"]) if data_dict["options_buying_power"] else None),
        bod_dtbp=(float(data_dict["bod_dtbp"]) if data_dict["bod_dtbp"] else None),
        cash=float(data_dict["cash"]) if data_dict["cash"] else None,
        accrued_fees=(float(data_dict["accrued_fees"]) if data_dict["accrued_fees"] else None),
        pending_transfer_in=(float(data_dict["pending_transfer_in"]) if data_dict["pending_transfer_in"] else None),
        portfolio_value=(float(data_dict["portfolio_value"]) if data_dict["portfolio_value"] else None),
        pattern_day_trader=bool(data_dict["pattern_day_trader"]),
        trading_blocked=bool(data_dict["trading_blocked"]),
        transfers_blocked=bool(data_dict["transfers_blocked"]),
        account_blocked=bool(data_dict["account_blocked"]),
        created_at=(data_dict["created_at"].split(".")[0].replace("T", " ") if data_dict["created_at"] else None),
        trade_suspended_by_user=bool(data_dict["trade_suspended_by_user"]),
        multiplier=(int(data_dict["multiplier"]) if data_dict["multiplier"] else None),
        shorting_enabled=bool(data_dict["shorting_enabled"]),
        equity=float(data_dict["equity"]) if data_dict["equity"] else None,
        last_equity=(float(data_dict["last_equity"]) if data_dict["last_equity"] else None),
        long_market_value=(float(data_dict["long_market_value"]) if data_dict["long_market_value"] else None),
        short_market_value=(float(data_dict["short_market_value"]) if data_dict["short_market_value"] else None),
        position_market_value=(float(data_dict["position_market_value"]) if data_dict["position_market_value"] else None),
        initial_margin=(float(data_dict["initial_margin"]) if data_dict["initial_margin"] else None),
        maintenance_margin=(float(data_dict["maintenance_margin"]) if data_dict["maintenance_margin"] else None),
        last_maintenance_margin=(float(data_dict["last_maintenance_margin"]) if data_dict["last_maintenance_margin"] else None),
        sma=float(data_dict["sma"]) if data_dict["sma"] else None,
        daytrade_count=(int(data_dict["daytrade_count"]) if data_dict["daytrade_count"] else None),
        balance_asof=(str(data_dict["balance_asof"]) if data_dict["balance_asof"] else ""),
        crypto_tier=(int(data_dict["crypto_tier"]) if data_dict["crypto_tier"] else None),
        intraday_adjustments=(int(data_dict["intraday_adjustments"]) if data_dict["intraday_adjustments"] else None),
        pending_reg_taf_fees=(float(data_dict["pending_reg_taf_fees"]) if data_dict["pending_reg_taf_fees"] else None),
    )


def asset_class_from_dict(data_dict):
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


def order_class_from_dict(data_dict):
    return OrderClass(
        id=str(data_dict["id"]) if data_dict["id"] else "",
        client_order_id=data_dict["client_order_id"],
        created_at=(data_dict["created_at"].split(".")[0].replace("T", " ") if data_dict["created_at"] else ""),
        updated_at=(data_dict["updated_at"].split(".")[0].replace("T", " ") if data_dict["updated_at"] else ""),
        submitted_at=(data_dict["submitted_at"].split(".")[0].replace("T", " ") if data_dict["submitted_at"] else ""),
        filled_at=(data_dict["filled_at"].split(".")[0].replace("T", " ") if data_dict["filled_at"] else ""),
        expired_at=(data_dict["expired_at"].split(".")[0].replace("T", " ") if data_dict["expired_at"] else ""),
        canceled_at=(data_dict["canceled_at"].split(".")[0].replace("T", " ") if data_dict["canceled_at"] else ""),
        failed_at=(data_dict["failed_at"].split(".")[0].replace("T", " ") if data_dict["failed_at"] else ""),
        replaced_at=(data_dict["replaced_at"].split(".")[0].replace("T", " ") if data_dict["replaced_at"] else ""),
        replaced_by=(data_dict["replaced_by"].split(".")[0].replace("T", " ") if data_dict["replaced_by"] else ""),
        replaces=str(data_dict["replaces"]) if data_dict["replaces"] else "",
        asset_id=str(data_dict["asset_id"]) if data_dict["asset_id"] else "",
        symbol=str(data_dict["symbol"]) if data_dict["symbol"] else "",
        asset_class=(str(data_dict["asset_class"]) if data_dict["asset_class"] else ""),
        notional=float(data_dict["notional"]) if data_dict["notional"] else 0,
        qty=float(data_dict["qty"]) if data_dict["qty"] else 0,
        filled_qty=(float(data_dict["filled_qty"]) if data_dict["filled_qty"] else 0),
        filled_avg_price=(float(data_dict["filled_avg_price"]) if data_dict["filled_avg_price"] else 0),
        order_class=(str(data_dict["order_class"]) if data_dict["order_class"] else ""),
        order_type=(str(data_dict["order_type"]) if data_dict["order_type"] else ""),
        type=str(data_dict["type"]) if data_dict["type"] else "",
        side=str(data_dict["side"]) if data_dict["side"] else "",
        time_in_force=(str(data_dict["time_in_force"]) if data_dict["time_in_force"] else ""),
        limit_price=(float(data_dict["limit_price"]) if data_dict["limit_price"] else 0),
        stop_price=(float(data_dict["stop_price"]) if data_dict["stop_price"] else 0),
        status=str(data_dict["status"]) if data_dict["status"] else "",
        extended_hours=bool(data_dict["extended_hours"]),
        legs=object(data_dict["legs"]) if data_dict["legs"] else {},
        trail_percent=(float(data_dict["trail_percent"]) if data_dict["trail_percent"] else 0),
        trail_price=(float(data_dict["trail_price"]) if data_dict["trail_price"] else 0),
        hwm=float(data_dict["hwm"]) if data_dict["hwm"] else 0,
        subtag=str(data_dict["subtag"]) if data_dict["subtag"] else "",
        source=str(data_dict["source"]) if data_dict["source"] else "",
    )
