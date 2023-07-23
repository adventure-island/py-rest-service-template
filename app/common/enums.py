"""
This module defines enumeration classes to be used across the entire codebase.
"""

import enum


class UserType(enum.Enum):
    """Enumeration class defining the possible values of the `user_type`
        attribute under the `User` model.

    Attributes:
        STAFF (str): Issued when a user is part of staff.
        CUSTOMER (str): Issued when a user is a customer.
    """

    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"
