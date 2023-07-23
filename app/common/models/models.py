"""
This module defines pydantic models used for validation and (de)serialization
in API requests/responses.
"""

import datetime
import uuid

from pydantic import BaseModel, SecretStr, EmailStr

from app.common.enums import UserType


class ModelUser(BaseModel):
    """Pydantic model class representing a user."""

    id: uuid.UUID
    name: str
    email: EmailStr
    dob: datetime.date
    password: SecretStr
    user_type: UserType
    dt_added: datetime.datetime

    class Config:
        orm_mode = True
