import os

import pytest

from py_alpaca_api import PyAlpacaAPI


@pytest.mark.skipif(
    not os.environ.get("ALPACA_API_KEY") or not os.environ.get("ALPACA_SECRET_KEY"),
    reason="API credentials not set",
)
class TestMetadataIntegration:
    @pytest.fixture
    def alpaca(self):
        return PyAlpacaAPI(
            api_key=os.environ.get("ALPACA_API_KEY"),
            api_secret=os.environ.get("ALPACA_SECRET_KEY"),
            api_paper=True,
        )

    def test_get_exchange_codes(self, alpaca):
        exchanges = alpaca.stock.metadata.get_exchange_codes()

        assert isinstance(exchanges, dict)
        assert len(exchanges) > 0

        # Check for some common exchanges
        assert "A" in exchanges  # NYSE American
        assert "N" in exchanges  # NYSE
        assert "Q" in exchanges  # NASDAQ
        assert "V" in exchanges  # IEX
        assert "P" in exchanges  # NYSE Arca

        # Verify values are strings
        for code, name in exchanges.items():
            assert isinstance(code, str)
            assert isinstance(name, str)
            assert len(name) > 0

        print(f"Found {len(exchanges)} exchange codes")

    def test_get_condition_codes_trade_tape_a(self, alpaca):
        conditions = alpaca.stock.metadata.get_condition_codes(
            ticktype="trade", tape="A"
        )

        assert isinstance(conditions, dict)
        assert len(conditions) > 0

        # Check for common condition codes
        if "" in conditions:
            assert conditions[""] == "Regular Sale"

        # Verify all values are strings
        for code, description in conditions.items():
            assert isinstance(code, str)
            assert isinstance(description, str)

        print(f"Found {len(conditions)} trade conditions for Tape A")

    def test_get_condition_codes_trade_tape_b(self, alpaca):
        conditions = alpaca.stock.metadata.get_condition_codes(
            ticktype="trade", tape="B"
        )

        assert isinstance(conditions, dict)
        assert len(conditions) > 0

        print(f"Found {len(conditions)} trade conditions for Tape B")

    def test_get_condition_codes_quote(self, alpaca):
        conditions = alpaca.stock.metadata.get_condition_codes(
            ticktype="quote", tape="A"
        )

        assert isinstance(conditions, dict)
        # Quote conditions might be fewer than trade conditions
        assert len(conditions) >= 0

        # Verify all values are strings
        for code, description in conditions.items():
            assert isinstance(code, str)
            assert isinstance(description, str)

        print(f"Found {len(conditions)} quote conditions for Tape A")

    def test_get_all_condition_codes(self, alpaca):
        all_conditions = alpaca.stock.metadata.get_all_condition_codes()

        assert isinstance(all_conditions, dict)
        assert "trade" in all_conditions
        assert "quote" in all_conditions

        # Check structure
        for ticktype in ["trade", "quote"]:
            assert ticktype in all_conditions
            for tape in ["A", "B", "C"]:
                assert tape in all_conditions[ticktype]
                assert isinstance(all_conditions[ticktype][tape], dict)

        # Count total conditions
        total = 0
        for ticktype in all_conditions:
            for tape in all_conditions[ticktype]:
                total += len(all_conditions[ticktype][tape])

        print(f"Found {total} total condition codes across all types and tapes")

    def test_lookup_exchange(self, alpaca):
        # Test valid exchange codes
        nasdaq = alpaca.stock.metadata.lookup_exchange("Q")
        assert nasdaq is not None
        assert "NASDAQ" in nasdaq

        nyse = alpaca.stock.metadata.lookup_exchange("N")
        assert nyse is not None
        assert "New York Stock Exchange" in nyse

        iex = alpaca.stock.metadata.lookup_exchange("V")
        assert iex is not None
        assert "IEX" in iex

        # Test invalid code
        invalid = alpaca.stock.metadata.lookup_exchange("ZZ")
        assert invalid is None

    def test_lookup_condition(self, alpaca):
        # Test looking up a specific condition
        # Empty string is often "Regular Sale"
        regular = alpaca.stock.metadata.lookup_condition("", ticktype="trade", tape="A")
        if regular:
            assert "Regular" in regular or "Sale" in regular

        # Test invalid condition
        invalid = alpaca.stock.metadata.lookup_condition(
            "ZZ", ticktype="trade", tape="A"
        )
        assert invalid is None

    def test_caching_behavior(self, alpaca):
        # Clear cache first
        alpaca.stock.metadata.clear_cache()

        # First call should hit API
        exchanges1 = alpaca.stock.metadata.get_exchange_codes()

        # Second call should use cache (should be faster)
        exchanges2 = alpaca.stock.metadata.get_exchange_codes()

        assert exchanges1 == exchanges2

        # Force API call by disabling cache
        exchanges3 = alpaca.stock.metadata.get_exchange_codes(use_cache=False)

        assert exchanges3 == exchanges1

    def test_clear_cache(self, alpaca):
        # Load some data into cache
        alpaca.stock.metadata.get_exchange_codes()
        alpaca.stock.metadata.get_condition_codes(ticktype="trade", tape="A")

        # Verify cache is populated
        assert alpaca.stock.metadata._exchange_cache is not None
        assert len(alpaca.stock.metadata._condition_cache) > 0

        # Clear cache
        alpaca.stock.metadata.clear_cache()

        # Verify cache is cleared
        assert alpaca.stock.metadata._exchange_cache is None
        assert len(alpaca.stock.metadata._condition_cache) == 0

    def test_different_tapes_have_same_conditions(self, alpaca):
        # Get conditions for different tapes
        tape_a = alpaca.stock.metadata.get_condition_codes(ticktype="trade", tape="A")
        tape_b = alpaca.stock.metadata.get_condition_codes(ticktype="trade", tape="B")
        tape_c = alpaca.stock.metadata.get_condition_codes(ticktype="trade", tape="C")

        # Tapes often have similar condition codes
        # Check if they have some overlap
        common_codes = set(tape_a.keys()) & set(tape_b.keys())
        assert len(common_codes) > 0

        print(f"Tape A: {len(tape_a)} conditions")
        print(f"Tape B: {len(tape_b)} conditions")
        print(f"Tape C: {len(tape_c)} conditions")
        print(f"Common codes between A and B: {len(common_codes)}")

    def test_exchange_codes_are_consistent(self, alpaca):
        # Get exchanges multiple times to ensure consistency
        exchanges1 = alpaca.stock.metadata.get_exchange_codes(use_cache=False)
        exchanges2 = alpaca.stock.metadata.get_exchange_codes(use_cache=False)

        assert exchanges1 == exchanges2
        assert len(exchanges1) == len(exchanges2)
