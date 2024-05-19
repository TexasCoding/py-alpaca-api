import json

import pandas as pd
import requests

from .account import Account
from .data_classes import PositionClass, position_class_from_dict


class Position:
    def __init__(self, trade_url: str, headers: object, account: Account) -> None:
        """Initialize Position class

        Parameters:
        ___________
        trade_url: str
                Alpaca Trade API URL required

        headers: object
                API request headers required

        account: Account
                Account object required

        Raises:
        _______
        ValueError: If trade URL is not provided

        ValueError: If headers are not provided

        ValueError: If account is not provided

        """  # noqa

        self.trade_url = trade_url
        self.headers = headers
        self.account = account

    ########################################################
    # \\\\\\\\\\\\\\\\\ Get Positions /////////////////////#
    ########################################################
    def get_all(self) -> pd.DataFrame:
        """Get all positions information from Alpaca API

        Returns:
        --------
        pd.DataFrame:   All positions information as a DataFrame with columns:
                    asset_id, symbol, exchange, asset_class, avg_entry_price, qty, qty_available, side, market_value, cost_basis,
                    profit_dol, profit_pct, intraday_profit_dol, intraday_profit_pct, portfolio_pct, current_price, lastday_price,
                    change_today, asset_marginable

        Raises:
        -------
        Exception: If failed to get positions information

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            positions = api.position.get_all()
            print(positions)

        asset_id symbol exchange asset_class  avg_entry_price  qty  qty_available  side  market_value  cost_basis  profit_dol  profit_pct  \
        0           Cash  Cash         Cash          0.0000  0.0            0.0  Cash       10000.0         0.0         0.0      0.000
        1  ASSET_ID   AAPL   NASDAQ   us_equity        100.0000  10.0           10.0  long       1000.0      1000.0         0.0      0.000

        intraday_profit_dol  intraday_profit_pct  portfolio_pct  current_price  lastday_price  change_today  asset_marginable
        0                  0.0                0.000         1.0000            0.0            0.0           0.0             False
        1                  0.0                0.000         0.1000          100.0          100.0           0.0              True
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
        """Get position information by symbol or asset ID

        Parameters:
        -----------
        symbol:         Asset symbol to get position information
                        A valid asset symbol string (optional) str

        symbol_dict:    Asset symbol dictionary to get position information
                        A valid asset symbol dictionary (optional) dict

        Returns:
        --------
        PositionClass:  Position information as a PositionClass object with attributes:
                    asset_id, symbol, exchange, asset_class, avg_entry_price, qty, qty_available, side, market_value, cost_basis,
                    profit_dol, profit_pct, intraday_profit_dol, intraday_profit_pct, portfolio_pct, current_price, lastday_price,
                    change_today, asset_marginable

        Raises:
        -------
        ValueError:     ValueError if symbol or symbol_dict is not provided

        ValueError:     ValueError if both symbol and symbol_dict are provided

        Exception:      Exception if failed to get position information

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            position = api.position.get(symbol="AAPL")
            print(position)

        PositionClass(
            asset_id="375f6b6e-3b5f-4b2b-8f6b-2e6b2a6b2e6b",
            symbol="AAPL",
            exchange="NASDAQ",
            asset_class="us_equity",
            avg_entry_price=100.0,
            qty=10.0,
            qty_available=10.0,
            side="long",
            market_value=1000.0,
            cost_basis=1000.0,
            profit_dol=0.0,
            profit_pct=0.0,
            intraday_profit_dol=0.0,
            intraday_profit_pct=0.0,
            portfolio_pct=0.1,
            current_price=100.0,
            lastday_price=100.0,
            change_today=0.0,
            asset_marginable=True
        )
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
        """Close all positions from Alpaca API

        Parameters:
        -----------
        cancel_orders:  Cancel open orders (default: False)
                        Cancel open orders (optional) bool

        Returns:
        --------
        str:            Text message for closing all positions confirmation

        Raises:
        -------
        Exception:      Exception if failed to close positions

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            message = api.position.close_all()
            print(message)

        '1 positions have been closed'
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
        """Close position by symbol or asset ID from Alpaca API

        Parameters:
        -----------
        symbol_or_id:   Asset symbol or asset ID to close position
                        A valid asset symbol or asset ID string required

        qty:            Quantity to close position (optional)
                        Quantity to close position (optional) float

        percentage:     Percentage to close position (optional)
                        Percentage to close position (optional) int

        Returns:
        --------
        str:            Text message for closing position confirmation

        Raises:
        -------
        ValueError:     ValueError if quantity or percentage is not provided

        ValueError:     ValueError if both quantity and percentage are provided

        ValueError:     ValueError if percentage is not between 0 and 100

        ValueError:     ValueError if symbol or asset_id is not provided

        Exception:      Exception if failed to close position

        Example:
        --------
        >>> from py_alpaca_api import PyAlpacaApi
            api = PyAlpacaApi(api_key="API", api_secret="SECRET", api_paper=True)
            message = api.position.close(symbol_or_id="AAPL", qty=10)
            print(message)

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
