"""
This module defines SQL data access layer (DAL) functions.
"""

import uuid
from typing import Optional

from sqlalchemy.orm import Query, Session

from app.common.models.models import ModelUser
from app.common.models.orm_models import User


def get_user_by_id(user_id: uuid.UUID, db: Session) -> Optional[ModelUser]:
    """Retrieves a user via its ID from the SQL database.

    Args:
        user_id (uuid.UUID): The ID of the user to retrieve.
        db (sqlalchemy): SQLAlchemy database session automatically injected by a middleware.

    Returns:
        Optional[ModelUser]: The retrieved user wrapped in an instance of the user model class or `None` if no user was
            found for the defined ID.
    """

    query = db.query(User)  # type: Query
    query = query.filter(User.id == user_id)

    user = query.one_or_none()

    if not user:
        return None

    return ModelUser.from_orm(obj=user)


def insert_user(user: ModelUser, db: Session) -> User:
    """Inserts a new user to the SQL database.

    Args:
        user (ModelUser): The instance of the user model class to be inserted to the database.
        db (sqlalchemy): SQLAlchemy database session automatically injected by a middleware.

    Returns:
        User: The stored user record..
    """

    obj = User()
    obj.id = user.id
    obj.name = user.name
    obj.email = user.email
    obj.dob = user.dob
    obj.password = user.password.get_secret_value()
    obj.user_type = user.user_type
    obj.dt_added = user.dt_added

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj
