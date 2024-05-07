from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.user import User


class UserRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.user_routes

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[User]:
        user = await self.collection.find_one({"id": user_id})
        if user:
            return User(**user)
        return None

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
        await self.collection.update_one({"id": user.pop('id', None)}, {"$set": user_data}) # Si no funciona, ver gamerepository
        return await self.get_user_by_id(user_id)

    async def delete_user(self, user_id: ObjectId) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.active = False
        await self.collection.update_one({"id": user.pop('id', None)}, {"$set": user}) # Lo mismo aqui
        return await self.get_user_by_id(user_id)
        # await self.collection.delete_one({"id": user_id})
        # user = await self.get_user_by_id(user_id)
        # return user is None
