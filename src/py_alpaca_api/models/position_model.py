from dataclasses import dataclass

from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class PositionModel:
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
# Data Class Position Conversion Functions
############################################
def position_class_from_dict(data_dict: dict) -> PositionModel:
    """
    Returns a PositionModel object created from a given data dictionary.

    Args:
        data_dict: A dictionary containing the data for creating a PositionModel object.

    Returns:
        PositionModel: A PositionModel object created using the data from the dictionary.
    """
    position_data = extract_class_data(data_dict, KEY_PROCESSORS, PositionModel)
    return PositionModel(**position_data)
