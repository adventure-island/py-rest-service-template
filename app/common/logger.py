"""
This module sets up the root logger under the `logging` module
"""
import logging
from typing import Any
import anticrlf

# from google.cloud.logging import Client

from app.common.server_env import server_env

LOGGING_MAX_LEN: int = 1024

if server_env.is_development:
    log_format = (
        "[%(filename)s:%(lineno)s - %(funcName)10s()] %(" "levelname)s: %(message)s"
    )
    # Note that default lever is INFO
    logging.basicConfig(level=logging.INFO, format=log_format)
else:
    # Instantiate a new Stackdriver logging client.
    client = Client()
    client.get_default_handler()
    client.setup_logging(log_level=logging.DEBUG)


# configure logging to prevent newline injection (CWE-117, detected by veracode)
logging_fmt = "%(levelname)s:%(name)s:%(message)s"
root_logger = logging.getLogger()
if root_logger.handlers:
    for root_handler in root_logger.handlers:
        if root_handler.formatter:
            root_handler.setFormatter(
                anticrlf.LogFormatter(root_handler.formatter._fmt)
            )


def get_truncated_str(data: Any, max_len: int = LOGGING_MAX_LEN):
    s = str(data)
    if len(s) > max_len:
        mark = "<TRUNCATED>"
        return s[: (max_len - len(mark))] + mark
    else:
        return s
