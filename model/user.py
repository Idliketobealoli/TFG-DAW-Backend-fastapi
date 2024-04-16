from enum import Enum
from pydantic import BaseModel, EmailStr
from bson import ObjectId
import datetime
from typing import Optional


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
    profile_picture: Optional[ObjectId] = None

    class Config:
        arbitrary_types_allowed = True
