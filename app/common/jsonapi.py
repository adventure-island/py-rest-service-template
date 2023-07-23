"""
This module defines pydantic models used for validation and (de)serialization in API requests/responses.
"""

import datetime
import uuid
from typing import Optional, Union, List

from pydantic import BaseModel

from app.common.enums import UserType
from app.common.models.models import ModelUser


class JsonApiUserContainer(BaseModel):
    """Pydantic model class meant to represent the JSONAPI document of an
    instance of the user model class."""

    class JsonApiUserAttributes(BaseModel):
        """Pydantic model class meant to represent the JSONAPI attributes of
        an instance of the user model class."""

        name: str
        email: str
        dob: datetime.date
        password: str
        user_type: UserType
        dt_added: datetime.datetime

    id: Optional[uuid.UUID]
    type: str = "user"
    attributes: JsonApiUserAttributes

    @classmethod
    def from_user(cls, user: ModelUser) -> "JsonApiUserContainer":
        """Creates a `JsonApiUserContainer` object from an instance of the
        user model class.

        Args:
            user (User): The instance of the user model class to be converted
            into a `JsonApiUserContainer` object.

        Returns:
            JsonApiUserContainer: The newly created object.
        """

        attributes = JsonApiUserContainer.JsonApiUserAttributes(
            name=user.name,
            email=user.email,
            dob=user.dob,
            password=str(user.password.get_secret_value()),
            user_type=user.user_type.value,
            dt_added=user.dt_added,
        )

        obj = cls(id=user.id, type="user", attributes=attributes)

        return obj

    def to_user(self) -> ModelUser:
        """Converts this object to an instance of the user model class.

        Returns:
            User: The converted instance of the user model class.
        """

        obj = ModelUser(
            id=str(self.id),
            name=self.attributes.name,
            email=self.attributes.email,
            dob=self.attributes.dob,
            password=self.attributes.password,
            user_type=self.attributes.user_type,
            dt_added=self.attributes.dt_added,
        )

        return obj


class JsonApiEnvelopeMeta(BaseModel):
    """Pydantic model class meant to represent the `meta` portion of a
    JSONAPI payload."""

    origin: str
    timestamp: datetime.datetime
    user_id: uuid.UUID


class JsonApiEnvelopeLinks(BaseModel):
    """Pydantic model class meant to represent the `links` portion of a J
    SONAPI payload."""

    first: Optional[str] = None
    last: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None


class JsonApiUserEnvelope(BaseModel):
    """Pydantic model class meant to represent a JSONAPI payload including one or more JSONAPI representations of
    instances of the user model class.
    """

    meta: Optional[JsonApiEnvelopeMeta] = None
    links: Optional[JsonApiEnvelopeLinks] = None
    data: Union[JsonApiUserContainer, List[JsonApiUserContainer]]

    @classmethod
    def from_user(
        cls,
        user: ModelUser,
        meta: Optional[JsonApiEnvelopeMeta] = None,
        links: Optional[JsonApiEnvelopeLinks] = None,
    ) -> "JsonApiUserEnvelope":
        """Creates a `JsonApiUserEnvelope` object from an instance of the user
        model class.

        Args:
            user (ModelUser): The instance of the user model class to be converted
                into a `JsonApiUserEnvelope` object.
            meta (Optional[JsonApiEnvelopeMeta] = None): An instance of the `
                JsonApiEnvelopeMeta` class to be included
                in the envelope.
            links (Optional[JsonApiEnvelopeLinks] = None): An instance of the
                `JsonApiEnvelopeLinks` class to be included in the envelope.

        Returns:
            JsonApiUserEnvelope: The newly created object.
        """

        if not isinstance(user, ModelUser):
            raise ValueError

        data = JsonApiUserContainer.from_user(user=user)

        obj = cls(meta=meta, links=links, data=data)

        return obj

    @classmethod
    def from_users(
        cls,
        users: List[ModelUser],
        meta: Optional[JsonApiEnvelopeMeta] = None,
        links: Optional[JsonApiEnvelopeLinks] = None,
    ) -> "JsonApiUserEnvelope":
        """Creates a `JsonApiUserEnvelope` object from a list of instances of
        the user model class.

        Args:
            users (List[User]): The instances of the user model class to be
                converted into a `JsonApiUserEnvelope` object.
            meta (Optional[JsonApiEnvelopeMeta] = None): An instance of the
                `JsonApiEnvelopeMeta` class to be included in the envelope.
            links (Optional[JsonApiEnvelopeLinks] = None): An instance of the
                `JsonApiEnvelopeLinks` class to be included in the envelope.

        Returns:
            JsonApiUserEnvelope: The newly created object.
        """

        if not isinstance(users, list):
            raise ValueError

        data = [JsonApiUserContainer.from_user(user=user) for user in users]

        obj = cls(meta=meta, links=links, data=data)

        return obj

    def to_user(self) -> ModelUser:
        """Extracts an instance of the user model class from this object.

        Returns:
            User: The extracted instance of the user model class.
        """

        if not isinstance(self.data, JsonApiUserContainer):
            raise ValueError

        return self.data.to_user()

    def to_users(self) -> List[ModelUser]:
        """Extracts a list of instances of the user model class from this
            object.

        Returns:
            List[User]: The list of extracted instances of the user model class.
        """

        if not isinstance(self.data, list):
            raise ValueError

        return [user.to_user() for user in self.data]
