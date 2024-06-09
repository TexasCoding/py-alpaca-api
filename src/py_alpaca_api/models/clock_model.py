from dataclasses import dataclass
from datetime import datetime

from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class ClockModel:
    market_time: datetime
    is_open: bool
    next_open: datetime
    next_close: datetime


############################################
# Data Class Clock Conversion Functions
############################################
def clock_class_from_dict(data_dict: dict) -> ClockModel:
    """
    Args:
        data_dict: A dictionary containing data for creating an instance of `ClockModel`.

    Returns:
        An instance of `ClockModel` created using the data from `data_dict`.

    Raises:
        None.
    """
    clock_data = extract_class_data(data_dict, KEY_PROCESSORS, ClockModel)
    return ClockModel(**clock_data)
