from enum import Enum
from pydantic import BaseModel, EmailStr, SkipValidation, Field
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
    birthdate: SkipValidation[datetime]
    role: Role = Field(default=Role.USER)
    active: bool = Field(default=True)
    profile_picture: str = Field(default="base.png")

    class Config:
        arbitrary_types_allowed = True
