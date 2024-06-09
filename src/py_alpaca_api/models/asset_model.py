from dataclasses import dataclass

from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class AssetModel:
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
# Data Class Asset Conversion Functions
############################################
def asset_class_from_dict(data_dict: dict) -> AssetModel:
    """
    Args:
        data_dict: A dictionary containing the data for creating an instance of AssetModel.

    Returns:
        An instance of the AssetModel class.

    Raises:
        None
    """
    asset_data = extract_class_data(data_dict, KEY_PROCESSORS, AssetModel)
    return AssetModel(**asset_data)
