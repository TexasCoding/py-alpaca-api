import json

import pandas as pd
import requests

from .account import Account
from .data_classes import PositionClass, position_class_from_dict


class Position:
    def __init__(self, trade_url: str, headers: dict[str, str], account: Account) -> None:
        """
        Initializes a Position object.

        Args:
            trade_url (str): The URL for trading.
            headers (dict[str, str]): The headers for API requests.
            account (Account): The account associated with the position.

        Returns:
            None
        """
        self.trade_url = trade_url
        self.headers = headers
        self.account = account

    ########################################################
    # \\\\\\\\\\\\\\\\\ Get Positions /////////////////////#
    ########################################################
    def get_all(self) -> pd.DataFrame:
        """
        Retrieves all positions from the Alpaca API and returns them as a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the positions data.

        Raises:
            Exception: If the API response is not successful.
        """

        url = f"{self.trade_url}/positions"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(response.text)

        res_data_df = pd.json_normalize(json.loads(response.text))

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

        if not res_data_df.empty:
            pos_data_df = pd.concat([pos_data_df, res_data_df], ignore_index=True)

        pos_data_df.rename(
            columns={
                "unrealized_pl": "profit_dol",
                "unrealized_plpc": "profit_pct",
                "unrealized_intraday_pl": "intraday_profit_dol",
                "unrealized_intraday_plpc": "intraday_profit_pct",
            },
            inplace=True,
        )

        pos_data_df["market_value"] = pos_data_df["market_value"].astype(float)
        asset_sum = pos_data_df["market_value"].sum()
        pos_data_df["portfolio_pct"] = pos_data_df["market_value"] / asset_sum

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

        round_2 = ["profit_dol", "intraday_profit_dol", "market_value"]
        round_4 = ["profit_pct", "intraday_profit_pct", "portfolio_pct"]

        pos_data_df[round_2] = pos_data_df[round_2].apply(lambda x: pd.Series.round(x, 2))
        pos_data_df[round_4] = pos_data_df[round_4].apply(lambda x: pd.Series.round(x, 4))

        return pos_data_df

    ########################################################
    # \\\\\\\\\\\\\\\\\ Get Position //////////////////////#
    ########################################################
    def get(self, symbol: str = None, symbol_dict: dict = None) -> PositionClass:
        """
        Retrieves position information for a given symbol or symbol dictionary.

        Args:
            symbol (str, optional): The symbol for which to retrieve position information. Defaults to None.
            symbol_dict (dict, optional): A dictionary containing position information. Defaults to None.

        Returns:
            PositionClass: An object representing the position information.

        Raises:
            ValueError: If neither symbol nor symbol_dict is provided.
            ValueError: If both symbol and symbol_dict are provided.

        """

        if not symbol and not symbol_dict:
            raise ValueError("Symbol or symbol_dict is required.")
        if symbol and symbol_dict:
            raise ValueError("Symbol or symbol_dict is required, not both.")

        if symbol_dict:
            return position_class_from_dict(symbol_dict)

        url = f"{self.trade_url}/positions/{symbol}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
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

        return position_class_from_dict(res_dict)

    ########################################################
    # \\\\\\\\\\\\\\\\ Close All Positions ////////////////#
    ########################################################
    def close_all(self, cancel_orders: bool = False) -> str:
        """
        Close all positions.

        Args:
            cancel_orders (bool, optional): Whether to cancel open orders associated with the positions.
                Defaults to False.

        Returns:
            str: A message indicating the number of positions that have been closed.

        Raises:
            Exception: If the request to close positions is not successful, an exception is raised with
                the error message from the API response.
        """

        url = f"{self.trade_url}/positions"
        params = {"cancel_orders": cancel_orders}
        response = requests.delete(url, headers=self.headers, params=params)

        if response.status_code == 207:
            res = json.loads(response.text)
            return f"{len(res)} positions have been closed"
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to close positions. Response: {res["message"]}')

    ########################################################
    # \\\\\\\\\\\\\\\\\\ Close Position ///////////////////#
    ########################################################
    def close(self, symbol_or_id: str, qty: float = None, percentage: int = None) -> str:
        """
        Closes a position for a given symbol or asset ID.

        Args:
            symbol_or_id (str): The symbol or asset ID of the position to be closed.
            qty (float, optional): The quantity of the position to be closed. Defaults to None.
            percentage (int, optional): The percentage of the position to be closed. Defaults to None.

        Returns:
            str: A message indicating the success or failure of closing the position.

        Raises:
            ValueError: If neither quantity nor percentage is provided.
            ValueError: If both quantity and percentage are provided.
            ValueError: If the percentage is not between 0 and 100.
            ValueError: If symbol_or_id is not provided.
            Exception: If the request to close the position fails.
        """

        if not qty and not percentage:
            raise ValueError("Quantity or percentage is required.")
        if qty and percentage:
            raise ValueError("Quantity or percentage is required, not both.")
        if percentage and (percentage < 0 or percentage > 100):
            raise ValueError("Percentage must be between 0 and 100.")
        if not symbol_or_id:
            raise ValueError("Symbol or asset_id is required.")

        url = f"{self.trade_url}/positions/{symbol_or_id}"
        params = {"qty": qty, "percentage": percentage}
        response = requests.delete(url, headers=self.headers, params=params)

        if response.status_code == 200:
            return f"Position {symbol_or_id} has been closed"
        else:
            res = json.loads(response.text)
            raise Exception(f'Failed to close position. Response: {res["message"]}')
