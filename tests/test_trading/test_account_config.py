import json
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api.exceptions import APIRequestError
from py_alpaca_api.models.account_config_model import (
    AccountConfigModel,
    account_config_class_from_dict,
)
from py_alpaca_api.trading.account import Account


class TestAccountConfig:
    @pytest.fixture
    def account(self):
        headers = {
            "APCA-API-KEY-ID": "test_key",
            "APCA-API-SECRET-KEY": "test_secret",
        }
        base_url = "https://paper-api.alpaca.markets/v2"
        return Account(headers=headers, base_url=base_url)

    @pytest.fixture
    def mock_config_response(self):
        return {
            "dtbp_check": "entry",
            "fractional_trading": True,
            "max_margin_multiplier": "4",
            "no_shorting": False,
            "pdt_check": "entry",
            "ptp_no_exception_entry": False,
            "suspend_trade": False,
            "trade_confirm_email": "all",
        }

    def test_get_configuration_success(self, account, mock_config_response):
        with patch("py_alpaca_api.trading.account.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = json.dumps(mock_config_response)
            mock_requests.return_value.request.return_value = mock_response

            result = account.get_configuration()

            assert isinstance(result, AccountConfigModel)
            assert result.dtbp_check == "entry"
            assert result.fractional_trading is True
            assert result.max_margin_multiplier == "4"
            assert result.no_shorting is False
            assert result.pdt_check == "entry"
            assert result.ptp_no_exception_entry is False
            assert result.suspend_trade is False
            assert result.trade_confirm_email == "all"

            mock_requests.return_value.request.assert_called_once_with(
                "GET",
                f"{account.base_url}/account/configurations",
                headers=account.headers,
            )

    def test_get_configuration_failure(self, account):
        with patch("py_alpaca_api.trading.account.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 401
            mock_response.text = "Unauthorized"
            mock_requests.return_value.request.return_value = mock_response

            with pytest.raises(APIRequestError) as exc_info:
                account.get_configuration()

            assert exc_info.value.status_code == 401
            assert "Failed to retrieve account configuration" in str(exc_info.value)

    def test_update_configuration_single_param(self, account, mock_config_response):
        mock_config_response["suspend_trade"] = True

        with patch("py_alpaca_api.trading.account.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = json.dumps(mock_config_response)
            mock_requests.return_value.request.return_value = mock_response

            result = account.update_configuration(suspend_trade=True)

            assert isinstance(result, AccountConfigModel)
            assert result.suspend_trade is True

            mock_requests.return_value.request.assert_called_once_with(
                "PATCH",
                f"{account.base_url}/account/configurations",
                headers=account.headers,
                json={"suspend_trade": True},
            )

    def test_update_configuration_multiple_params(self, account, mock_config_response):
        mock_config_response["no_shorting"] = True
        mock_config_response["trade_confirm_email"] = "none"

        with patch("py_alpaca_api.trading.account.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = json.dumps(mock_config_response)
            mock_requests.return_value.request.return_value = mock_response

            result = account.update_configuration(
                no_shorting=True, trade_confirm_email="none"
            )

            assert isinstance(result, AccountConfigModel)
            assert result.no_shorting is True
            assert result.trade_confirm_email == "none"

            mock_requests.return_value.request.assert_called_once_with(
                "PATCH",
                f"{account.base_url}/account/configurations",
                headers=account.headers,
                json={"no_shorting": True, "trade_confirm_email": "none"},
            )

    def test_update_configuration_all_params(self, account):
        updated_config = {
            "dtbp_check": "both",
            "fractional_trading": False,
            "max_margin_multiplier": "2",
            "no_shorting": True,
            "pdt_check": "exit",
            "ptp_no_exception_entry": True,
            "suspend_trade": True,
            "trade_confirm_email": "none",
        }

        with patch("py_alpaca_api.trading.account.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = json.dumps(updated_config)
            mock_requests.return_value.request.return_value = mock_response

            result = account.update_configuration(
                dtbp_check="both",
                fractional_trading=False,
                max_margin_multiplier="2",
                no_shorting=True,
                pdt_check="exit",
                ptp_no_exception_entry=True,
                suspend_trade=True,
                trade_confirm_email="none",
            )

            assert isinstance(result, AccountConfigModel)
            assert result.dtbp_check == "both"
            assert result.fractional_trading is False
            assert result.max_margin_multiplier == "2"
            assert result.no_shorting is True
            assert result.pdt_check == "exit"
            assert result.ptp_no_exception_entry is True
            assert result.suspend_trade is True
            assert result.trade_confirm_email == "none"

    def test_update_configuration_invalid_dtbp_check(self, account):
        with pytest.raises(ValueError, match="dtbp_check must be one of"):
            account.update_configuration(dtbp_check="invalid")

    def test_update_configuration_invalid_pdt_check(self, account):
        with pytest.raises(ValueError, match="pdt_check must be one of"):
            account.update_configuration(pdt_check="invalid")

    def test_update_configuration_invalid_margin_multiplier(self, account):
        with pytest.raises(ValueError, match="max_margin_multiplier must be one of"):
            account.update_configuration(max_margin_multiplier="3")

    def test_update_configuration_invalid_trade_confirm_email(self, account):
        with pytest.raises(ValueError, match="trade_confirm_email must be one of"):
            account.update_configuration(trade_confirm_email="some")

    def test_update_configuration_no_params(self, account):
        with pytest.raises(
            ValueError, match="At least one configuration parameter must be provided"
        ):
            account.update_configuration()

    def test_update_configuration_failure(self, account):
        with patch("py_alpaca_api.trading.account.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.text = "Bad Request"
            mock_requests.return_value.request.return_value = mock_response

            with pytest.raises(APIRequestError) as exc_info:
                account.update_configuration(suspend_trade=True)

            assert exc_info.value.status_code == 400
            assert "Failed to update account configuration" in str(exc_info.value)


class TestAccountConfigModel:
    def test_account_config_from_dict(self):
        data = {
            "dtbp_check": "both",
            "fractional_trading": True,
            "max_margin_multiplier": "2",
            "no_shorting": True,
            "pdt_check": "exit",
            "ptp_no_exception_entry": True,
            "suspend_trade": False,
            "trade_confirm_email": "none",
        }

        config = account_config_class_from_dict(data)

        assert isinstance(config, AccountConfigModel)
        assert config.dtbp_check == "both"
        assert config.fractional_trading is True
        assert config.max_margin_multiplier == "2"
        assert config.no_shorting is True
        assert config.pdt_check == "exit"
        assert config.ptp_no_exception_entry is True
        assert config.suspend_trade is False
        assert config.trade_confirm_email == "none"

    def test_account_config_from_dict_with_defaults(self):
        # Test with empty dict to verify defaults
        data = {}

        config = account_config_class_from_dict(data)

        assert isinstance(config, AccountConfigModel)
        assert config.dtbp_check == "entry"
        assert config.fractional_trading is False
        assert config.max_margin_multiplier == "1"
        assert config.no_shorting is False
        assert config.pdt_check == "entry"
        assert config.ptp_no_exception_entry is False
        assert config.suspend_trade is False
        assert config.trade_confirm_email == "all"

    def test_account_config_from_dict_partial(self):
        data = {
            "dtbp_check": "exit",
            "fractional_trading": True,
            "trade_confirm_email": "none",
        }

        config = account_config_class_from_dict(data)

        assert config.dtbp_check == "exit"
        assert config.fractional_trading is True
        assert config.trade_confirm_email == "none"
        # Check defaults for missing fields
        assert config.max_margin_multiplier == "1"
        assert config.no_shorting is False
        assert config.pdt_check == "entry"
