"""
This module defines utility functions for SQLAlchemy.
"""

import os


def get_sqlachemy_db_uri():
    """Assembles an SQLAlchemy-compatible URI to the SQL database.

    Note:
         If a `LOCAL_MODE` environment variable is defined the resulting URI will pertain to the local test server.
         Otherwise the URI will pertain to the production server.

    Returns:
        str: The SQLAlchemy-compatible URI to the SQL database.
    """

    # If a `LOCAL_MODE` environment-variable was set then set the SQL variables to pertain to the test server as
    # opposed to the production server.

    if os.environ.get("LOCAL_MODE"):
        username = os.environ["POSTGRES_USER"] or "postgres"
        password = os.environ["POSTGRES_PASSWORD"]
        host = os.environ["POSTGRES_HOST"] or "postgres"
        port = os.environ["POSTGRES_PORT"] or 5432
        db = os.environ["POSTGRES_DB"] or "postgres"

        db_uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db}"
    else:
        username = os.environ["POSTGRES_USER"]
        password = os.environ["POSTGRES_PASSWORD"]
        db = os.environ["POSTGRES_DB"]
        cloudsql_connection_name = os.environ["CLOUDSQL_CONNECTION_NAME"]

        db_uri = f"postgresql+psycopg2://{username}:{password}@/{db}?host=/cloudsql/{cloudsql_connection_name}"

    return db_uri
