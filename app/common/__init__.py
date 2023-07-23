# -*- coding: utf-8 -*-

"""
Package __init__.py module.
"""

import logging

# Initialize logging module
from app.common import logger

# Import `server_env` module to check deployment environment
from app.common.server_env import server_env

logger = logging.getLogger(__name__)

if not server_env.is_development:
    # Enable the Stackdriver Debugger as instructed under
    # https://cloud.google.com/debugger/docs/setup/python#python_37

    try:
        import googleclouddebugger

        googleclouddebugger.enable()
        logger.info("Cloud debugger enabled.")
    except ImportError:
        logger.error("Failed to load googleclouddebugger.")
        pass
