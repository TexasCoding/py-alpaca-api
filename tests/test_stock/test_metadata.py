import json
from unittest.mock import MagicMock, patch

import pytest

from py_alpaca_api.exceptions import APIRequestError, ValidationError
from py_alpaca_api.stock.metadata import Metadata


class TestMetadata:
    @pytest.fixture
    def metadata(self):
        headers = {
            "APCA-API-KEY-ID": "test_key",
            "APCA-API-SECRET-KEY": "test_secret",
        }
        return Metadata(headers=headers)

    @pytest.fixture
    def mock_exchange_response(self):
        return {
            "A": "NYSE American (AMEX)",
            "B": "NASDAQ OMX BX",
            "C": "National Stock Exchange",
            "D": "FINRA ADF",
            "E": "Market Independent",
            "H": "MIAX",
            "I": "International Securities Exchange",
            "J": "Cboe EDGA",
            "K": "Cboe EDGX",
            "L": "Long Term Stock Exchange",
            "M": "Chicago Stock Exchange",
            "N": "New York Stock Exchange",
            "P": "NYSE Arca",
            "Q": "NASDAQ",
            "S": "NASDAQ Small Cap",
            "T": "NASDAQ Int",
            "U": "Members Exchange",
            "V": "IEX",
            "W": "CBOE",
            "X": "NASDAQ OMX PSX",
            "Y": "Cboe BYX",
            "Z": "Cboe BZX",
        }

    @pytest.fixture
    def mock_condition_response(self):
        return {
            "": "Regular Sale",
            "4": "Derivatively Priced",
            "5": "Market Center Reopening Trade",
            "6": "Market Center Closing Trade",
            "7": "Qualified Contingent Trade",
            "B": "Average Price Trade",
            "C": "Cash Sale",
            "E": "Automatic Execution",
            "F": "Intermarket Sweep",
            "H": "Price Variation Trade",
            "I": "Odd Lot Trade",
            "K": "Rule 127 NYSE",
            "L": "Sold Last",
            "M": "Market Center Official Close",
            "N": "Next Day",
            "O": "Market Center Opening Trade",
            "P": "Prior Reference Price",
            "Q": "Market Center Official Open",
            "R": "Seller",
            "S": "Split Trade",
            "T": "Form T",
            "U": "Extended Trading Hours",
            "V": "Contingent Trade",
            "W": "Average Price Trade",
            "X": "Cross/Periodic Auction Trade",
            "Y": "Yellow Flag Regular Trade",
            "Z": "Sold Out of Sequence",
        }

    def test_get_exchange_codes(self, metadata, mock_exchange_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_exchange_response)
            mock_requests.return_value.request.return_value = mock_response

            result = metadata.get_exchange_codes()

            assert isinstance(result, dict)
            assert len(result) == 22
            assert result["A"] == "NYSE American (AMEX)"
            assert result["Q"] == "NASDAQ"
            assert result["N"] == "New York Stock Exchange"
            assert result["V"] == "IEX"

            mock_requests.return_value.request.assert_called_once_with(
                method="GET",
                url=f"{metadata.base_url}/exchanges",
                headers=metadata.headers,
            )

    def test_get_exchange_codes_with_cache(self, metadata, mock_exchange_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_exchange_response)
            mock_requests.return_value.request.return_value = mock_response

            # First call should hit API
            result1 = metadata.get_exchange_codes()
            # Second call should use cache
            result2 = metadata.get_exchange_codes()

            assert result1 == result2
            # API should only be called once due to caching
            assert mock_requests.return_value.request.call_count == 1

    def test_get_exchange_codes_without_cache(self, metadata, mock_exchange_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_exchange_response)
            mock_requests.return_value.request.return_value = mock_response

            # First call
            metadata.get_exchange_codes()
            # Second call without cache
            metadata.get_exchange_codes(use_cache=False)

            # API should be called twice
            assert mock_requests.return_value.request.call_count == 2

    def test_get_exchange_codes_api_error(self, metadata):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_requests.return_value.request.side_effect = Exception("API Error")

            with pytest.raises(APIRequestError) as exc_info:
                metadata.get_exchange_codes()

            assert "Failed to get exchange codes" in str(exc_info.value)

    def test_get_condition_codes_trade(self, metadata, mock_condition_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_condition_response)
            mock_requests.return_value.request.return_value = mock_response

            result = metadata.get_condition_codes(ticktype="trade", tape="A")

            assert isinstance(result, dict)
            assert result[""] == "Regular Sale"
            assert result["4"] == "Derivatively Priced"
            assert result["F"] == "Intermarket Sweep"

            mock_requests.return_value.request.assert_called_once_with(
                method="GET",
                url=f"{metadata.base_url}/conditions/trade",
                headers=metadata.headers,
                params={"tape": "A"},
            )

    def test_get_condition_codes_quote(self, metadata):
        mock_quote_conditions = {
            "4": "On Demand Intra Day Auction",
            "A": "Slow Quote Offer Side",
            "B": "Slow Quote Bid Side",
            "C": "Exchange Specific Quote Condition",
            "D": "NASDAQ",
            "E": "Manual Ask Automated Bid",
            "F": "Manual Bid Automated Ask",
            "G": "Manual Bid And Ask",
            "H": "Fast Trading",
            "I": "Pending",
            "L": "Closed Quote",
            "O": "Opening Quote Automated",
            "R": "Regular Two Sided Open",
        }

        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_quote_conditions)
            mock_requests.return_value.request.return_value = mock_response

            result = metadata.get_condition_codes(ticktype="quote", tape="B")

            assert isinstance(result, dict)
            assert result["A"] == "Slow Quote Offer Side"
            assert result["B"] == "Slow Quote Bid Side"

            mock_requests.return_value.request.assert_called_once_with(
                method="GET",
                url=f"{metadata.base_url}/conditions/quote",
                headers=metadata.headers,
                params={"tape": "B"},
            )

    def test_get_condition_codes_invalid_ticktype(self, metadata):
        with pytest.raises(ValidationError, match="Invalid ticktype"):
            metadata.get_condition_codes(ticktype="invalid")

    def test_get_condition_codes_invalid_tape(self, metadata):
        with pytest.raises(ValidationError, match="Invalid tape"):
            metadata.get_condition_codes(tape="X")

    def test_get_condition_codes_with_cache(self, metadata, mock_condition_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_condition_response)
            mock_requests.return_value.request.return_value = mock_response

            # First call should hit API
            result1 = metadata.get_condition_codes(ticktype="trade", tape="A")
            # Second call should use cache
            result2 = metadata.get_condition_codes(ticktype="trade", tape="A")

            assert result1 == result2
            # API should only be called once due to caching
            assert mock_requests.return_value.request.call_count == 1

    def test_get_all_condition_codes(self, metadata):
        mock_conditions = {"": "Regular Sale", "4": "Derivatively Priced"}

        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_conditions)
            mock_requests.return_value.request.return_value = mock_response

            result = metadata.get_all_condition_codes()

            assert isinstance(result, dict)
            assert "trade" in result
            assert "quote" in result
            assert "A" in result["trade"]
            assert "B" in result["trade"]
            assert "C" in result["trade"]
            assert "A" in result["quote"]
            assert "B" in result["quote"]
            assert "C" in result["quote"]

            # Should call API 6 times (2 ticktypes * 3 tapes)
            assert mock_requests.return_value.request.call_count == 6

    def test_clear_cache(self, metadata, mock_exchange_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_exchange_response)
            mock_requests.return_value.request.return_value = mock_response

            # Load data into cache
            metadata.get_exchange_codes()
            assert metadata._exchange_cache is not None

            # Clear cache
            metadata.clear_cache()
            assert metadata._exchange_cache is None
            assert metadata._condition_cache == {}

    def test_lookup_exchange(self, metadata, mock_exchange_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_exchange_response)
            mock_requests.return_value.request.return_value = mock_response

            # Test valid code
            result = metadata.lookup_exchange("Q")
            assert result == "NASDAQ"

            # Test invalid code
            result = metadata.lookup_exchange("ZZ")
            assert result is None

    def test_lookup_condition(self, metadata, mock_condition_response):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = json.dumps(mock_condition_response)
            mock_requests.return_value.request.return_value = mock_response

            # Test valid code
            result = metadata.lookup_condition("F", ticktype="trade", tape="A")
            assert result == "Intermarket Sweep"

            # Test invalid code
            result = metadata.lookup_condition("ZZ", ticktype="trade", tape="A")
            assert result is None

    def test_get_condition_codes_api_error(self, metadata):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_requests.return_value.request.side_effect = Exception("API Error")

            with pytest.raises(APIRequestError) as exc_info:
                metadata.get_condition_codes()

            assert "Failed to get condition codes" in str(exc_info.value)

    def test_get_condition_codes_empty_response(self, metadata):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = "null"
            mock_requests.return_value.request.return_value = mock_response

            with pytest.raises(APIRequestError, match="No condition data returned"):
                metadata.get_condition_codes()

    def test_get_exchange_codes_empty_response(self, metadata):
        with patch("py_alpaca_api.stock.metadata.Requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.text = "{}"
            mock_requests.return_value.request.return_value = mock_response

            with pytest.raises(APIRequestError, match="No exchange data returned"):
                metadata.get_exchange_codes()
