import os
import pytest

from py_alpaca_api.models.quote_model import QuoteModel


class TestLatestQuote:
    @pytest.fixture
    def latest_quote(self):
        from py_alpaca_api import PyAlpacaAPI

        api_key = os.environ.get("ALPACA_API_KEY")
        api_secret = os.environ.get("ALPACA_SECRET_KEY")
        quote_client = PyAlpacaAPI(
            api_key=api_key, api_secret=api_secret
        ).stock.latest_quote
        return quote_client

    def test_get_with_invalid_symbol(self, latest_quote):
        with pytest.raises(
            ValueError, match="Symbol is required. Must be a string or list of strings."
        ):
            latest_quote.get(symbol=None)

    def test_get_with_empty_string_symbol(self, latest_quote):
        with pytest.raises(
            ValueError, match="Symbol is required. Must be a string or list of strings."
        ):
            latest_quote.get(symbol="")

    def test_get_with_single_valid_symbol(self, latest_quote):
        quote = latest_quote.get(symbol="AAPL")
        assert isinstance(quote, QuoteModel)
        assert quote.symbol == "AAPL"

    def test_get_with_multiple_valid_symbols(self, latest_quote):
        quotes = latest_quote.get(symbol=["AAPL", "MSFT", "GOOG"])
        assert isinstance(quotes, list)
        assert len(quotes) == 3
        for quote in quotes:
            assert isinstance(quote, QuoteModel)

    def test_get_with_invalid_feed(self, latest_quote):
        with pytest.raises(ValueError, match="Invalid feed"):
            latest_quote.get(symbol="AAPL", feed="invalid_feed")
