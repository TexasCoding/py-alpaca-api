import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from py_alpaca_api.http.requests import Requests
from py_alpaca_api.models.quote_model import QuoteModel, quote_class_from_dict


class LatestQuote:
    BATCH_SIZE = 200  # Alpaca API limit for multi-symbol requests

    def __init__(self, headers: dict[str, str]) -> None:
        self.headers = headers

    def get(
        self,
        symbol: list[str] | str | None,
        feed: str = "iex",
        currency: str = "USD",
    ) -> list[QuoteModel] | QuoteModel:
        """Get latest quotes for one or more symbols.

        Args:
            symbol: A string or list of strings representing the stock symbol(s).
            feed: The data feed source. Default is "iex".
            currency: The currency for the quotes. Default is "USD".

        Returns:
            A single QuoteModel or list of QuoteModel objects.

        Raises:
            ValueError: If symbol is None/empty or if feed is invalid.
        """
        if symbol is None or symbol == "":
            raise ValueError("Symbol is required. Must be a string or list of strings.")

        valid_feeds = ["iex", "sip", "otc"]
        if feed not in valid_feeds:
            raise ValueError("Invalid feed, must be one of: 'iex', 'sip', 'otc'")

        # Handle single vs multiple symbols
        is_single = isinstance(symbol, str)
        if is_single:
            assert isinstance(symbol, str)  # Type guard for mypy
            symbols = [symbol.upper().strip()]
        else:
            assert isinstance(symbol, list)  # Type guard for mypy
            symbols = [s.upper().strip() for s in symbol]

        # If more than BATCH_SIZE symbols, need to batch the requests
        if len(symbols) > self.BATCH_SIZE:
            quotes = self._get_batched_quotes(symbols, feed, currency)
        else:
            quotes = self._fetch_quotes(symbols, feed, currency)

        # Return single quote if single symbol requested
        if is_single and quotes:
            return quotes[0]
        return quotes

    def _fetch_quotes(
        self, symbols: list[str], feed: str, currency: str
    ) -> list[QuoteModel]:
        """Fetch quotes for a list of symbols.

        Args:
            symbols: List of stock symbols.
            feed: The data feed source.
            currency: The currency for the quotes.

        Returns:
            List of QuoteModel objects.
        """
        url = "https://data.alpaca.markets/v2/stocks/quotes/latest"
        symbols_str = ",".join(symbols)

        params: dict[str, str | bool | float | int] = {
            "symbols": symbols_str,
            "feed": feed,
            "currency": currency,
        }

        response = json.loads(
            Requests()
            .request(method="GET", url=url, headers=self.headers, params=params)
            .text
        )

        quotes = []
        for key, value in response.get("quotes", {}).items():
            quotes.append(
                quote_class_from_dict(
                    {
                        "symbol": key,
                        "timestamp": value["t"],
                        "ask": value["ap"],
                        "ask_size": value["as"],
                        "bid": value["bp"],
                        "bid_size": value["bs"],
                    }
                )
            )

        return quotes

    def _get_batched_quotes(
        self, symbols: list[str], feed: str, currency: str
    ) -> list[QuoteModel]:
        """Handle large symbol lists by batching requests.

        Args:
            symbols: List of stock symbols.
            feed: The data feed source.
            currency: The currency for the quotes.

        Returns:
            List of QuoteModel objects.
        """
        # Split symbols into batches
        batches = [
            symbols[i : i + self.BATCH_SIZE]
            for i in range(0, len(symbols), self.BATCH_SIZE)
        ]

        # Use ThreadPoolExecutor for concurrent batch requests
        all_quotes = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for batch in batches:
                future = executor.submit(self._fetch_quotes, batch, feed, currency)
                futures.append(future)

            for future in as_completed(futures):
                try:
                    quotes = future.result()
                    all_quotes.extend(quotes)
                except Exception as e:
                    # Log error but continue with other batches
                    print(f"Error fetching batch: {e}")

        return all_quotes
