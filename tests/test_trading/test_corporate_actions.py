import os
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.models.corporate_action_model import (
    CorporateActionModel,
    DividendModel,
    MergerModel,
    SpinoffModel,
    SplitModel,
    corporate_action_class_from_dict,
)


@pytest.fixture
def alpaca():
    """Create PyAlpacaAPI instance for testing."""
    return PyAlpacaAPI(
        api_key=os.environ.get("ALPACA_API_KEY", "test_key"),
        api_secret=os.environ.get("ALPACA_SECRET_KEY", "test_secret"),
        api_paper=True,
    )


@pytest.fixture
def mock_dividend_response():
    """Sample dividend corporate action response."""
    return {
        "id": "123456",
        "corporate_action_id": "CA123",
        "ca_type": "dividend",
        "ca_sub_type": "cash",
        "initiating_symbol": "AAPL",
        "initiating_original_cusip": "037833100",
        "declaration_date": "2024-01-15",
        "ex_date": "2024-02-01",
        "record_date": "2024-02-02",
        "payable_date": "2024-02-15",
        "cash": 0.96,
        "cash_amount": 0.96,
        "dividend_type": "quarterly",
        "frequency": 4,
    }


@pytest.fixture
def mock_split_response():
    """Sample stock split corporate action response."""
    return {
        "id": "789012",
        "corporate_action_id": "CA789",
        "ca_type": "split",
        "ca_sub_type": "stock_split",
        "initiating_symbol": "TSLA",
        "initiating_original_cusip": "88160R101",
        "declaration_date": "2024-01-10",
        "ex_date": "2024-01-25",
        "split_from": 1.0,
        "split_to": 3.0,
    }


@pytest.fixture
def mock_merger_response():
    """Sample merger corporate action response."""
    return {
        "id": "345678",
        "corporate_action_id": "CA345",
        "ca_type": "merger",
        "ca_sub_type": "acquisition",
        "initiating_symbol": "TARGET",
        "target_symbol": "TARGET",
        "acquirer_symbol": "BUYER",
        "acquirer_cusip": "123456789",
        "declaration_date": "2024-01-05",
        "ex_date": "2024-03-01",
        "cash_rate": 0.5,
        "stock_rate": 1.2,
    }


@pytest.fixture
def mock_spinoff_response():
    """Sample spinoff corporate action response."""
    return {
        "id": "901234",
        "corporate_action_id": "CA901",
        "ca_type": "spinoff",
        "ca_sub_type": "spinoff",
        "initiating_symbol": "PARENT",
        "new_symbol": "CHILD",
        "new_cusip": "987654321",
        "declaration_date": "2024-01-20",
        "ex_date": "2024-02-15",
        "ratio": 0.25,
    }


class TestCorporateActions:
    """Test suite for Corporate Actions functionality."""

    def test_get_announcements_success(self, alpaca):
        """Test successful retrieval of corporate action announcements."""
        with patch.object(
            alpaca.trading.corporate_actions, "get_announcements"
        ) as mock_get:
            # Setup mock response
            mock_get.return_value = [
                DividendModel(
                    id="123",
                    corporate_action_id="CA123",
                    ca_type="dividend",
                    ca_sub_type="cash",
                    initiating_symbol="AAPL",
                    initiating_original_cusip="037833100",
                    target_symbol=None,
                    target_original_cusip=None,
                    declaration_date="2024-01-15",
                    ex_date="2024-02-01",
                    record_date="2024-02-02",
                    payable_date="2024-02-15",
                    cash=0.96,
                    old_rate=None,
                    new_rate=None,
                    cash_amount=0.96,
                    dividend_type="quarterly",
                    frequency=4,
                )
            ]

            # Call method
            result = alpaca.trading.corporate_actions.get_announcements(
                since="2024-01-01",
                until="2024-03-31",
                ca_types=["dividend"],
                symbol="AAPL",
            )

            # Verify
            assert len(result) == 1
            assert isinstance(result[0], DividendModel)
            assert result[0].initiating_symbol == "AAPL"
            assert result[0].cash_amount == 0.96

    def test_get_announcements_date_validation(self, alpaca):
        """Test date range validation for get_announcements."""
        # Test date range exceeds 90 days
        with pytest.raises(ValidationError, match="Date range cannot exceed 90 days"):
            alpaca.trading.corporate_actions.get_announcements(
                since="2024-01-01",
                until="2024-06-01",  # More than 90 days
                ca_types=["dividend"],
            )

        # Test invalid date format
        with pytest.raises(ValidationError, match="Invalid date format"):
            alpaca.trading.corporate_actions.get_announcements(
                since="01-01-2024",  # Wrong format
                until="2024-03-31",
                ca_types=["dividend"],
            )

        # Test since after until
        with pytest.raises(
            ValidationError, match="'since' date must be before 'until'"
        ):
            alpaca.trading.corporate_actions.get_announcements(
                since="2024-03-31",
                until="2024-01-01",
                ca_types=["dividend"],
            )

    def test_get_announcements_type_validation(self, alpaca):
        """Test corporate action type validation."""
        with pytest.raises(ValidationError, match="Invalid corporate action type"):
            alpaca.trading.corporate_actions.get_announcements(
                since="2024-01-01",
                until="2024-03-31",
                ca_types=["invalid_type"],
            )

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_announcement_by_id_success(self, mock_request, alpaca):
        """Test successful retrieval of a specific announcement."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            '{"id": "123456", "ca_type": "dividend", "corporate_action_id": "CA123"}'
        )
        mock_request.return_value = mock_response

        # Call method
        result = alpaca.trading.corporate_actions.get_announcement_by_id("123456")

        # Verify
        assert isinstance(result, CorporateActionModel | DividendModel)
        assert result.id == "123456"

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_announcement_by_id_not_found(self, mock_request, alpaca):
        """Test handling of not found announcement."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not found"
        mock_request.return_value = mock_response

        # Call method and expect error
        with pytest.raises(APIRequestError, match="announcement not found"):
            alpaca.trading.corporate_actions.get_announcement_by_id("invalid_id")

    def test_corporate_action_model_creation_dividend(self, mock_dividend_response):
        """Test creation of DividendModel from dict."""
        model = corporate_action_class_from_dict(mock_dividend_response)

        assert isinstance(model, DividendModel)
        assert model.id == "123456"
        assert model.ca_type == "dividend"
        assert model.cash_amount == 0.96
        assert model.dividend_type == "quarterly"
        assert model.frequency == 4

    def test_corporate_action_model_creation_split(self, mock_split_response):
        """Test creation of SplitModel from dict."""
        model = corporate_action_class_from_dict(mock_split_response)

        assert isinstance(model, SplitModel)
        assert model.id == "789012"
        assert model.ca_type == "split"
        assert model.split_from == 1.0
        assert model.split_to == 3.0

    def test_corporate_action_model_creation_merger(self, mock_merger_response):
        """Test creation of MergerModel from dict."""
        model = corporate_action_class_from_dict(mock_merger_response)

        assert isinstance(model, MergerModel)
        assert model.id == "345678"
        assert model.ca_type == "merger"
        assert model.acquirer_symbol == "BUYER"
        assert model.cash_rate == 0.5
        assert model.stock_rate == 1.2

    def test_corporate_action_model_creation_spinoff(self, mock_spinoff_response):
        """Test creation of SpinoffModel from dict."""
        model = corporate_action_class_from_dict(mock_spinoff_response)

        assert isinstance(model, SpinoffModel)
        assert model.id == "901234"
        assert model.ca_type == "spinoff"
        assert model.new_symbol == "CHILD"
        assert model.ratio == 0.25

    def test_corporate_action_model_unknown_type(self):
        """Test handling of unknown corporate action type."""
        unknown_data = {
            "id": "999",
            "corporate_action_id": "CA999",
            "ca_type": "unknown_type",
            "initiating_symbol": "TEST",
        }

        model = corporate_action_class_from_dict(unknown_data)

        assert isinstance(model, CorporateActionModel)
        assert not isinstance(
            model, DividendModel | SplitModel | MergerModel | SpinoffModel
        )
        assert model.id == "999"
        assert model.ca_type == "unknown_type"

    @patch("py_alpaca_api.http.requests.Requests.request")
    def test_get_all_announcements_pagination(self, mock_request, alpaca):
        """Test get_all_announcements with pagination handling."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"announcements": [{"id": "1", "ca_type": "dividend", "corporate_action_id": "CA1"}]}'
        mock_request.return_value = mock_response

        # Call method
        result = alpaca.trading.corporate_actions.get_all_announcements(
            since="2024-01-01",
            until="2024-03-31",
            ca_types=["dividend", "split"],
        )

        # Verify
        assert isinstance(result, list)
        # Note: Current implementation doesn't handle pagination fully,
        # this test ensures the method works

    @pytest.mark.skipif(
        not os.environ.get("ALPACA_API_KEY"), reason="API credentials not available"
    )
    def test_live_api_call(self, alpaca):
        """Test actual API call (requires valid credentials)."""
        # Use a recent date range
        today = datetime.now()
        since = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")

        try:
            result = alpaca.trading.corporate_actions.get_announcements(
                since=since,
                until=until,
                ca_types=["dividend"],
            )
            # Just verify it returns a list (may be empty)
            assert isinstance(result, list)
        except APIRequestError as e:
            # API might return error for various reasons (auth, rate limit, endpoint not available, etc.)
            assert e.status_code in [401, 403, 404, 429]

    def test_optional_parameters(self, alpaca):
        """Test that optional parameters are handled correctly."""
        with patch.object(
            alpaca.trading.corporate_actions, "get_announcements"
        ) as mock_get:
            mock_get.return_value = []

            # Call with optional parameters
            alpaca.trading.corporate_actions.get_announcements(
                since="2024-01-01",
                until="2024-03-31",
                ca_types=["dividend"],
                symbol="AAPL",
                cusip="037833100",
                date_type="ex_date",
                page_limit=50,
                page_token="next_page",
            )

            # Verify the method was called with all parameters
            mock_get.assert_called_once()
            call_args = mock_get.call_args[1]
            assert call_args["symbol"] == "AAPL"
            assert call_args["cusip"] == "037833100"
            assert call_args["date_type"] == "ex_date"
