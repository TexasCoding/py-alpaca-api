import json
import os
from unittest.mock import Mock, patch
import pandas as pd
import pytest
from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.stock.assets import Assets
from py_alpaca_api.models.asset_model import AssetModel
from py_alpaca_api.http.requests import Requests


api_key = os.environ.get("ALPACA_API_KEY")
api_secret = os.environ.get("ALPACA_SECRET_KEY")


@pytest.fixture
def assets_obj():
    return Assets(
        base_url="https://example.com", headers={"Authorization": "Bearer token"}
    )


@pytest.fixture
def alpaca():
    return PyAlpacaAPI(api_key=api_key, api_secret=api_secret, api_paper=True)


def test_get_asset_invalid_symbol(alpaca):
    with pytest.raises(Exception):
        alpaca.stock.assets.get("INVALID")


def test_get_all_assets_successful(alpaca):
    assets = alpaca.stock.assets.get_all()
    assert isinstance(assets, pd.DataFrame)
    assert len(assets) > 0
    assert isinstance(assets.iloc[0].id, str)
    assert isinstance(assets.iloc[0].exchange, str)
    assert isinstance(assets.iloc[0].symbol, str)
    assert isinstance(assets.iloc[0].status, str)
    assert assets.dtypes.tradable == "bool"
    assert assets.dtypes.easy_to_borrow == "bool"
    assert assets.dtypes.fractionable == "bool"
    assert assets.dtypes.marginable == "bool"
    assert assets.dtypes.shortable == "bool"


def test_get_asset_attributes(alpaca):
    asset = alpaca.stock.assets.get("AAPL")
    assert asset.symbol == "AAPL"
    assert isinstance(asset, AssetModel)
    assert isinstance(asset.id, str)
    assert isinstance(asset.easy_to_borrow, bool)
    assert isinstance(asset.exchange, str)
    assert isinstance(asset.fractionable, bool)
    assert isinstance(asset.maintenance_margin_requirement, float)
    assert isinstance(asset.marginable, bool)
    assert isinstance(asset.name, str)
    assert isinstance(asset.shortable, bool)
    assert isinstance(asset.status, str)
    assert isinstance(asset.symbol, str)
    assert isinstance(asset.tradable, bool)


def test_get_asset_successful(assets_obj):
    mock_response = Mock()
    mock_response.text = json.dumps(
        {
            "id": "asset_id",
            "symbol": "AAPL",
            "easy_to_borrow": True,
            "fractionable": True,
            "maintenance_margin_requirement": 0.25,
            "marginable": True,
            "name": "Apple Inc.",
            "shortable": True,
            "status": "active",
            "tradable": True,
            "class": "us_equity",
            "exchange": "NASDAQ",
        }
    )
    mock_response.status_code = 200
    with patch.object(Requests, "request", return_value=mock_response):
        asset = assets_obj.get("AAPL")
        assert isinstance(asset, AssetModel)
        assert asset.id == "asset_id"
        assert asset.symbol == "AAPL"


def test_get_asset_not_found(assets_obj):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    with patch.object(Requests, "request", return_value=mock_response):
        with pytest.raises(Exception):
            assets_obj.get("INVALID")


def test_get_asset_server_error(assets_obj):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    with patch.object(Requests, "request", return_value=mock_response):
        with pytest.raises(Exception):
            assets_obj.get("AAPL")
