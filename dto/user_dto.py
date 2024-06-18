from bson import ObjectId
from pydantic import BaseModel, EmailStr, SkipValidation
from fastapi import HTTPException, status
from typing import Optional
import datetime
from services.cipher_service import encode
from model.user import Role, User


class UserDto(BaseModel):
    id: str
    name: str
    surname: str
    username: str
    email: EmailStr
    birthdate: SkipValidation[datetime]
    role: Role
    active: bool

    @classmethod
    async def from_user(cls, user: User):
        return UserDto(
            id=str(user.id),
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            birthdate=user.birthdate,
            role=user.role,
            active=user.active
        )

    class Config:
        arbitrary_types_allowed = True


class UserDtoShort(BaseModel):
    id: str
    name: str
    surname: str
    username: str
    email: EmailStr

    @classmethod
    async def from_user(cls, user: User):
        return UserDtoShort(
            id=str(user.id),
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email
        )


class UserDtoToken(BaseModel):
    user: UserDto
    token: str


class UserDtoLogin(BaseModel):
    username: str
    password: str


class UserDtoCreate(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str
    repeatPassword: str
    birthdate: SkipValidation[datetime]

    def validate_fields(self):
        if len(self.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {self.name}")

        if len(self.surname) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Surname must be longer than 4 characters: {self.surname}")

        if len(self.username) < 4:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Username must be longer than 3 characters: {self.username}")

        if self.repeatPassword != self.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Passwords do not match.")

        if len(self.password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Password must be at least 6 characters long.")

        if datetime.datetime.fromisoformat(self.birthdate.__str__()) > datetime.datetime.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Birthdate must not be in the future.")
        return

    def to_user(self):
        return User(
            id=ObjectId(),
            name=self.name,
            surname=self.surname,
            username=self.username,
            email=self.email,
            password=encode(self.password),
            birthdate=self.birthdate,
        )

    class Config:
        arbitrary_types_allowed = True


class UserDtoUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]
    birthdate: Optional[str]

    def validate_fields(self):
        if self.name is not None and len(self.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {self.name}")

        if self.surname is not None and len(self.surname) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Surname must be longer than 4 character: {self.surname}")

        if self.password is not None and len(self.password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Password must be at least 6 characters long.")

        if (self.birthdate is not None and
                datetime.datetime.fromisoformat(self.birthdate) > datetime.datetime.today()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Birthdate must not be in the future.")
        return

    def to_user(self, user: User):
        if self.name is None:
            self.name = user.name
        if self.surname is None:
            self.surname = user.surname
        if self.password is None:  # en este caso no debemos cifrarla porque ya está cifrada
            passwd = user.password
        else:  # en este caso si la ciframos
            passwd = encode(self.password)
        if self.birthdate is None:
            b_date = user.birthdate
        else:
            b_date = datetime.datetime.fromisoformat(self.birthdate)

        return User(
            id=user.id,
            name=self.name,
            surname=self.surname,
            username=user.username,
            email=user.email,
            password=passwd,
            birthdate=b_date,
            role=user.role,
            active=user.active
        )
