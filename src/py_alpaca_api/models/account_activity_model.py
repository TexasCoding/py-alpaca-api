from dataclasses import dataclass
from datetime import datetime
from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class AccountActivityModel:
    activity_type: str
    id: str
    cum_qty: float
    leaves_qty: float
    price: float
    qty: float
    side: str
    symbol: str
    transaction_time: datetime
    order_id: str
    type: str
    order_status: str
    date: datetime
    net_amount: float
    per_share_amount: float


############################################
# Data Class Asset Conversion Functions
############################################
def account_activity_class_from_dict(data_dict: dict) -> AccountActivityModel:
    """
    Args:
        data_dict: A dictionary containing the data for creating an instance of AccountActivityModel.

    Returns:
        An instance of the AccountActivityModel class.

    Raises:
        None
    """
    account_activity_data = extract_class_data(
        data_dict, KEY_PROCESSORS, AccountActivityModel
    )
    return AccountActivityModel(**account_activity_data)
