import json
from unittest.mock import Mock, patch
import pytest
from py_alpaca_api.trading.assets import Assets
from py_alpaca_api.models.asset_model import AssetModel
from py_alpaca_api.http.requests import Requests


@pytest.fixture
def assets_obj():
    return Assets(
        base_url="https://example.com", headers={"Authorization": "Bearer token"}
    )


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
            "asset_class": "us_equity",
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
