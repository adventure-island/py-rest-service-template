"""
This module defines unit-tests for the endpoints facilitating retrieval of users.
"""

import uuid
import json

from starlette.testclient import TestClient
import sqlalchemy.orm

from app.common.jsonapi import JsonApiUserEnvelope
from app.common.models.models import ModelUser
from app.common.sql_dals import insert_user


def test_retrieve_user_one_success(
    client_api: TestClient, user: ModelUser, db: sqlalchemy.orm.Session
):
    """Tests the retrieval of a single existing user through the corresponding
    endpoint."""

    insert_user(user=user, db=db)

    # Retrieve the user.
    request_response = client_api.get(url=f"/api/sql/user/{user.id}")

    assert request_response.status_code == 200

    data = request_response.json()

    assert data
    assert data["data"]["attributes"]

    attrs = data["data"]["attributes"]

    assert data["data"]["id"] == str(user.id)
    assert data["data"]["type"] == "user"
    assert attrs["name"] == user.name
    assert attrs["email"] == user.email
    assert attrs["dob"] == user.dob.isoformat()
    assert attrs["password"] == str(user.password.get_secret_value())
    assert attrs["user_type"] == user.user_type.value
    assert attrs["dt_added"]


def test_retrieve_user_one_failure_404(client_api: TestClient):
    """Tests the retrieval of a single non-existing user through the
    corresponding endpoint that should result in a 404.
    """

    # Retrieve the user with a non-existent ID.
    request_response = client_api.get(url=f"/api/sql/user/{uuid.uuid1()}")

    data = request_response.json()

    assert request_response.status_code == 404
    assert data
    assert "errors" in data
    assert "status" in data["errors"][0]
    assert "code" in data["errors"][0]
    assert data["errors"][0]["status"] == "404"
    assert "title" in data["errors"][0]
    assert "detail" in data["errors"][0]


def test_store_user_success(
    client_api: TestClient, user: ModelUser, db: sqlalchemy.orm.Session
):
    """Tests the retrieval of a single existing user through the
    corresponding endpoint."""

    payload = JsonApiUserEnvelope.from_user(user)

    request_response = client_api.post(url=f"/api/sql/user/add", data=payload.json())

    assert request_response.status_code == 201
