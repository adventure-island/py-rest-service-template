"""
This module defines SQL user-retrieval resource-classes.
"""

import uuid

import fastapi
import sqlalchemy.orm
from starlette.concurrency import run_in_threadpool

from app.common.jsonapi import JsonApiUserEnvelope
from app.common.sql_dals import get_user_by_id, insert_user
from app.common.api_dependencies import get_db
from app.common.excs import NotFoundError


async def get_sql_user(
    user_id: uuid.UUID, db: sqlalchemy.orm.Session = fastapi.Depends(dependency=get_db)
) -> JsonApiUserEnvelope:
    """Retrieves a single user through its ID from the SQL database.

    Args:
        user_id (uuid.UUID): The ID of the user to be retrieved.
        db (sqlalchemy.orm.Session): SQLAlchemy database session automatically
        injected by a middleware.

    Returns:
        JsonApiUserEnvelope: The retrieved user wrapped in a JSONAPI envelope.

    Raises:
        NotFoundError: Raised when no user could be found for the given ID.
    """

    # Retrieve the `User` database record mapped to an instance of the user
    # model class.
    user = await run_in_threadpool(get_user_by_id, user_id=user_id, db=db)

    # Raise a 404 if nothing was found.
    if not user:
        raise NotFoundError(
            detail=f"No user with ID {user_id} found in the SQL database."
        )

    # Assemble the JSONAPI result defining the returned user.
    result = JsonApiUserEnvelope.from_user(user=user, meta=None, links=None)

    return result


async def store_sql_user(
    user: JsonApiUserEnvelope,
    db: sqlalchemy.orm.Session = fastapi.Depends(dependency=get_db),
) -> dict:
    # Store the user.
    user_model = user.to_user()
    insert_user(user_model, db)

    return {"message": f"User {user_model.id} has been created successfully."}
