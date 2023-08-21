"""Test picorun classes."""

import pytest

from picorun import ApiError, ApiRequestArgs, ApiResponse


def mock_response(
    status_code: int = 200,
    headers: dict[str, str] | None = None,
    text: str | None = None,
    json: dict[str, str] | None = None,
) -> "MockResponse": # noqa: F821 class defined in this function
    """Mock requests.Response."""
    class MockResponse:
        def __init__(self) -> None:
            self.status_code = status_code
            self.headers = headers or {}
            self.text = text
            self.json = lambda: json
    return MockResponse()

def test_api_error() -> None:
    """Test ApiError."""
    error = ApiError("message", 404)
    assert str(error) == "Error 404: message"
    assert error.status_code == 404


def test_api_request_args() -> None:
    """Test ApiRequestArgs."""
    args = ApiRequestArgs(
        path={"path": "value"},
        query={"query": "value"},
        payload={"payload": "value"},
        headers={"headers": "value"},
    )
    assert args.path == {"path": "value"}
    assert args.query == {"query": "value"}
    assert args.json == {"payload": "value"}
    assert args.headers == {"headers": "value"}
    assert args.to_kwargs() == {
        "headers": {"headers": "value"},
        "json": {"payload": "value"},
        "query": {"query": "value"},
    }


def test_api_request_args_invalid_args() -> None:
    """Test ApiRequestArgs with invalid arguments."""
    with pytest.raises(TypeError):
        _ = ApiRequestArgs(
            invalid={"invalid": "value"},
        )

def test_api_response() -> None:
    """Test ApiResponse."""
    response = mock_response(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        text="body",
    )
    api_response = ApiResponse(response)
    assert api_response.response == response
    assert api_response.status_code == 200
    assert api_response.headers == {"Content-Type": "text/plain"}
    assert api_response.body == "body"
    assert api_response.asdict() == {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "body",
    }

def test_api_response_json() -> None:
    """Test ApiResponse with JSON body."""
    response = mock_response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        json={"key": "value"},
    )
    api_response = ApiResponse(response)
    assert api_response.body == {"key": "value"}
    assert api_response.asdict() == {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": {"key": "value"},
    }
