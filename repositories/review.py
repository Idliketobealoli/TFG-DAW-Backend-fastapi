from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional

from db.database import db
from model.review import Review


class reviewRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.review_routes

    async def get_review_by_id(self, review_id: ObjectId) -> Optional[Review]:
        review = await self.collection.find_one({"id": review_id})
        if review:
            return Review(**review)
        return None

    async def get_reviews(self) -> List[Review]:
        reviews = await self.collection.find({}).to_list(length=None)
        return [Review(**review) for review in reviews]

    async def create_review(self, review: Review) -> Optional[Review]:
        await self.collection.insert_one(review.dict())
        return await self.get_review_by_id(review.id)

    async def update_review(self, review_id: ObjectId, review_data: dict) -> Optional[Review]:
        review = await self.collection.find_one({"id": review_id})
        await self.collection.update_one({"_id": review.pop('_id', None)}, {"$set": review_data})
        return await self.get_review_by_id(review_id)

    async def delete_review(self, review_id: ObjectId) -> bool:
        await self.collection.delete_one({"id": review_id})
        review = await self.get_review_by_id(review_id)
        return review is None
