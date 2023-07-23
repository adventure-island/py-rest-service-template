import sqlalchemy.orm
from sqlalchemy_utils import UUIDType

from app.common.orm_base import Base
from app.common.enums import UserType


class User(Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(UUIDType, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.Unicode(length=190))
    email = sqlalchemy.Column(sqlalchemy.Unicode(length=190))
    dob = sqlalchemy.Column(sqlalchemy.Date())
    password = sqlalchemy.Column(sqlalchemy.Unicode(length=190))
    user_type = sqlalchemy.Column(sqlalchemy.Enum(UserType))
    dt_added = sqlalchemy.Column(sqlalchemy.DateTime())
