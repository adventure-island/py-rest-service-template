"""
This module defines unit-test fixtures.
"""
import datetime
import os
import uuid

import pytest
import sqlalchemy

from starlette.testclient import TestClient

from app.common.enums import UserType
from app.common.models.models import ModelUser
from app.common.orm_base import Base, engine, session_factory
from app.services.default.api import app as default_app
from app.services.api.api import app as api_app

_schema_initialized = False


def initialize_schema():
    """Initialize the SQL schema if not already initialized."""
    global _schema_initialized
    if not _schema_initialized:
        # Drop and recreate the entire ORM schema.
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        _schema_initialized = True


@pytest.fixture()
def db() -> sqlalchemy.orm.Session:
    """SQL DB session fixture."""

    initialize_schema()
    db = session_factory()

    yield db


@pytest.fixture()
def user() -> ModelUser:
    """Instance fixture of the user model class."""

    user = ModelUser(
        id=uuid.uuid4(),
        name="jane.doe",
        email="jane.doe@abc.com",
        dob=datetime.date(1987, 1, 13),
        password="Something, Something, Something, Dark Side",
        user_type=UserType.STAFF,
        dt_added=datetime.datetime(2017, 10, 9, 9, 0, 0),
    )

    yield user


@pytest.fixture()
def client_default() -> TestClient:
    """Starlette API test-client fixture for the `api` service."""

    client = TestClient(default_app)

    yield client


@pytest.fixture()
def client_api() -> TestClient:
    """Starlette API test-client fixture for the `api` service."""

    client = TestClient(api_app)

    yield client
