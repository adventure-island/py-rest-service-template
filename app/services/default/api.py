# coding=utf-8
"""
This module defines the routes for the `default` service.
"""

import os
import logging

from starlette.concurrency import run_in_threadpool
from starlette.status import HTTP_200_OK
from typing import Dict

import app as app_module
from app.common.api_base import create_app

logger = logging.getLogger(__name__)

app = create_app(
    prefix="default",
    debug=False if os.getenv("GAE_DEPLOYMENT_ID") else True,
    title="New Service Project Template Default Service API",
    description="An template API for new project development.",
    version=app_module.__version__,
)


async def ping() -> Dict:
    """Returns a simple status serving as a ping endpoint.

    Returns:
        Dict: A status response.
    """

    logger.debug("ping request received.")

    return {"status": "OK"}


async def warmup() -> Dict:
    """Returns a simple status serving as a warmup endpoint.

    Returns:
        Dict: A status response.
    """

    logger.debug("warmup request received.")

    return {"status": "OK"}


def get_version() -> str:
    """Retrieves the API versioning details.

    Returns:
        str: API versioning details.
    """

    # Assemble the path to the `version.txt` file.
    version_path = os.path.join(os.path.dirname(__file__), "resources/version.txt")

    # Read in the versioning details from the `version.txt` file.
    with open(version_path, "r") as content_file:
        content = content_file.read()

    return content


async def get_version_async() -> str:
    return await run_in_threadpool(get_version)


app.add_api_route(
    path="/", endpoint=ping, methods=["GET"], tags=["ping"], status_code=HTTP_200_OK
)

app.add_api_route(
    path="/_ah/warmup",
    endpoint=warmup,
    methods=["GET"],
    tags=["warmup"],
    status_code=HTTP_200_OK,
)

app.add_api_route(
    path="/version",
    endpoint=get_version_async,
    methods=["GET"],
    tags=["get_version"],
    status_code=HTTP_200_OK,
)
