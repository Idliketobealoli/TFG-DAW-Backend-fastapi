from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.wishlist import Wishlist


class WishlistRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.wishlist_routes

    async def get_wishlist_by_id(self, wishlist_id: ObjectId) -> Optional[Wishlist]:
        wishlist = await self.collection.find_one({"id": wishlist_id})
        if wishlist:
            return Wishlist(**wishlist)
        return None
    
    async def get_wishlist_by_user_id(self, user_id: ObjectId) -> Optional[Wishlist]:
        wishlist = await self.collection.find_one({"user_id": user_id})
        if wishlist:
            return Wishlist(**wishlist)
        return None

    # Sinceramente, el getAll y el findById lo quitaria tanto de wishlist como de library
    # y dejaria solo getByUserId, create, update y delete
    async def get_wishlists(self) -> List[Wishlist]:
        wishlists = await self.collection.find({}).to_list(length=None)
        return [Wishlist(**wishlist) for wishlist in wishlists]

    async def create_wishlist(self, wishlist: Wishlist) -> Optional[Wishlist]:
        await self.collection.insert_one(wishlist.dict())
        return await self.get_wishlist_by_id(wishlist.id)

    async def update_wishlist(self, wishlist_id: ObjectId, wishlist_data: dict) -> Optional[Wishlist]:
        wishlist = await self.collection.find_one({"id": wishlist_id})
        await self.collection.update_one({"_id": wishlist.pop('_id', None)}, {"$set": wishlist_data})
        return await self.get_wishlist_by_id(wishlist_id)

    async def delete_wishlist(self, wishlist_id: ObjectId) -> bool:
        await self.collection.delete_one({"id": wishlist_id})
        wishlist = await self.get_wishlist_by_id(wishlist_id)
        return wishlist is None
