"""
This module defines the API base-class including prefix-based paths for specs
and documentation as well as error-handling.
"""

import fastapi
from typing import Any
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette_json import UJsonResponse
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.common.middlewares import inject_db_session


async def http_exception_handler(request: Request, exc: HTTPException) -> UJsonResponse:
    """Formats `HTTPException` exceptions as JSONAPI errors.

    Args:
        request (Request): The request that triggered the error.
        exc (HTTPException): The exception to be formatted.

    Returns:
        UJsonResponse: The JSONAPI formatted error.
    """

    content = {
        "errors": [
            {
                "status": str(exc.status_code),
                "code": str(type(exc).__name__),
                "title": getattr(exc, "title") if hasattr(exc, "title") else None,
                "detail": exc.detail,
            }
        ]
    }

    response = UJsonResponse(status_code=exc.status_code, content=content)

    return response


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> UJsonResponse:
    """Formats `RequestValidationError` exceptions as JSONAPI errors.

    Args:
        request (Request): The request that triggered the error.
        exc (HTTPException): The exception to be formatted.

    Returns:
        UJsonResponse: The JSONAPI formatted error.
    """

    content = {
        "errors": [
            {
                "status": str(HTTP_422_UNPROCESSABLE_ENTITY),
                "code": str(type(exc).__name__),
                "title": "Validation Error",
                "detail": "A validation error occurred when processing the request.",
                "meta": {"detail": exc.errors(), "body": exc.body},
            }
        ]
    }

    response = UJsonResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content=content)

    return response


def create_app(prefix: str, *args: Any, **kwargs: Any) -> fastapi.FastAPI:
    """Creates a new FastAPI app with built-in error-handling and URL definition for spec and documentation.

    Args:
        prefix (str): The prefix of the new app that will define the URLs for spec and documentation.
        *args: Arguments that will be passed to the `FastAPI` constructor.
        **kwargs: Keyword arguments that will be passed to the `FastAPI` constructor.

    Returns:
        fastapi.FastAPI: The created app.
    """

    kwargs.update(
        {
            "openapi_url": f"/{prefix}/openapi.json",
            "docs_url": f"/{prefix}/docs",
            "redoc_url": f"/{prefix}/redoc",
        }
    )

    app = fastapi.FastAPI(*args, **kwargs)

    # app.add_middleware(BaseHTTPMiddleware, dispatch=inject_request_context)
    app.add_middleware(BaseHTTPMiddleware, dispatch=inject_db_session)

    # Add exception handler for standard `HTTPException` errors.
    app.add_exception_handler(
        exc_class_or_status_code=HTTPException, handler=http_exception_handler
    )
    # Add exception handler for built-in validation errors.
    app.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=validation_exception_handler,
    )

    return app
