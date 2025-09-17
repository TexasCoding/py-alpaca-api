"""Global test configuration and fixtures."""

import os
import time

import pytest


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "ci_skip: mark test to skip in CI environment")
    config.addinivalue_line(
        "markers", "rate_limited: mark test as rate limited (adds delays in CI)"
    )


@pytest.fixture(scope="session")
def is_ci():
    """Check if tests are running in CI environment."""
    return os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true"


@pytest.fixture(autouse=True)
def handle_rate_limits(request, is_ci):
    """Add delays for rate-limited tests when running in CI."""
    if is_ci:
        # Check if test is marked as rate_limited
        if request.node.get_closest_marker("rate_limited"):
            # Add delay before test
            time.sleep(2)
            yield
            # Add delay after test
            time.sleep(1)
        else:
            # Small delay for all tests in CI to avoid rate limits
            time.sleep(0.5)
            yield
    else:
        yield


def pytest_collection_modifyitems(config, items):
    """Skip CI-specific tests."""
    if os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true":
        skip_ci = pytest.mark.skip(reason="Skipped in CI due to rate limits")
        for item in items:
            if "ci_skip" in item.keywords:
                item.add_marker(skip_ci)
