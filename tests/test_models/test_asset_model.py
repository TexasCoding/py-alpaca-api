from py_alpaca_api.models.asset_model import AssetModel, asset_class_from_dict


def test_asset_class_from_dict():
    data_dict = {
        "id": "12345678",
        "asset_class": "equity",
        "easy_to_borrow": True,
        "exchange": "NYSE",
        "fractionable": False,
        "maintenance_margin_requirement": 0.25,
        "marginable": True,
        "name": "Apple Inc.",
        "shortable": False,
        "status": "active",
        "symbol": "AAPL",
        "tradable": True,
    }
    expected_asset = AssetModel(
        id="12345678",
        asset_class="equity",
        easy_to_borrow=True,
        exchange="NYSE",
        fractionable=False,
        maintenance_margin_requirement=0.25,
        marginable=True,
        name="Apple Inc.",
        shortable=False,
        status="active",
        symbol="AAPL",
        tradable=True,
    )
    assert asset_class_from_dict(data_dict) == expected_asset
