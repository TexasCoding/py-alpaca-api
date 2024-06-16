from dataclasses import dataclass
from datetime import datetime

from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class QuoteModel:
    symbol: str
    timestamp: datetime
    ask: float
    ask_size: int
    bid: float
    bid_size: int


############################################
# Data Class Quote Conversion Functions
############################################
def quote_class_from_dict(data_dict: dict) -> QuoteModel:
    """
    Args:
        data_dict: A dictionary containing data for creating an instance of `QuoteModel`.

    Returns:
        An instance of `QuoteModel` created using the data from `data_dict`.

    Raises:
        None.
    """
    clock_data = extract_class_data(data_dict, KEY_PROCESSORS, QuoteModel)
    return QuoteModel(**clock_data)
