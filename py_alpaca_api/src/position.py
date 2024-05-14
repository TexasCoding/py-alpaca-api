import json

import pandas as pd
import requests

from .account import Account
from .data_classes import PositionClass, position_class_from_dict


class Position:
    def __init__(self, trade_url: str, headers: object, account: Account) -> None:
        self.trade_url = trade_url
        self.headers = headers
        self.account = account

    ########################################################
    # \\\\\\\\\\\\\\\\\ Get Positions /////////////////////#
    ########################################################
    def get_all(self) -> pd.DataFrame:
        """Get account positions, including cash

        Returns:
        --------
        DataFrame:  Account positions as a DataFrame with columns:
                    asset_id, symbol, exchange, asset_class, qty, qty_available, side, market_value, cost_basis, profit_dol, profit_pct,
                    intraday_profit_dol, intraday_profit_pct, portfolio_pct, current_price, lastday_price, change_today, asset_marginable

        Raises:
        -------
        Exception:
            Exception if failed to get account positions

        Example:
        --------
        >>> get_positions()
            asset_id    symbol  exchange    asset_class qty qty_available   side    market_value    cost_basis  profit_dol  profit_pct  intraday_profit_dol intraday_profit_pct portfolio_pct   current_price   lastday_price   change_today    asset_marginable
        0   ""          Cash    ""          ""          0   0               ""      1000.0          0.0         0.0         0.0         0.0                 0.0                 1.0             1.0             1.0             0.0             False
        1   ASSET_ID    AAPL    NASDAQ      us_equity   10  10              long    1000.0          1000.0      0.0         0.0         0.0                 0.0                 0.0             100.0           100.0           0.0             True
        """  # noqa

        # Url for positions
        url = f"{self.trade_url}/positions"
        # Get request to Alpaca API for positions
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code != 200:
            # Raise exception if response is not successful
            raise Exception(response.text)
        # Normalize JSON response and convert to DataFrame
        res_data_df = pd.json_normalize(json.loads(response.text))
        # Create DataFrame for Cash position
        pos_data_df = pd.DataFrame(
            {
                "asset_id": "",
                "symbol": "Cash",
                "exchange": "",
                "asset_class": "",
                "avg_entry_price": 0,
                "qty": 0,
                "qty_available": 0,
                "side": "",
                "market_value": self.account.get().cash,
                "cost_basis": 0,
                "unrealized_pl": 0,
                "unrealized_plpc": 0,
                "unrealized_intraday_pl": 0,
                "unrealized_intraday_plpc": 0,
                "current_price": 0,
                "lastday_price": 0,
                "change_today": 0,
                "asset_marginable": False,
            },
            index=[0],
        )
        # If response is not empty, concatenate DataFrames
        if not res_data_df.empty:
            # Return DataFrame if no positions
            pos_data_df = pd.concat([pos_data_df, res_data_df], ignore_index=True)
        # Rename columns for consistency
        pos_data_df.rename(
            columns={
                "unrealized_pl": "profit_dol",
                "unrealized_plpc": "profit_pct",
                "unrealized_intraday_pl": "intraday_profit_dol",
                "unrealized_intraday_plpc": "intraday_profit_pct",
            },
            inplace=True,
        )
        # Calculate portfolio percentage
        pos_data_df["market_value"] = pos_data_df["market_value"].astype(float)
        asset_sum = pos_data_df["market_value"].sum()
        pos_data_df["portfolio_pct"] = pos_data_df["market_value"] / asset_sum
        # Convert columns to appropriate data types
        pos_data_df = pos_data_df.astype(
            {
                "asset_id": "str",
                "symbol": "str",
                "exchange": "str",
                "asset_class": "str",
                "avg_entry_price": "float",
                "qty": "float",
                "qty_available": "float",
                "side": "str",
                "market_value": "float",
                "cost_basis": "float",
                "profit_dol": "float",
                "profit_pct": "float",
                "intraday_profit_dol": "float",
                "intraday_profit_pct": "float",
                "portfolio_pct": "float",
                "current_price": "float",
                "lastday_price": "float",
                "change_today": "float",
                "asset_marginable": "bool",
            }
        )
        # Round columns to appropriate decimal places
        round_2 = ["profit_dol", "intraday_profit_dol", "market_value"]
        round_4 = ["profit_pct", "intraday_profit_pct", "portfolio_pct"]

        pos_data_df[round_2] = pos_data_df[round_2].apply(lambda x: pd.Series.round(x, 2))
        pos_data_df[round_4] = pos_data_df[round_4].apply(lambda x: pd.Series.round(x, 4))

        return pos_data_df

    ########################################################
    # \\\\\\\\\\\\\\\\\ Get Position //////////////////////#
    ########################################################
    def get(self, symbol: str = None, symbol_dict: dict = None) -> PositionClass:
        """Get position information by symbol or symbol dictionary

        Parameters:
        -----------
        symbol:     Asset symbol to get position information
                    A valid asset symbol string (e.g., AAPL, or asset_id) optional, not required if symbol_dict is provided

        symbol_dict: Position information dictionary
                    A valid position information dictionary optional, not required if symbol is provided

        Returns:
        --------
        PositionClass: Position information as a PositionClass object with values:
                    asset_id, symbol, exchange, asset_class, qty, qty_available, side, market_value, cost_basis, profit_dol, profit_pct,
                    intraday_profit_dol, intraday_profit_pct, portfolio_pct, current_price, lastday_price, change_today, asset_marginable

        Raises:
        -------
        ValueError:
            ValueError if symbol or symbol_dict is not provided

        ValueError:
            ValueError if both symbol and symbol_dict are provided

        ValueError:
            ValueError if failed to get position information

        Example:
        --------
        >>> get_position(symbol="AAPL")
        PositionClass(asset_id='ASSET_ID', symbol='AAPL', exchange='NASDAQ', asset_class='us_equity', qty=10.0, qty_available=10.0, \
                    side='long', market_value=1000.0, cost_basis=1000.0, profit_dol=0.0, profit_pct=0.0, intraday_profit_dol=0.0, \
                    intraday_profit_pct=0.0, portfolio_pct=1.0, current_price=100.0, lastday_price=100.0, change_today=0.0, asset_marginable=True)

        >>> get_position(symbol_dict={"asset_id": "ASSET_ID", "symbol": "AAPL", "exchange": "NASDAQ", "asset_class": "us_equity", \
                    "qty": 10.0, "qty_available": 10.0, "side": "long", "market_value": 1000.0, "cost_basis": 1000.0, "profit_dol": 0.0, \
                    "profit_pct": 0.0, "intraday_profit_dol": 0.0, "intraday_profit_pct": 0.0, "portfolio_pct": 1.0, "current_price": 100.0, \
                    "lastday_price": 100.0, "change_today": 0.0, "asset_marginable": True})
        PositionClass(asset_id='ASSET_ID', symbol='AAPL', exchange='NASDAQ', asset_class='us_equity', qty=10.0, qty_available=10.0, \
                    side='long', market_value=1000.0, cost_basis=1000.0, profit_dol=0.0, profit_pct=0.0, intraday_profit_dol=0.0, \
                    intraday_profit_pct=0.0, portfolio_pct=1.0, current_price=100.0, lastday_price=100.0, change_today=0.0, asset_marginable=True)
        """  # noqa
        # Check if symbol or symbol_dict is provided
        if not symbol and not symbol_dict:
            # Raise ValueError if symbol or symbol_dict is not provided
            raise ValueError("Symbol or symbol_dict is required.")
        # Check if both symbol and symbol_dict are provided
        if symbol and symbol_dict:
            # Raise ValueError if both symbol and symbol_dict are provided
            raise ValueError("Symbol or symbol_dict is required, not both.")

        # Check if symbol_dict is provided
        if symbol_dict:
            # Return position information as a PositionClass object
            return position_class_from_dict(symbol_dict)

        # If symbol is provided get position information from Alpaca API
        url = f"{self.trade_url}/positions/{symbol}"
        # Get request to Alpaca API for position information
        response = requests.get(url, headers=self.headers)
        # Check if response is successful
        if response.status_code != 200:
            # Raise exception if response is not successful
            raise ValueError(response.text)

        res_dict = json.loads(response.text)

        equity = self.account.get().equity
        res_dict["portfolio_pct"] = round(float(res_dict["market_value"]) / equity, 4)

        res_dict["profit_dol"] = round(float(res_dict["unrealized_pl"]), 2)
        del res_dict["unrealized_pl"]

        res_dict["profit_pct"] = round(float(res_dict["unrealized_plpc"]), 4)
        del res_dict["unrealized_plpc"]

        res_dict["intraday_profit_dol"] = round(float(res_dict["unrealized_intraday_pl"]), 2)
        del res_dict["unrealized_intraday_pl"]

        res_dict["intraday_profit_pct"] = round(float(res_dict["unrealized_intraday_plpc"]), 4)
        del res_dict["unrealized_intraday_plpc"]

        # Return position information as a PositionClass object
        return position_class_from_dict(res_dict)

    ########################################################
    # \\\\\\\\\\\\\\\\ Close All Positions ////////////////#
    ########################################################
    def close_all(self, cancel_orders: bool = False) -> str:
        """Close all positions

        Parameters:
        -----------
        cancel_orders:  Cancel open orders (default: False)
                        Cancel open orders before closing positions (optional) bool

        Returns:
        --------
        str:            Position closing confirmation message

        Raises:
        -------
        Exception:
            Exception if failed to close positions

        Example:
        --------
        >>> close_all_positions()
        '2 positions have been closed'
        """  # noqa
        # Url for positions
        url = f"{self.trade_url}/positions"
        # Parameters for the request
        params = {"cancel_orders": cancel_orders}
        # Delete request to Alpaca API for closing all positions
        response = requests.delete(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code == 207:
            # Convert JSON response to dictionary
            res = json.loads(response.text)
            # Return text message
            return f"{len(res)} positions have been closed"
        # If response is not successful, raise an exception
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to close positions. Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\\\ Close Position ///////////////////#
    ########################################################
    def close(self, symbol_or_id: str, qty: float = None, percentage: int = None) -> str:
        """Close a position by symbol or asset ID

        Parameters:
        -----------
        symbol_or_id:   Asset symbol or asset ID to close position
                        A valid asset symbol or asset ID string required

        qty:            Quantity to close position (default: None)
                        Quantity to close position (optional) float

        percentage:     Percentage to close position (default: None)
                        Percentage to close position (optional) int

        Returns:
        --------
        str:            Position closing confirmation message

        Raises:
        -------
        ValueError:
            ValueError if quantity or percentage is not provided

        ValueError:
            ValueError if both quantity and percentage are provided

        ValueError:
            ValueError if percentage is not between 0 and 100

        ValueError:
            ValueError if symbol or asset_id is not provided

        Exception:
            Exception if failed to close position

        Example:
        --------
        >>> close_position(symbol_or_id="AAPL", qty=10)
        'Position AAPL has been closed'
        """  # noqa

        # Check if quantity or percentage is provided
        if not qty and not percentage:
            raise ValueError("Quantity or percentage is required.")
        # Check if both quantity and percentage are provided
        if qty and percentage:
            raise ValueError("Quantity or percentage is required, not both.")
        # Check if percentage is between 0 and 100
        if percentage and (percentage < 0 or percentage > 100):
            raise ValueError("Percentage must be between 0 and 100.")
        # Check if symbol or asset_id is provided
        if not symbol_or_id:
            raise ValueError("Symbol or asset_id is required.")
        # Url for closing position
        url = f"{self.trade_url}/positions/{symbol_or_id}"
        # Parameters for the request
        params = {"qty": qty, "percentage": percentage}
        # Delete request to Alpaca API for closing position
        response = requests.delete(url, headers=self.headers, params=params)
        # Check if response is successful
        if response.status_code == 200:
            return f"Position {symbol_or_id} has been closed"
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to close position. Response: {res["message"]}')
