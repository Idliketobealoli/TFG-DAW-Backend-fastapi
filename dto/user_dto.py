from bson import ObjectId
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status
from typing import Optional
import datetime
import base64
from services.cipher_service import encode
from model.user import Role, User
from db.database import db


class UserDto(BaseModel):
    id: str
    name: str
    surname: str
    username: str
    email: EmailStr
    birthdate: datetime
    role: Role
    profile_picture: Optional[str] = None

    @classmethod
    def from_user(cls, user: User):
        image_data = db.get_file(user.profile_picture)
        image_data_base64 = None
        if image_data and image_data.content_type.startswith("image/"):
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return UserDto(
            id=str(user.id),
            name=user.name,
            surname=user.surname,
            username=user.username,
            email=user.email,
            birthdate=user.birthdate,
            role=user.role,
            profile_picture=image_data_base64
        )


class UserDtoToken(BaseModel):
    user: UserDto
    token: str


class UserDtoCreate(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str
    repeatPassword: str
    birthdate:datetime
    role: Role

    @classmethod
    def validate_fields(cls):
        if len(cls.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {cls.name}")
        
        if len(cls.surname) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Surname must be longer than 4 character: {cls.surname}")
        
        if len(cls.username) < 4:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Username must be longer than 3 character: {cls.username}")

        if cls.repeatPassword != cls.password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Passwords do not match.")

        if len(cls.password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Password must be at least 6 characters long.")
        
        if cls.birthdate > datetime.datetime.today:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Birthdate must not be in the future.")
        return

    @classmethod
    def to_user(cls):
        return User(
            id=ObjectId(),
            name=cls.name,
            surname=cls.surname,
            username=cls.username,
            email=cls.email,
            password=encode(cls.password),
            birthdate=cls.birthdate,
            role=cls.role,
            active=True
        )


class UserDtoUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]

    @classmethod
    def validate_fields(cls):
        if cls.name is not None and len(cls.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {cls.name}")
        
        if cls.surname is not None and len(cls.surname) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Surname must be longer than 4 character: {cls.surname}")

        if cls.password is not None and len(cls.password) < 6:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Password must be at least 6 characters long.")
        return

    @classmethod
    def to_user(cls, user: User):
        if cls.name is None: 
            cls.name = user.name
        if cls.surname is None:
            cls.surname = user.surname
        if cls.password is None: # en este caso no debemos cifrarla porque ya está cifrada
            passwd = user.password
        else: # en este caso si la ciframos
            passwd = encode(cls.password)
        
        return User(
            id=user.id,
            name=cls.name,
            surname=cls.surname,
            username=user.username,
            email=user.email,
            password=passwd,
            birthdate=user.birthdate,
            role=user.role,
            active=user.active
        )
