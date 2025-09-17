import json

import pandas as pd

from py_alpaca_api.exceptions import APIRequestError
from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.account_activity_model import (
    AccountActivityModel,
    account_activity_class_from_dict,
)
from py_alpaca_api.models.account_config_model import (
    AccountConfigModel,
    account_config_class_from_dict,
)
from py_alpaca_api.models.account_model import AccountModel, account_class_from_dict


class Account:
    def __init__(self, headers: dict[str, str], base_url: str) -> None:
        self.headers = headers
        self.base_url = base_url

    ############################################
    # Get Account
    ############################################
    def get(self) -> AccountModel:
        """Retrieves the user's account information.

        Returns:
            AccountModel: The user's account model.
        """
        url = f"{self.base_url}/account"
        http_response = Requests().request("GET", url, headers=self.headers)

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve account: {http_response.status_code}",
            )

        response = json.loads(http_response.text)
        return account_class_from_dict(response)

    #######################################
    # Get Account Activities
    #######################################
    def activities(
        self,
        activity_type: str,
        date: str | None = None,
        until_date: str | None = None,
    ) -> list[AccountActivityModel]:
        """Retrieves the account activities for the specified activity type.

        Optionally filtered by date or until date.

        Args:
            activity_type (str): The type of account activity to retrieve.
            date (str, optional): The date to filter the activities by.
                If provided, only activities on this date will be returned.
            until_date (str, optional): The date to filter the activities up to.
                If provided, only activities up to and including this date
                will be returned.

        Returns:
            List[AccountActivityModel]: A list of account activity models
                representing the retrieved activities.

        Raises:
            ValueError: If the activity type is not provided, or if both
                date and until_date are provided.
        """
        if not activity_type:
            raise ValueError()

        if date and until_date:
            raise ValueError()

        url = f"{self.base_url}/account/activities/{activity_type}"

        params: dict[str, str | bool | float | int] = {}
        if date:
            params["date"] = date
        if until_date:
            params["until_date"] = until_date

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        return [account_activity_class_from_dict(activity) for activity in response]

    ########################################################
    # \\\\\\\\\\\\\  Get Portfolio History ///////////////#
    ########################################################
    def portfolio_history(
        self,
        period: str = "1W",
        timeframe: str = "1D",
        intraday_reporting: str = "market_hours",
    ) -> pd.DataFrame:
        """Retrieves portfolio history data.

        Args:
            period (str): The period of time for which the portfolio history
                is requested. Defaults to "1W" (1 week).
            timeframe (str): The timeframe for the intervals of the portfolio
                history. Defaults to "1D" (1 day).
            intraday_reporting (str): The type of intraday reporting to be used.
                Defaults to "market_hours".

        Returns:
            pd.DataFrame: A pandas DataFrame containing the portfolio history data.

        Raises:
            Exception: If the request to the Alpaca API fails.
        """
        url = f"{self.base_url}/account/portfolio/history"

        params: dict[str, str | bool | float | int] = {
            "period": period,
            "timeframe": timeframe,
            "intraday_reporting": intraday_reporting,
        }

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        if not response or not any(response.values()):
            return pd.DataFrame()

        portfolio_df = pd.DataFrame(response)

        # Only set columns if we have data
        if not portfolio_df.empty:
            # The API may return different numbers of columns depending on the account type
            # We only rename the columns we expect
            expected_columns = [
                "timestamp",
                "equity",
                "profit_loss",
                "profit_loss_pct",
                "base_value",
            ]

            # Only rename columns if we have the expected number or more
            if len(portfolio_df.columns) >= len(expected_columns):
                # Rename the first 5 columns
                portfolio_df.columns = pd.Index(
                    expected_columns
                    + list(portfolio_df.columns[len(expected_columns) :])
                )
                # Keep only the expected columns
                portfolio_df = portfolio_df[expected_columns]
            else:
                # If we have fewer columns than expected, just rename what we have
                portfolio_df.columns = pd.Index(
                    expected_columns[: len(portfolio_df.columns)]
                )

            # Convert timestamp column - explicitly handle as Series
            timestamp_series: pd.Series = pd.Series(
                pd.to_datetime(portfolio_df["timestamp"], unit="s")
            )
            # Now we can safely use dt accessor on the Series
            timestamp_transformed = (
                timestamp_series.dt.tz_localize("America/New_York")
                .dt.tz_convert("UTC")
                .dt.date
            )
            portfolio_df["timestamp"] = timestamp_transformed
            portfolio_df = portfolio_df.astype(
                {
                    "equity": "float",
                    "profit_loss": "float",
                    "profit_loss_pct": "float",
                    "base_value": "float",
                }
            )
            portfolio_df["profit_loss_pct"] = portfolio_df["profit_loss_pct"] * 100

        # Ensure we always return a DataFrame
        assert isinstance(portfolio_df, pd.DataFrame)
        return portfolio_df

    ############################################
    # Get Account Configuration
    ############################################
    def get_configuration(self) -> AccountConfigModel:
        """Retrieves the current account configuration settings.

        Returns:
            AccountConfigModel: The current account configuration.

        Raises:
            APIRequestError: If the request to retrieve configuration fails.
        """
        url = f"{self.base_url}/account/configurations"
        http_response = Requests().request("GET", url, headers=self.headers)

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to retrieve account configuration: {http_response.status_code}",
            )

        response = json.loads(http_response.text)
        return account_config_class_from_dict(response)

    ############################################
    # Update Account Configuration
    ############################################
    def update_configuration(
        self,
        dtbp_check: str | None = None,
        fractional_trading: bool | None = None,
        max_margin_multiplier: str | None = None,
        no_shorting: bool | None = None,
        pdt_check: str | None = None,
        ptp_no_exception_entry: bool | None = None,
        suspend_trade: bool | None = None,
        trade_confirm_email: str | None = None,
    ) -> AccountConfigModel:
        """Updates the account configuration settings.

        Args:
            dtbp_check: Day trade buying power check ("entry", "exit", "both")
            fractional_trading: Whether to enable fractional trading
            max_margin_multiplier: Maximum margin multiplier ("1", "2", "4")
            no_shorting: Whether to disable short selling
            pdt_check: Pattern day trader check ("entry", "exit", "both")
            ptp_no_exception_entry: Whether to enable PTP no exception entry
            suspend_trade: Whether to suspend trading
            trade_confirm_email: Trade confirmation emails ("all", "none")

        Returns:
            AccountConfigModel: The updated account configuration.

        Raises:
            APIRequestError: If the request to update configuration fails.
            ValueError: If invalid parameter values are provided.
        """
        # Validate parameters using a validation map
        validations = {
            "dtbp_check": (dtbp_check, ["entry", "exit", "both"]),
            "pdt_check": (pdt_check, ["entry", "exit", "both"]),
            "max_margin_multiplier": (max_margin_multiplier, ["1", "2", "4"]),
            "trade_confirm_email": (trade_confirm_email, ["all", "none"]),
        }

        for param_name, (value, valid_values) in validations.items():
            if value and value not in valid_values:
                raise ValueError(
                    f"{param_name} must be one of: {', '.join(valid_values)}"
                )

        # Build request body with only provided parameters
        body: dict[str, str | bool] = {}
        if dtbp_check is not None:
            body["dtbp_check"] = dtbp_check
        if fractional_trading is not None:
            body["fractional_trading"] = fractional_trading
        if max_margin_multiplier is not None:
            body["max_margin_multiplier"] = max_margin_multiplier
        if no_shorting is not None:
            body["no_shorting"] = no_shorting
        if pdt_check is not None:
            body["pdt_check"] = pdt_check
        if ptp_no_exception_entry is not None:
            body["ptp_no_exception_entry"] = ptp_no_exception_entry
        if suspend_trade is not None:
            body["suspend_trade"] = suspend_trade
        if trade_confirm_email is not None:
            body["trade_confirm_email"] = trade_confirm_email

        if not body:
            raise ValueError("At least one configuration parameter must be provided")

        url = f"{self.base_url}/account/configurations"
        http_response = Requests().request(
            "PATCH", url, headers=self.headers, json=body
        )

        if http_response.status_code != 200:
            raise APIRequestError(
                http_response.status_code,
                f"Failed to update account configuration: {http_response.status_code}",
            )

        response = json.loads(http_response.text)
        return account_config_class_from_dict(response)
