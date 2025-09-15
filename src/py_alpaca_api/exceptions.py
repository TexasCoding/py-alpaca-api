"""Custom exceptions for the py-alpaca-api library."""


class PyAlpacaAPIError(Exception):
    """Base exception for all py-alpaca-api errors."""

    pass


class AuthenticationError(PyAlpacaAPIError):
    """Raised when API authentication fails."""

    def __init__(self, message: str = "API Key and Secret are required"):
        self.message = message
        super().__init__(self.message)


class APIRequestError(PyAlpacaAPIError):
    """Raised when an API request fails."""

    def __init__(self, status_code: int | None = None, message: str = ""):
        self.status_code = status_code
        self.message = f"Request Error: {message}" if message else "Request Error"
        super().__init__(self.message)


class ValidationError(PyAlpacaAPIError):
    """Raised when input validation fails."""

    pass


class OrderError(PyAlpacaAPIError):
    """Raised when order operations fail."""

    pass


class PositionError(PyAlpacaAPIError):
    """Raised when position operations fail."""

    pass


class DataError(PyAlpacaAPIError):
    """Raised when data processing fails."""

    pass
