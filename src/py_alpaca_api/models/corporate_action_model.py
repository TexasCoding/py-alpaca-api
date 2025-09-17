from dataclasses import dataclass
from typing import Any


@dataclass
class CorporateActionModel:
    """Base model for corporate action announcements."""

    id: str
    corporate_action_id: str
    ca_type: str
    ca_sub_type: str | None
    initiating_symbol: str | None
    initiating_original_cusip: str | None
    target_symbol: str | None
    target_original_cusip: str | None
    declaration_date: str | None
    ex_date: str | None
    record_date: str | None
    payable_date: str | None
    cash: float | None
    old_rate: float | None
    new_rate: float | None


@dataclass
class DividendModel(CorporateActionModel):
    """Model for dividend corporate actions."""

    cash_amount: float | None
    dividend_type: str | None
    frequency: int | None


@dataclass
class SplitModel(CorporateActionModel):
    """Model for stock split corporate actions."""

    split_from: float | None
    split_to: float | None


@dataclass
class MergerModel(CorporateActionModel):
    """Model for merger corporate actions."""

    acquirer_symbol: str | None
    acquirer_cusip: str | None
    cash_rate: float | None
    stock_rate: float | None


@dataclass
class SpinoffModel(CorporateActionModel):
    """Model for spinoff corporate actions."""

    new_symbol: str | None
    new_cusip: str | None
    ratio: float | None


def corporate_action_class_from_dict(data: dict[str, Any]) -> CorporateActionModel:
    """Create appropriate corporate action model from dictionary.

    Args:
        data: Dictionary containing corporate action data

    Returns:
        CorporateActionModel or one of its subclasses based on ca_type
    """
    ca_type = data.get("ca_type", "").lower()

    # Extract common fields
    base_fields = {
        "id": data.get("id", ""),
        "corporate_action_id": data.get("corporate_action_id", ""),
        "ca_type": data.get("ca_type", ""),
        "ca_sub_type": data.get("ca_sub_type"),
        "initiating_symbol": data.get("initiating_symbol"),
        "initiating_original_cusip": data.get("initiating_original_cusip"),
        "target_symbol": data.get("target_symbol"),
        "target_original_cusip": data.get("target_original_cusip"),
        "declaration_date": data.get("declaration_date"),
        "ex_date": data.get("ex_date"),
        "record_date": data.get("record_date"),
        "payable_date": data.get("payable_date"),
        "cash": data.get("cash"),
        "old_rate": data.get("old_rate"),
        "new_rate": data.get("new_rate"),
    }

    if ca_type == "dividend":
        return DividendModel(
            **base_fields,
            cash_amount=data.get("cash_amount"),
            dividend_type=data.get("dividend_type"),
            frequency=data.get("frequency"),
        )
    if ca_type == "split":
        return SplitModel(
            **base_fields,
            split_from=data.get("split_from"),
            split_to=data.get("split_to"),
        )
    if ca_type == "merger":
        return MergerModel(
            **base_fields,
            acquirer_symbol=data.get("acquirer_symbol"),
            acquirer_cusip=data.get("acquirer_cusip"),
            cash_rate=data.get("cash_rate"),
            stock_rate=data.get("stock_rate"),
        )
    if ca_type == "spinoff":
        return SpinoffModel(
            **base_fields,
            new_symbol=data.get("new_symbol"),
            new_cusip=data.get("new_cusip"),
            ratio=data.get("ratio"),
        )
    # Return base model for unknown types
    return CorporateActionModel(**base_fields)


def extract_corporate_action_data(data: dict[str, Any]) -> dict[str, Any]:
    """Extract and transform corporate action data from API response.

    Args:
        data: Raw API response data

    Returns:
        Transformed dictionary ready for model creation
    """
    # This function can handle any data transformation needed
    # between the API response and our model structure
    return data
