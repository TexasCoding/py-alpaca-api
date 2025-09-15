from dataclasses import dataclass


@dataclass
class AccountConfigModel:
    """Model for account configuration settings.

    Attributes:
        dtbp_check: Day trade buying power check setting ("entry", "exit", "both")
        fractional_trading: Whether fractional trading is enabled
        max_margin_multiplier: Maximum margin multiplier allowed ("1", "2", "4")
        no_shorting: Whether short selling is disabled
        pdt_check: Pattern day trader check setting ("entry", "exit", "both")
        ptp_no_exception_entry: Whether PTP no exception entry is enabled
        suspend_trade: Whether trading is suspended
        trade_confirm_email: Trade confirmation email setting ("all", "none")
    """

    dtbp_check: str
    fractional_trading: bool
    max_margin_multiplier: str
    no_shorting: bool
    pdt_check: str
    ptp_no_exception_entry: bool
    suspend_trade: bool
    trade_confirm_email: str


def account_config_class_from_dict(data: dict) -> AccountConfigModel:
    """Create AccountConfigModel from API response dictionary.

    Args:
        data: Dictionary containing account configuration data from API

    Returns:
        AccountConfigModel instance
    """
    return AccountConfigModel(
        dtbp_check=data.get("dtbp_check", "entry"),
        fractional_trading=data.get("fractional_trading", False),
        max_margin_multiplier=data.get("max_margin_multiplier", "1"),
        no_shorting=data.get("no_shorting", False),
        pdt_check=data.get("pdt_check", "entry"),
        ptp_no_exception_entry=data.get("ptp_no_exception_entry", False),
        suspend_trade=data.get("suspend_trade", False),
        trade_confirm_email=data.get("trade_confirm_email", "all"),
    )
