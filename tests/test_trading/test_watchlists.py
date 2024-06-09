# Retrieves watchlist successfully using watchlist_id
import json
import pytest
from py_alpaca_api.trading.watchlists import Watchlist


def test_retrieves_watchlist_successfully_using_watchlist_id(mocker):
    # Arrange
    mock_response = {
        "id": "1234567890",
        "account_id": "account123",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "name": "Test Watchlist",
        "assets": [],
    }
    mocker.patch(
        "py_alpaca_api.http.requests.Requests.request",
        return_value=mocker.Mock(text=json.dumps(mock_response)),
    )
    watchlist = Watchlist(
        base_url="https://api.alpaca.markets",
        headers={"Authorization": "Bearer YOUR_API_KEY_HERE"},
    )

    # Act
    result = watchlist.get(watchlist_id="1234567890")

    # Assert
    assert result.id == "1234567890"
    assert result.name == "Test Watchlist"


# Raises ValueError when both watchlist_id and watchlist_name are provided
def test_raises_value_error_when_both_watchlist_id_and_watchlist_name_are_provided():
    # Arrange
    watchlist = Watchlist(
        base_url="https://api.alpaca.markets",
        headers={"Authorization": "Bearer YOUR_API_KEY_HERE"},
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Watchlist ID or Name is required, not both."):
        watchlist.get(watchlist_id="1234567890", watchlist_name="Test Watchlist")
