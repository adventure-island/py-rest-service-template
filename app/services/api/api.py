# -*- coding: utf-8 -*-

"""
Package api.py module.
"""

import logging

from app.common.jsonapi import JsonApiUserEnvelope
from app.services.api.resources.sql_users import get_sql_user, store_sql_user

"""
This module defines the API class and declares the routes for the `api` service.
"""

import os

import fastapi
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

import app as app_module
from app.common.api_base import create_app

logger = logging.getLogger(__name__)

app = create_app(
    prefix="api",
    debug=False if os.getenv("GAE_DEPLOYMENT_ID") else True,
    title="New Service Project Template API Service API",
    description="An template API for new project development.",
    version=app_module.__version__,
)  # type: fastapi.FastAPI

app.add_api_route(
    path="/api/sql/user/{user_id}",
    endpoint=get_sql_user,
    methods=["GET"],
    tags=["user"],
    response_model=JsonApiUserEnvelope,
    status_code=HTTP_200_OK,
    responses={404: {"description": "`User` not found."}},
)

app.add_api_route(
    path="/api/sql/user/add",
    endpoint=store_sql_user,
    methods=["POST"],
    tags=["user"],
    status_code=HTTP_201_CREATED,
)
