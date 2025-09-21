"""Test cases for company logos functionality."""

import base64
from unittest.mock import MagicMock, mock_open, patch

import pytest

from py_alpaca_api.exceptions import ValidationError
from py_alpaca_api.stock.logos import Logos


class TestLogos:
    """Test suite for the Logos class."""

    @pytest.fixture
    def logos_instance(self):
        """Create a Logos instance for testing."""
        return Logos(headers={"Authorization": "Bearer TEST"})

    def test_get_logo_single_symbol(self, logos_instance, mocker):
        """Test getting logo for a single symbol."""
        # Mock response with binary data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"\x89PNG\r\n\x1a\n"  # PNG file header

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = mock_response

        # Call the method
        result = logos_instance.get_logo("AAPL")

        # Assertions
        assert isinstance(result, bytes)
        assert result == b"\x89PNG\r\n\x1a\n"

        # Verify API call
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert call_args[1]["method"] == "GET"
        assert "logos/AAPL" in call_args[1]["url"]
        assert call_args[1]["raw_response"] is True

    def test_get_logo_with_placeholder(self, logos_instance, mocker):
        """Test getting logo with placeholder option."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"placeholder_image_data"

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = mock_response

        # Call with placeholder
        result = logos_instance.get_logo("AAPL", placeholder=True)

        # Assertions
        assert isinstance(result, bytes)
        assert result == b"placeholder_image_data"

        # Check that placeholder parameter was passed
        call_args = mock_request.call_args
        assert call_args[1]["params"]["placeholder"] == "true"

    def test_get_logo_not_found(self, logos_instance, mocker):
        """Test handling when logo is not found."""
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = mock_response

        # Call the method and expect exception
        with pytest.raises(Exception, match="Logo not found for symbol: INVALID"):
            logos_instance.get_logo("INVALID")

    def test_get_logo_server_error(self, logos_instance, mocker):
        """Test handling server errors."""
        # Mock 500 response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = mock_response

        # Call the method and expect exception
        with pytest.raises(Exception, match="Failed to retrieve logo: 500"):
            logos_instance.get_logo("AAPL")

    def test_get_logo_invalid_symbol(self, logos_instance):
        """Test that invalid symbol raises ValidationError."""
        with pytest.raises(ValidationError, match="Symbol must be a non-empty string"):
            logos_instance.get_logo("")

        with pytest.raises(ValidationError, match="Symbol must be a non-empty string"):
            logos_instance.get_logo(None)  # type: ignore

    def test_get_logo_url(self, logos_instance):
        """Test getting the URL for a logo."""
        # Test basic URL
        url = logos_instance.get_logo_url("AAPL")
        assert url == "https://data.alpaca.markets/v1beta1/logos/AAPL"

        # Test with placeholder
        url_with_placeholder = logos_instance.get_logo_url("AAPL", placeholder=True)
        assert (
            url_with_placeholder
            == "https://data.alpaca.markets/v1beta1/logos/AAPL?placeholder=true"
        )

    def test_get_logo_url_invalid_symbol(self, logos_instance):
        """Test that invalid symbol raises ValidationError for URL method."""
        with pytest.raises(ValidationError, match="Symbol must be a non-empty string"):
            logos_instance.get_logo_url("")

    def test_save_logo(self, logos_instance, mocker):
        """Test saving a logo to a file."""
        # Mock logo data
        logo_data = b"\x89PNG\r\n\x1a\n"

        # Mock get_logo to return our test data
        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.return_value = logo_data

        # Mock file operations
        m = mock_open()
        with patch("pathlib.Path.open", m):
            logos_instance.save_logo("AAPL", "/tmp/aapl_logo.png")

        # Verify get_logo was called
        mock_get_logo.assert_called_once_with("AAPL", placeholder=False)

        # Verify file was opened and written
        m.assert_called_once_with("wb")
        m().write.assert_called_once_with(logo_data)

    def test_save_logo_with_placeholder(self, logos_instance, mocker):
        """Test saving a logo with placeholder option."""
        # Mock logo data
        logo_data = b"placeholder_image"

        # Mock get_logo to return placeholder data
        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.return_value = logo_data

        # Mock file operations
        m = mock_open()
        with patch("pathlib.Path.open", m):
            logos_instance.save_logo("AAPL", "/tmp/aapl_logo.png", placeholder=True)

        # Verify get_logo was called with placeholder
        mock_get_logo.assert_called_once_with("AAPL", placeholder=True)

    def test_save_logo_invalid_filepath(self, logos_instance):
        """Test that invalid filepath raises ValidationError."""
        with pytest.raises(
            ValidationError, match="Filepath must be a non-empty string"
        ):
            logos_instance.save_logo("AAPL", "")

        with pytest.raises(
            ValidationError, match="Filepath must be a non-empty string"
        ):
            logos_instance.save_logo("AAPL", None)  # type: ignore

    def test_save_logo_file_write_error(self, logos_instance, mocker):
        """Test handling file write errors."""
        # Mock get_logo to return data
        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.return_value = b"logo_data"

        # Mock file open to raise exception
        with (
            patch("pathlib.Path.open", side_effect=OSError("Permission denied")),
            pytest.raises(Exception, match="Failed to save logo to"),
        ):
            logos_instance.save_logo("AAPL", "/invalid/path/logo.png")

    def test_get_logo_base64(self, logos_instance, mocker):
        """Test getting logo as base64 encoded string."""
        # Mock logo data
        logo_data = b"\x89PNG\r\n\x1a\n"

        # Mock get_logo
        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.return_value = logo_data

        # Call the method
        result = logos_instance.get_logo_base64("AAPL")

        # Verify result is base64 encoded
        assert isinstance(result, str)
        assert result == base64.b64encode(logo_data).decode("utf-8")

        # Verify get_logo was called
        mock_get_logo.assert_called_once_with("AAPL", placeholder=False)

    def test_get_logo_base64_with_placeholder(self, logos_instance, mocker):
        """Test getting logo as base64 with placeholder."""
        # Mock logo data
        logo_data = b"placeholder"

        # Mock get_logo
        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.return_value = logo_data

        # Call with placeholder
        result = logos_instance.get_logo_base64("AAPL", placeholder=True)

        # Verify result
        assert result == base64.b64encode(logo_data).decode("utf-8")
        mock_get_logo.assert_called_once_with("AAPL", placeholder=True)

    def test_get_multiple_logos(self, logos_instance, mocker):
        """Test getting logos for multiple symbols."""

        # Mock get_logo to return different data for each symbol
        def mock_get_logo_side_effect(symbol, placeholder=False):
            if symbol == "AAPL":
                return b"apple_logo"
            if symbol == "MSFT":
                return b"microsoft_logo"
            if symbol == "INVALID":
                raise Exception("Logo not found")
            return b"default_logo"

        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.side_effect = mock_get_logo_side_effect

        # Call the method
        result = logos_instance.get_multiple_logos(["AAPL", "MSFT", "INVALID"])

        # Assertions
        assert isinstance(result, dict)
        assert len(result) == 3
        assert result["AAPL"] == b"apple_logo"
        assert result["MSFT"] == b"microsoft_logo"
        assert result["INVALID"] is None  # Failed to get logo, no placeholder

    def test_get_multiple_logos_with_placeholder(self, logos_instance, mocker):
        """Test getting multiple logos with placeholder for missing ones."""
        # Mock get_logo
        call_count = 0

        def mock_get_logo_side_effect(symbol, placeholder=False):
            nonlocal call_count
            call_count += 1
            if symbol == "INVALID" and not placeholder:
                raise Exception("Logo not found")
            if symbol == "INVALID" and placeholder:
                return b"placeholder_logo"
            return f"{symbol}_logo".encode()

        mock_get_logo = mocker.patch.object(logos_instance, "get_logo")
        mock_get_logo.side_effect = mock_get_logo_side_effect

        # Call with placeholder
        result = logos_instance.get_multiple_logos(
            ["AAPL", "INVALID"], placeholder=True
        )

        # Assertions
        assert result["AAPL"] == b"AAPL_logo"
        assert result["INVALID"] == b"placeholder_logo"

    def test_get_multiple_logos_empty_symbols(self, logos_instance):
        """Test that empty symbols list raises ValidationError."""
        with pytest.raises(ValidationError, match="Symbols must be a non-empty list"):
            logos_instance.get_multiple_logos([])

        with pytest.raises(ValidationError, match="Symbols must be a non-empty list"):
            logos_instance.get_multiple_logos(None)  # type: ignore

    def test_get_multiple_logos_invalid_list(self, logos_instance):
        """Test that non-list input raises ValidationError."""
        with pytest.raises(ValidationError, match="Symbols must be a non-empty list"):
            logos_instance.get_multiple_logos("AAPL")  # type: ignore

    def test_symbol_uppercase_conversion(self, logos_instance, mocker):
        """Test that symbols are converted to uppercase."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"logo_data"

        # Mock the Requests call
        mock_request = mocker.patch("py_alpaca_api.http.requests.Requests.request")
        mock_request.return_value = mock_response

        # Call with lowercase symbol
        logos_instance.get_logo("aapl")

        # Verify uppercase symbol was used in URL
        call_args = mock_request.call_args
        assert "logos/AAPL" in call_args[1]["url"]
