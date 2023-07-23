# -*- coding: utf-8 -*-

"""
This module defines basic utility functions.
"""

import os
import logging

_SERVICE = None

logger = logging.getLogger(__name__)


def get_service_identity():
    """Returns the application ID.

    Returns:
        str: The application ID.
    """

    global _SERVICE

    if not _SERVICE:
        # See a list of existing env vars provided in Python 3 runtime here:
        # https://cloud.google.com/appengine/docs/standard/python3/runtime
        _SERVICE = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not _SERVICE:
            logger.error("Could not load the value of GOOGLE_CLOUD_PROJECT")

    return _SERVICE


def get_project_location() -> str:
    return os.environ["GOOGLE_CLOUD_LOCATION"]
