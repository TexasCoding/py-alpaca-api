from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class OrderModel:
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
# Data Class Order Conversion Functions
############################################
def process_legs(legs: List[Dict]) -> List[OrderModel]:
    """
    Process the legs and create a list of OrderModel objects based on the provided data.

    Args:
        legs (List[Dict]): A list of dictionaries representing the legs.

    Returns:
        List[OrderModel]: A list of OrderModel objects generated from the leg data.

    Note:
        If the legs parameter is empty, an empty list will be returned.
    """
    if not legs:
        return []
    return (
        [
            OrderModel(**extract_class_data(leg, KEY_PROCESSORS, OrderModel))
            for leg in legs
        ]
        if legs
        else []
    )


def order_class_from_dict(data_dict: Dict) -> OrderModel:
    """
    Creates an instance of `OrderModel` using the provided dictionary data.

    Args:
        data_dict (Dict): A dictionary containing the data used to create the `OrderModel` instance.

    Returns:
        OrderModel: An instance of `OrderModel` created using the provided data.

    Raises:
        None
    """
    order_data = extract_class_data(data_dict, KEY_PROCESSORS, OrderModel)
    order_data["legs"] = process_legs(data_dict.get("legs", []))
    return OrderModel(**order_data)
