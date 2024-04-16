from typing import List, Optional

from bson import ObjectId

from dto.review_dto import ReviewDto, ReviewDtoCreate, ReviewDtoUpdate
from repositories.review_repository import ReviewRepository


class ReviewService:
    review_repository = ReviewRepository()

    async def get_all_reviews(self) -> List[ReviewDto]:
        reviews = await self.review_repository.get_reviews()
        return [ReviewDto.from_review(review) for review in reviews]
    
    async def get_all_reviews_from_user(self, user_id: ObjectId) -> List[ReviewDto]:
        reviews = await self.review_repository.get_reviews_from_user(user_id)
        return [ReviewDto.from_review(review) for review in reviews]
    
    async def get_all_reviews_from_game(self, game_id: ObjectId) -> List[ReviewDto]:
        reviews = await self.review_repository.get_reviews_from_game(game_id)
        return [ReviewDto.from_review(review) for review in reviews]

    async def get_review_by_id(self, review_id: ObjectId) -> Optional[ReviewDto]:
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            return None
        return ReviewDto.from_review(review)

    async def create_review(self, review_dto: ReviewDtoCreate) -> Optional[ReviewDto]:
        review = await self.review_repository.create_review(review_dto.to_review())
        if not review:
            return None
        return ReviewDto.from_review(review)

    async def update_review(self, review_id: ObjectId, review_dto: ReviewDtoUpdate) -> Optional[ReviewDto]:
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            return None
        updated_review = await self.review_repository.update_review(review_id, review_dto.to_review(review).dict())
        if not updated_review:
            return None
        return ReviewDto.from_review(updated_review)

    async def delete_review(self, review_id: ObjectId) -> bool:
        review = await self.get_review_by_id(review_id)
        if not review:
            return False
        return await self.review_repository.delete_review(review_id)
