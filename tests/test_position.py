import json
import unittest
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd

from py_alpaca_api.src import position


class TestPosition(unittest.TestCase):

    @patch("requests.get")
    @patch.object(position.Account, "get")
    def test_get_all(self, mock_get, mock_request_get):
        # Mocking the "get" method of "Account" class
        mock_get.return_value = Mock(cash=10000)

        # Mocking the "get" method of "requests" module
        mock_request_get.return_value = Mock(status_code=200)
        mock_request_get.return_value.text = json.dumps(
            [
                {
                    "asset_id": "ASSET_ID",
                    "symbol": "AAPL",
                    "exchange": "NASDAQ",
                    "asset_class": "us_equity",
                    "avg_entry_price": 100.0000,
                    "qty": 10.0,
                    "qty_available": 10.0,
                    "side": "long",
                    "market_value": 1000.0,
                    "cost_basis": 1000.0,
                    "unrealized_pl": 0.0,
                    "unrealized_plpc": 0.0,
                    "unrealized_intraday_pl": 0.0,
                    "unrealized_intraday_plpc": 0.0,
                    "current_price": 100.0,
                    "lastday_price": 100.0,
                    "change_today": 0.0,
                    "asset_marginable": True,
                }
            ]
        )

        pos = position.Position(
            "https://paper-api.alpaca.markets",
            {"APCA-API-KEY-ID": "API", "APCA-API-SECRET-KEY": "SECRET"},
            position.Account(
                "https://paper-api.alpaca.markets",
                {"APCA-API-KEY-ID": "API", "APCA-API-SECRET-KEY": "SECRET"},
            ),
        )
        df = pos.get_all()

        # assert dataframe structure
        self.assertIsInstance(df, pd.DataFrame)

        # assert index
        self.assertTrue((df.index == np.array([0, 1])).all())

        # assert columns
        expected_columns = [
            "asset_id",
            "symbol",
            "exchange",
            "asset_class",
            "avg_entry_price",
            "qty",
            "qty_available",
            "side",
            "market_value",
            "cost_basis",
            "profit_dol",
            "profit_pct",
            "intraday_profit_dol",
            "intraday_profit_pct",
            "current_price",
            "lastday_price",
            "change_today",
            "asset_marginable",
            "portfolio_pct",
        ]
        self.assertListEqual(df.columns.tolist(), expected_columns)

        # assert values
        self.assertEqual(df.loc[1, "symbol"], "AAPL")
        self.assertEqual(df.loc[1, "qty"], 10)
        self.assertEqual(df.loc[1, "asset_marginable"], True)

    # add other unit tests as needed


if __name__ == "__main__":
    unittest.main()
