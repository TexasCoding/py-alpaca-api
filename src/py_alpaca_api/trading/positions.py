import json
from typing import Dict

import pandas as pd

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.position_model import PositionModel, position_class_from_dict
from py_alpaca_api.trading.account import Account


class Positions:
    def __init__(
        self, base_url: str, headers: Dict[str, str], account: Account
    ) -> None:
        self.base_url = base_url
        self.headers = headers
        self.account = account

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

        url = f"{self.base_url}/positions"
        params = {"cancel_orders": cancel_orders}

        response = json.loads(
            Requests()
            .request(method="DELETE", url=url, headers=self.headers, params=params)
            .text
        )
        return f"{len(response)} positions have been closed"

    ########################################################
    # \\\\\\\\\\\\\\\\\\ Close Position ///////////////////#
    ########################################################
    def close(
        self, symbol_or_id: str, qty: float = None, percentage: int = None
    ) -> str:
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

        url = f"{self.base_url}/positions/{symbol_or_id}"
        params = {"qty": qty, "percentage": percentage}
        Requests().request(
            method="DELETE", url=url, headers=self.headers, params=params
        )

        return f"Position {symbol_or_id} has been closed"

    def get(self, symbol: str) -> PositionModel:
        """
        Retrieves the position for the specified symbol.

        Args:
            symbol (str): The symbol of the asset for which to retrieve the position.

        Returns:
            PositionModel: The position for the specified symbol.

        Raises:
            ValueError: If the symbol is not provided or if a position for the specified symbol is not found.
        """

        if not symbol:
            raise ValueError("Symbol is required.")

        try:
            position = self.get_all().query(f"symbol == '{symbol}'").iloc[0]
        except IndexError:
            raise ValueError(f"Position for symbol '{symbol}' not found.")

        return position_class_from_dict(position)

    ############################################
    # Get All Positions
    ############################################
    def get_all(
        self, order_by: str = "profit_pct", order_asc: bool = False
    ) -> pd.DataFrame:
        """
        Retrieves all positions for the user's Alpaca account, including cash positions.

        The positions are returned as a pandas DataFrame, with the following columns:
        - asset_id: The unique identifier for the asset
        - symbol: The symbol for the asset
        - exchange: The exchange the asset is traded on
        - asset_class: The class of the asset (e.g. 'stock', 'crypto')
        - avg_entry_price: The average price at which the position was entered
        - qty: The quantity of the asset held in the position
        - qty_available: The quantity of the asset that is available to trade
        - side: The side of the position (either 'long' or 'short')
        - market_value: The current market value of the position
        - cost_basis: The total cost basis of the position
        - profit_dol: The unrealized profit/loss in dollars
        - profit_pct: The unrealized profit/loss as a percentage
        - intraday_profit_dol: The unrealized intraday profit/loss in dollars
        - intraday_profit_pct: The unrealized intraday profit/loss as a percentage
        - portfolio_pct: The percentage of the total portfolio value that this position represents
        - current_price: The current price of the asset
        - lastday_price: The price of the asset at the end of the previous trading day
        - change_today: The percent change in the asset's price from the previous trading day
        - asset_marginable: Whether the asset is marginable or not

        The positions are sorted based on the provided `order_by` parameter, in ascending or descending order based on the `order_asc` parameter.
        """
        sorting_list = [
            "profit_pct",
            "profit_dol",
            "intraday_profit_pct",
            "intraday_profit_dol",
            "market_value",
            "symbol",
            "exchange",
            "asset_class",
            "avg_entry_price",
            "qty",
            "qty_available",
            "side",
            "cost_basis",
            "current_price",
            "lastday_price",
            "change_today",
            "asset_marginable",
        ]

        if order_by not in sorting_list:
            raise ValueError(
                f"Sorting by '{order_by}' is not supported. Please use one of the following: {', '.join(sorting_list)}"
            )

        url = f"{self.base_url}/positions"
        response = json.loads(Requests().request("GET", url, headers=self.headers).text)
        positions_df = pd.DataFrame(response)

        if not positions_df.empty:
            positions_df = pd.concat(
                [self.cash_position_df(), positions_df], ignore_index=True
            )
        else:
            positions_df = self.cash_position_df()

        positions_df = self.modify_position_df(positions_df)

        return positions_df.sort_values(by=order_by, ascending=order_asc).reset_index(
            drop=True
        )

    ############################################
    # static Modify Positions DataFrame
    ############################################
    @staticmethod
    def modify_position_df(positions_df: pd.DataFrame) -> pd.DataFrame:
        """
        Modifies the given positions DataFrame by renaming columns, converting data types,
        and rounding values.

        Args:
            positions_df (pd.DataFrame): The positions DataFrame to be modified.

        Returns:
            pd.DataFrame: The modified positions DataFrame.
        """
        positions_df.rename(
            columns={
                "unrealized_pl": "profit_dol",
                "unrealized_plpc": "profit_pct",
                "unrealized_intraday_pl": "intraday_profit_dol",
                "unrealized_intraday_plpc": "intraday_profit_pct",
            },
            inplace=True,
        )

        positions_df["market_value"] = positions_df["market_value"].astype(float)
        asset_sum = positions_df["market_value"].sum()
        positions_df["portfolio_pct"] = positions_df["market_value"] / asset_sum

        positions_df = positions_df.astype(
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

        positions_df[round_2] = positions_df[round_2].apply(
            lambda x: pd.Series.round(x, 2)
        )
        positions_df[round_4] = positions_df[round_4].apply(
            lambda x: pd.Series.round(x, 4) * 100
        )

        return positions_df

    ############################################
    # Cash Position DataFrame
    ############################################
    def cash_position_df(self):
        """
        Retrieves the user's cash position data as a DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the user's cash position data.
        """
        return pd.DataFrame(
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
