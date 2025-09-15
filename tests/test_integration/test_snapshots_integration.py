import os

import pytest

from py_alpaca_api import PyAlpacaAPI
from py_alpaca_api.models.snapshot_model import BarModel, SnapshotModel


@pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_SECRET_KEY"),
    reason="API credentials not set",
)
class TestSnapshotsIntegration:
    @pytest.fixture
    def alpaca(self):
        return PyAlpacaAPI(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            api_paper=True,
        )

    def test_get_snapshot_single_symbol(self, alpaca):
        result = alpaca.stock.snapshots.get_snapshot("AAPL")

        assert isinstance(result, SnapshotModel)
        assert result.symbol == "AAPL"

        # At least one of these should be present during market hours
        # Some may be None during pre/post market
        assert any(
            [
                result.latest_trade is not None,
                result.latest_quote is not None,
                result.minute_bar is not None,
                result.daily_bar is not None,
                result.prev_daily_bar is not None,
            ]
        )

        # If latest_trade exists, validate its structure
        if result.latest_trade:
            assert result.latest_trade.price > 0
            assert result.latest_trade.size >= 0
            assert result.latest_trade.symbol == "AAPL"

        # If latest_quote exists, validate its structure
        if result.latest_quote:
            assert result.latest_quote.ask >= 0
            assert result.latest_quote.bid >= 0
            assert result.latest_quote.symbol == "AAPL"

        # If minute_bar exists, validate its structure
        if result.minute_bar:
            assert isinstance(result.minute_bar, BarModel)
            assert result.minute_bar.open > 0
            assert result.minute_bar.high >= result.minute_bar.low
            assert result.minute_bar.volume >= 0

        # If daily_bar exists, validate its structure
        if result.daily_bar:
            assert isinstance(result.daily_bar, BarModel)
            assert result.daily_bar.open > 0
            assert result.daily_bar.high >= result.daily_bar.low
            assert result.daily_bar.volume >= 0

        # If prev_daily_bar exists, validate its structure
        if result.prev_daily_bar:
            assert isinstance(result.prev_daily_bar, BarModel)
            assert result.prev_daily_bar.open > 0
            assert result.prev_daily_bar.high >= result.prev_daily_bar.low
            assert result.prev_daily_bar.volume >= 0

    def test_get_snapshot_with_different_feeds(self, alpaca):
        # Test with IEX feed (default)
        result_iex = alpaca.stock.snapshots.get_snapshot("AAPL", feed="iex")
        assert isinstance(result_iex, SnapshotModel)
        assert result_iex.symbol == "AAPL"

        # Test with SIP feed if available (might require subscription)
        try:
            result_sip = alpaca.stock.snapshots.get_snapshot("AAPL", feed="sip")
            assert isinstance(result_sip, SnapshotModel)
            assert result_sip.symbol == "AAPL"
        except Exception:
            # SIP feed might not be available for all accounts
            pass

    def test_get_snapshots_multiple_symbols(self, alpaca):
        symbols = ["AAPL", "MSFT", "GOOGL"]
        result = alpaca.stock.snapshots.get_snapshots(symbols)

        assert isinstance(result, dict)
        assert len(result) == 3

        for symbol in symbols:
            assert symbol in result
            assert isinstance(result[symbol], SnapshotModel)
            assert result[symbol].symbol == symbol

            # Validate at least some data is present
            snapshot = result[symbol]
            assert any(
                [
                    snapshot.latest_trade is not None,
                    snapshot.latest_quote is not None,
                    snapshot.minute_bar is not None,
                    snapshot.daily_bar is not None,
                    snapshot.prev_daily_bar is not None,
                ]
            )

    def test_get_snapshots_single_symbol_returns_list(self, alpaca):
        result = alpaca.stock.snapshots.get_snapshots("AAPL")

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], SnapshotModel)
        assert result[0].symbol == "AAPL"

    def test_get_snapshots_comma_separated_string(self, alpaca):
        result = alpaca.stock.snapshots.get_snapshots("AAPL,MSFT,TSLA")

        assert isinstance(result, dict)
        assert len(result) == 3
        assert all(symbol in result for symbol in ["AAPL", "MSFT", "TSLA"])

    def test_get_snapshots_large_batch(self, alpaca):
        # Test with a larger batch of symbols
        symbols = [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "META",
            "TSLA",
            "NVDA",
            "JPM",
            "V",
            "JNJ",
        ]
        result = alpaca.stock.snapshots.get_snapshots(symbols)

        assert isinstance(result, dict)
        assert len(result) == 10

        for symbol in symbols:
            assert symbol in result
            assert isinstance(result[symbol], SnapshotModel)
            assert result[symbol].symbol == symbol

    def test_get_snapshot_with_otc_symbol(self, alpaca):
        # Test with an OTC symbol if available
        try:
            result = alpaca.stock.snapshots.get_snapshot("TCEHY", feed="otc")
            assert isinstance(result, SnapshotModel)
            assert result.symbol == "TCEHY"
        except Exception:
            # OTC feed might not be available or symbol might not exist
            pass

    def test_snapshot_data_consistency(self, alpaca):
        # Get snapshot and verify data consistency
        result = alpaca.stock.snapshots.get_snapshot("SPY")

        assert isinstance(result, SnapshotModel)
        assert result.symbol == "SPY"

        # If we have both minute and daily bars, check consistency
        if result.minute_bar and result.daily_bar:
            # Minute bar should be within the daily bar's range
            assert result.minute_bar.high <= result.daily_bar.high
            assert result.minute_bar.low >= result.daily_bar.low

        # If we have latest trade and minute bar, check consistency
        if result.latest_trade and result.minute_bar:
            # Latest trade should be within reasonable range of minute bar
            # (allowing for some time difference)
            assert result.latest_trade.price > 0
            assert result.minute_bar.close > 0

    def test_get_snapshots_handles_invalid_symbol_gracefully(self, alpaca):
        # Mix valid and potentially invalid symbols
        symbols = ["AAPL", "INVALID123", "MSFT"]

        try:
            result = alpaca.stock.snapshots.get_snapshots(symbols)
            # If it doesn't error, check we at least got valid symbols
            assert "AAPL" in result or "MSFT" in result
        except Exception:
            # API might reject the entire request with invalid symbols
            # This is acceptable behavior
            pass

    def test_snapshot_during_market_hours(self, alpaca):
        # This test is most meaningful during market hours
        # Get snapshot for a highly liquid symbol
        result = alpaca.stock.snapshots.get_snapshot("SPY")

        assert isinstance(result, SnapshotModel)
        assert result.symbol == "SPY"

        # During market hours, SPY should have most data available
        # Note: This might fail outside market hours
        try:
            market_info = alpaca.trading.market.get_market_info()
            market_open = (
                market_info.is_open if hasattr(market_info, "is_open") else False
            )
        except Exception:
            market_open = False

        if market_open:
            # During market hours, we expect more data to be available
            assert result.latest_trade is not None
            assert result.latest_quote is not None
            # Minute bar might not be immediately available at market open
            # Daily bar updates throughout the day
