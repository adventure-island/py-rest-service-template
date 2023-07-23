""" Custom application-wide exception classes.

This module contains custom exception classes that can be used to wrap other exceptions and allow for consistent
error-handling across the application.
"""

from typing import Dict, Optional

import fastapi
import starlette.status


class JsonApiHttpException(fastapi.HTTPException):
    """Wrapper class around `fastapi.HTTPException` specific to JSONAPI HTTP errors."""

    def __init__(
        self,
        status_code: int,
        title: Optional[str],
        detail: str,
        headers: Optional[Dict] = None,
    ):
        """Initializes exception.

        Args:
            status_code (int): The exceptions HTTP status code.
            title (str): The error title.
            detail (str): The error cause in detail.
            headers (Optional[Dict]): Headers to be added to the error response.
        """

        super().__init__(status_code=status_code, detail=detail, headers=headers)

        self.title = title


class NotFoundError(JsonApiHttpException):
    """Exception raised when a requested resource was not found."""

    def __init__(self, detail: str, title: Optional[str] = "Resource not found."):
        """Initializes exception.

        Args:
            detail (str): The error cause in detail.
            title (Optional[str] = "Resource not found."): The error title.
        """

        super().__init__(
            status_code=starlette.status.HTTP_404_NOT_FOUND, title=title, detail=detail
        )
