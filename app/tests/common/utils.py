"""
This module defines utility functions used in API testing.
"""

import os
import requests


def delete_all_entities():
    """Deletes all Datastore entities of the kinds defined in the codebase to
    ensure that tests can run in a clean environment.
    """

    host = os.getenv("DATASTORE_EMULATOR_HOST", "localhost:8814")
    url = f"http://{host}/reset"
    requests.post(url)

    foo = 1
