from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Union

from py_alpaca_api.models.asset_model import AssetModel
from py_alpaca_api.models.model_utils import KEY_PROCESSORS, extract_class_data


@dataclass
class WatchlistModel:
    id: str
    account_id: str
    created_at: datetime
    updated_at: datetime
    name: str
    assets: List[Union[object | AssetModel]]


############################################
# Data Class Watchlist Conversion Functions
############################################
def process_assets(assets: List[Dict]) -> List[AssetModel]:
    """Process a list of assets.

    This function takes a list of asset dictionaries and returns a list of AssetModel objects.
    Each asset dictionary should contain the necessary information to create an AssetModel object.

    Args:
        assets (List[Dict]): A list of asset dictionaries.

    Returns:
        List[AssetModel]: A list of AssetModel objects.
    """
    if not assets:
        return []
    return (
        [
            AssetModel(**extract_class_data(asset, KEY_PROCESSORS, AssetModel))
            for asset in assets
        ]
        if assets
        else []
    )


def watchlist_class_from_dict(data_dict: dict) -> WatchlistModel:
    """
    Args:
        data_dict: A dictionary containing the data needed to create a WatchlistModel object.

    Returns:
        A new instance of the WatchlistModel created from the data in the input dictionary.
    """
    watchlist_data = extract_class_data(data_dict, KEY_PROCESSORS, WatchlistModel)
    watchlist_data["assets"] = process_assets(data_dict.get("assets", []))
    return WatchlistModel(**watchlist_data)
