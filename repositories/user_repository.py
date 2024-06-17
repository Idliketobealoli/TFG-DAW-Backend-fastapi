from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional

from pydantic import EmailStr

from db.database import db
from model.user import User
from repositories import file_repository


def get_pfp_by_name(name: str) -> str:
    return file_repository.get_file_full_path("user_pfp", name)


class UserRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.user_routes

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[User]:
        user = await self.collection.find_one({"id": user_id})
        if user:
            return User(**user)
        return None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user = await self.collection.find_one({"username": username})
        if user:
            return User(**user)
        return None

    async def user_exists_by_username_or_email(self, username: str, email: EmailStr) -> bool:
        user_by_username = await self.collection.find_one({"username": username})
        user_by_email = await self.collection.find_one({"email": email})
        if user_by_username or user_by_email:
            return True
        return False

    async def get_users(self) -> List[User]:
        users = await self.collection.find({}).to_list(length=None)
        return [User(**user) for user in users]

    async def get_users_active(self, active: bool) -> List[User]:
        users = await self.collection.find({"active": active}).to_list(length=None)
        return [User(**user) for user in users]

    async def create_user(self, user: User) -> Optional[User]:
        await self.collection.insert_one(user.dict())
        return await self.get_user_by_id(user.id)

    async def update_user(self, user_id: ObjectId, user_data: dict) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        await self.collection.update_one({"id": user.dict().pop('id', None)},
                                         {"$set": user_data})  # Si no funciona, ver gamerepository
        return await self.get_user_by_id(user_id)

    async def upload_image_for_user(self, file: UploadFile, user_id: ObjectId) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        pfp = await file_repository.upload_file(file, "user_pfp", str(user_id))
        user.profile_picture = pfp
        await self.collection.update_one({"id": user.dict().pop('id', None)},
                                         {"$set": user.dict()})
        return True

    async def delete_user(self, user_id: ObjectId) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.active = not user.active
        await self.collection.update_one({"id": user.dict().pop('id', None)}, {"$set": user.dict()})
        return await self.get_user_by_id(user_id)
