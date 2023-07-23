# -*- coding: utf-8 -*-

"""
This module defines the base `flask_sqlalchemy.SQLAlchemy` instance to be used
in defining all ORM classes as well as the `OrmMixin` ORM class providing
generic to all ORM classes that inherit from it.
"""

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base

from app.common.sql_utils import get_sqlachemy_db_uri


# Create schema metadata with a constraint naming convention so that all
# constraints are named automatically based on the tables and columns they're
# defined upon. This ensures that all constraints will be given a unique name
# regardless of the backend database which allows for `alembic` to create
# comprehensive migrations of the defined schemata.
metadata = sqlalchemy.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s",
        "pk": "pk_%(table_name)s",
    }
)

engine = sqlalchemy.create_engine(get_sqlachemy_db_uri())
session_factory = sqlalchemy.orm.sessionmaker(bind=engine)

Base = declarative_base()


class OrmMixin(object):
    """Mixin class providing generic methods to all the 
    ORM classes that inherit from it."""

    @sqlalchemy.ext.declarative.declared_attr
    def dt_created(self):
        """Declared column storing when the record was first created (DB
        timestamp).
        """
        return sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)

    @sqlalchemy.ext.declarative.declared_attr
    def dt_updated(self):
        """Declared column storing when the record was last updated (DB
        timestamp).
        """
        return sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)

    @classmethod
    def get_pk(cls):
        """Retrieves the class' primary-key attribute.

        Returns:
            sqlalchemy.Column: The class' primary-key attribute.
        """

        pk = sqlalchemy.inspect(cls).primary_key[0]

        return pk

    @classmethod
    def get_pk_name(cls):
        """Retrieves the name of the class' primary-key attribute.

        Returns:
            str: The name of the class' primary-key attribute.
        """

        pk = cls.get_pk()

        return pk.name

    @classmethod
    def get_col_names(cls):
        """Retrieves the names of the class' attributes excluding foreign-keys.

        Returns:
            list[str]: List of names of the class' attributes excluding
                foreign-keys.
        """

        columns_all = sqlalchemy.inspect(cls).columns

        columns_wo_fks = [col for col in columns_all if not col.foreign_keys]

        return [col.name for col in columns_wo_fks]

    @classmethod
    def get_fk_names(cls):
        """Retrieves the names of the class' foreign-key attributes.

        Returns:
            list[str]: List of names of the class' foreign-key attributes.
        """

        columns_all = sqlalchemy.inspect(cls).columns

        columns_fks = [col for col in columns_all if col.foreign_keys]

        return [col.name for col in columns_fks]
