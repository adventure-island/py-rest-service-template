"""
This module specifies middleware functions to be used in the project's APIs.
"""

import logging
from starlette import status
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable

from app.common.orm_base import session_factory

logger = logging.getLogger(__name__)


async def inject_db_session(request: Request, call_next):
    try:
        request.state.db = session_factory()
        response = await call_next(request)
    except:
        logger.exception("An exception occurred when processing the request.")
        response = Response(
            "Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    finally:
        request.state.db.close()
    return response
