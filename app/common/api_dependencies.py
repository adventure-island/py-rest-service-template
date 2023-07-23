"""
This module defines API dependency resolver functions.
"""

import sqlalchemy.orm
from starlette.requests import Request


def get_db(request: Request) -> sqlalchemy.orm.Session:
    """FastAPI dependency meant to automatically retrieve the SQL DB session
    injected via a middleware."""
    return request.state.db
