"""PicoRun runtime classes."""

from typing import Any

from requests import Response


class ApiError(Exception):

    """Exception raised when an API call fails."""

    def __init__(self, message: str, status_code: int) -> None:
        """Construct an ApiError."""
        super().__init__(f"Error {status_code}: {message}")
        self.status_code = status_code


class ApiRequestArgs:

    """Arguments for making an API call with requests."""

    def __init__(
        self,
        path: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        """Construct an object with the arguments for the API call."""
        self.path = path
        self.query = query
        self.json = payload
        self.headers = headers

    def to_kwargs(self) -> dict[str, Any]:
        """Convert the object to a dictionary of keyword arguments for requests."""
        output = {}
        for property in ["headers", "json", "query"]:
            if getattr(self, property):
                output[property] = getattr(self, property)
        return output


class ApiResponse:

    """API response."""

    def __init__(self, response: Response) -> None:
        """Construct an ApiResponse."""
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self.body = response.text
        if "application/json" in response.headers["Content-Type"]:
            self.body = response.json()

    def asdict(self) -> dict[str, Any]:
        """Convert the object to a dictionary."""
        return {
            "statusCode": self.status_code,
            "headers": dict(self.headers),
            "body": self.body,
        }
