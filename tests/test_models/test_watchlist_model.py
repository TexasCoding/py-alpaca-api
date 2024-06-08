import pytest
import pendulum
from py_alpaca_api.models.asset_model import AssetModel
from py_alpaca_api.models.watchlist_model import (
    WatchlistModel,
    watchlist_class_from_dict,
)


def test_watchlist_class_from_dict_with_valid_data():
    data_dict = {
        "id": "12345678",
        "account_id": "87654321",
        "name": "My Watchlist",
        "assets": [
            {
                "id": "asset1",
                "symbol": "AAPL",
                "easy_to_borrow": True,
                "tradable": True,
                "fractionable": True,
                "marginable": True,
                "shortable": True,
                "status": "active",
                "exchange": "NASDAQ",
                "maintenance_margin_requirement": 0.05,
                "name": "",
                "asset_class": "us_equity",
            },
            {
                "id": "asset2",
                "symbol": "GOOG",
                "easy_to_borrow": True,
                "tradable": True,
                "fractionable": True,
                "marginable": True,
                "shortable": True,
                "status": "active",
                "exchange": "NASDAQ",
                "maintenance_margin_requirement": 0.05,
                "name": "",
                "asset_class": "us_equity",
            },
        ],
        "created_at": "2021-01-01T00:00:00.000Z",
        "updated_at": "2021-01-01T00:00:00.000Z",
    }
    expected_watchlist = WatchlistModel(
        id="12345678",
        account_id="87654321",
        name="My Watchlist",
        assets=[
            AssetModel(
                id="asset1",
                asset_class="us_equity",
                symbol="AAPL",
                easy_to_borrow=True,
                name="",
                maintenance_margin_requirement=0.05,
                tradable=True,
                fractionable=True,
                marginable=True,
                shortable=True,
                status="active",
                exchange="NASDAQ",
            ),
            AssetModel(
                id="asset2",
                symbol="GOOG",
                easy_to_borrow=True,
                asset_class="us_equity",
                name="",
                maintenance_margin_requirement=0.05,
                tradable=True,
                fractionable=True,
                marginable=True,
                shortable=True,
                status="active",
                exchange="NASDAQ",
            ),
        ],
        created_at=pendulum.DateTime(
            2021, 1, 1, 0, 0, 0, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=pendulum.DateTime(
            2021, 1, 1, 0, 0, 0, tzinfo=pendulum.Timezone("UTC")
        ).strftime("%Y-%m-%d %H:%M:%S"),
    )
    assert watchlist_class_from_dict(data_dict) == expected_watchlist


def test_watchlist_class_from_dict_with_invalid_data():
    data_dict = {
        "id": 12345678,
        "account_id": 87654321,
        "name": "My Watchlist",
        "assets": [
            {"id": "asset1", "symbol": "AAPL"},
            {"id": "asset2", "symbol": "GOOG"},
        ],
    }
    with pytest.raises(Exception):
        watchlist_class_from_dict(data_dict)
