import os

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.models.account_config_model import AccountConfigModel


@pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_SECRET_KEY"),
    reason="API credentials not set",
)
class TestAccountConfigIntegration:
    @pytest.fixture
    def alpaca(self):
        return PyAlpacaAPI(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            api_paper=True,
        )

    @pytest.fixture
    def original_config(self, alpaca):
        """Get the original configuration to restore after tests."""
        return alpaca.trading.account.get_configuration()

    def test_get_configuration(self, alpaca):
        config = alpaca.trading.account.get_configuration()

        assert isinstance(config, AccountConfigModel)
        # These fields should always be present
        assert config.dtbp_check in ["entry", "exit", "both"]
        assert isinstance(config.fractional_trading, bool)
        assert config.max_margin_multiplier in ["1", "2", "4"]
        assert isinstance(config.no_shorting, bool)
        assert config.pdt_check in ["entry", "exit", "both"]
        assert isinstance(config.ptp_no_exception_entry, bool)
        assert isinstance(config.suspend_trade, bool)
        assert config.trade_confirm_email in ["all", "none"]

    def test_update_single_configuration_param(self, alpaca, original_config):
        # Toggle trade confirmation email
        new_setting = "none" if original_config.trade_confirm_email == "all" else "all"

        updated_config = alpaca.trading.account.update_configuration(
            trade_confirm_email=new_setting
        )

        assert isinstance(updated_config, AccountConfigModel)
        assert updated_config.trade_confirm_email == new_setting

        # Verify other settings remain unchanged
        assert updated_config.dtbp_check == original_config.dtbp_check
        assert updated_config.fractional_trading == original_config.fractional_trading
        assert updated_config.no_shorting == original_config.no_shorting
        assert updated_config.pdt_check == original_config.pdt_check
        assert updated_config.suspend_trade == original_config.suspend_trade

        # Restore original setting
        alpaca.trading.account.update_configuration(
            trade_confirm_email=original_config.trade_confirm_email
        )

    def test_update_multiple_configuration_params(self, alpaca, original_config):
        # Toggle no_shorting and change pdt_check
        new_no_shorting = not original_config.no_shorting
        new_pdt_check = "exit" if original_config.pdt_check == "entry" else "entry"

        updated_config = alpaca.trading.account.update_configuration(
            no_shorting=new_no_shorting, pdt_check=new_pdt_check
        )

        assert isinstance(updated_config, AccountConfigModel)
        assert updated_config.no_shorting == new_no_shorting
        assert updated_config.pdt_check == new_pdt_check

        # Verify other settings remain unchanged
        assert updated_config.dtbp_check == original_config.dtbp_check
        assert updated_config.fractional_trading == original_config.fractional_trading
        assert (
            updated_config.max_margin_multiplier
            == original_config.max_margin_multiplier
        )
        assert updated_config.suspend_trade == original_config.suspend_trade
        assert updated_config.trade_confirm_email == original_config.trade_confirm_email

        # Restore original settings
        alpaca.trading.account.update_configuration(
            no_shorting=original_config.no_shorting,
            pdt_check=original_config.pdt_check,
        )

    def test_update_margin_multiplier(self, alpaca, original_config):
        # Test changing margin multiplier
        current_multiplier = original_config.max_margin_multiplier
        new_multiplier = "2" if current_multiplier != "2" else "4"

        updated_config = alpaca.trading.account.update_configuration(
            max_margin_multiplier=new_multiplier
        )

        assert updated_config.max_margin_multiplier == new_multiplier

        # Restore original
        alpaca.trading.account.update_configuration(
            max_margin_multiplier=original_config.max_margin_multiplier
        )

    def test_update_dtbp_check(self, alpaca, original_config):
        # Cycle through dtbp_check options
        options = ["entry", "exit", "both"]
        current = original_config.dtbp_check
        new_value = options[(options.index(current) + 1) % 3]

        updated_config = alpaca.trading.account.update_configuration(
            dtbp_check=new_value
        )

        assert updated_config.dtbp_check == new_value

        # Restore original
        alpaca.trading.account.update_configuration(
            dtbp_check=original_config.dtbp_check
        )

    def test_toggle_fractional_trading(self, alpaca, original_config):
        # Toggle fractional trading
        new_value = not original_config.fractional_trading

        updated_config = alpaca.trading.account.update_configuration(
            fractional_trading=new_value
        )

        assert updated_config.fractional_trading == new_value

        # Restore original
        alpaca.trading.account.update_configuration(
            fractional_trading=original_config.fractional_trading
        )

    def test_configuration_persistence(self, alpaca, original_config):
        # Update a configuration
        new_email_setting = (
            "none" if original_config.trade_confirm_email == "all" else "all"
        )
        alpaca.trading.account.update_configuration(
            trade_confirm_email=new_email_setting
        )

        # Get configuration again to verify persistence
        config = alpaca.trading.account.get_configuration()
        assert config.trade_confirm_email == new_email_setting

        # Restore original
        alpaca.trading.account.update_configuration(
            trade_confirm_email=original_config.trade_confirm_email
        )

    def test_invalid_parameter_handling(self, alpaca):
        # Test that invalid parameters raise appropriate errors
        with pytest.raises(ValueError):
            alpaca.trading.account.update_configuration(dtbp_check="invalid")

        with pytest.raises(ValueError):
            alpaca.trading.account.update_configuration(pdt_check="invalid")

        with pytest.raises(ValueError):
            alpaca.trading.account.update_configuration(max_margin_multiplier="5")

        with pytest.raises(ValueError):
            alpaca.trading.account.update_configuration(trade_confirm_email="sometimes")

    @pytest.mark.skip(reason="Suspend trade affects account functionality")
    def test_suspend_trade_toggle(self, alpaca, original_config):
        # This test is skipped as it would actually suspend trading
        # Only run manually when testing this specific feature
        updated_config = alpaca.trading.account.update_configuration(suspend_trade=True)
        assert updated_config.suspend_trade is True

        # Immediately restore
        alpaca.trading.account.update_configuration(
            suspend_trade=original_config.suspend_trade
        )
