import pytest
from unittest.mock import Mock, patch
from py_alpaca_api.http.requests import Requests


@pytest.fixture
def requests_obj():
    return Requests()


def test_request_successful(requests_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "Success"
    with patch("requests.Session.request", return_value=mock_response):
        response = requests_obj.request("GET", "https://example.com")
        assert response == mock_response


def test_request_error(requests_obj):
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Error"
    with patch("requests.Session.request", return_value=mock_response):
        with pytest.raises(Exception):
            requests_obj.request("GET", "https://example.com")


def test_request_with_headers(requests_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    headers = {"Authorization": "Bearer token"}
    with patch("requests.Session.request", return_value=mock_response):
        response = requests_obj.request("GET", "https://example.com", headers=headers)
        assert response == mock_response


def test_request_with_params(requests_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    params = {"key": "value"}
    with patch("requests.Session.request", return_value=mock_response):
        response = requests_obj.request("GET", "https://example.com", params=params)
        assert response == mock_response


def test_request_with_json(requests_obj):
    mock_response = Mock()
    mock_response.status_code = 200
    json_data = {"data": "value"}
    with patch("requests.Session.request", return_value=mock_response):
        response = requests_obj.request("POST", "https://example.com", json=json_data)
        assert response == mock_response
