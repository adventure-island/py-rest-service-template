# """
# This module defines unit-tests for the SQSL DAL functions.
# """

import sqlalchemy.orm

from app.common.models.orm_models import User
from app.common.sql_dals import get_user_by_id
from app.common.sql_dals import insert_user


def test_insert_user(user: User, db: sqlalchemy.orm.Session):
    """Tests the `insert_user` function by storing an instance of the user
    model class to the SQL database."""

    user_eval = insert_user(user=user, db=db)

    assert user_eval is not None
    assert user_eval.id == user.id
    assert user_eval.name == user.name
    assert user_eval.email == user.email
    assert user_eval.dob == user.dob
    assert user_eval.password == user.password.get_secret_value()
    assert user_eval.user_type == user.user_type
    assert user_eval.dt_added.replace(tzinfo=None) == user.dt_added.replace(tzinfo=None)


def test_get_user(user: User, db: sqlalchemy.orm.Session):
    """Tests the `get_user` function by storing an instance of the user model class to the SQL database and then
    retrieving it wrapped in an instance of the user model class.
    """

    insert_user(user=user, db=db)
    user_eval = get_user_by_id(user_id=user.id, db=db)

    assert user_eval is not None
    assert user_eval.id == user.id
    assert user_eval.name == user.name
    assert user_eval.email == user.email
    assert user_eval.dob == user.dob
    assert user_eval.password.get_secret_value() == user.password.get_secret_value()
    assert user_eval.user_type == user.user_type
    assert user_eval.dt_added.replace(tzinfo=None) == user.dt_added.replace(tzinfo=None)
