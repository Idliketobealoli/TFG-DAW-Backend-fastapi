from enum import Enum
from pydantic import BaseModel, EmailStr
from bson import ObjectId
import datetime


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(BaseModel):
    id: ObjectId
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str
    birthdate: datetime
    role: Role
    active: bool

    class Config:
        arbitrary_types_allowed = True
