from bson import ObjectId
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import HTTPException, status

from model.user import Role, User


class UserDto(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role

    @classmethod
    def from_user(cls, user):
        return UserDto(
            id=str(user.id),
            name=user.name,
            email=user.email,
            role=user.role
        )


class UserDtoCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    repeatPassword: str
    role: Role

    @classmethod
    @field_validator("password")
    # Crear los validadores a pelo y llamarlos yo mismo, sin usar field validator.
    def passwords_match(cls, value, values):
        if 'repeatPassword' in values and values['repeatPassword'] != value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"passwords do not match.")
        return value

    @classmethod
    def to_user(cls, dto):
        return User(
            id=ObjectId(),
            name=dto.name,
            email=dto.email,
            password=dto.password,
            role=dto.role
        )


class UserDtoUpdate(BaseModel):
    name: str
    password: str

    @classmethod
    def to_user(cls, user, dto):
        return User(
            id=user.id,
            name=dto.name,
            email=user.email,
            password=dto.password,
            role=user.role
        )
