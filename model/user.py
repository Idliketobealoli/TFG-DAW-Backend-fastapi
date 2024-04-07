from enum import Enum

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from bson import ObjectId


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(BaseModel):
    id: ObjectId
    name: str
    email: EmailStr
    password: str
    role: Role

    # Si no funcionase, cambiar por @validator, aunque esté deprecado (o quitar classmethod)
    @classmethod
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"password must be longer than 4 characters: {value}")
        return value

    @classmethod
    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"name must be longer than 1 character: {value}")
        return value

    class Config:
        arbitrary_types_allowed = True
