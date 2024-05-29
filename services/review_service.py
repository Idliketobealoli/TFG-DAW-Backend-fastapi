from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from dto.review_dto import ReviewDto, ReviewDtoCreate, ReviewDtoUpdate
from repositories.game_repository import GameRepository
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository


class ReviewService:
    review_repository = ReviewRepository()
    user_repository = UserRepository()
    game_repository = GameRepository()

    async def get_all_reviews(self) -> List[ReviewDto]:
        reviews = await self.review_repository.get_reviews()
        return [await ReviewDto.from_review(review, self.user_repository, self.game_repository) for review in reviews]
    
    async def get_all_reviews_from_user(self, user_id: ObjectId) -> List[ReviewDto]:
        reviews = await self.review_repository.get_reviews_from_user(user_id)
        return [await ReviewDto.from_review(review, self.user_repository, self.game_repository) for review in reviews]
    
    async def get_all_reviews_from_game(self, game_id: ObjectId) -> List[ReviewDto]:
        reviews = await self.review_repository.get_reviews_from_game(game_id)
        return [await ReviewDto.from_review(review, self.user_repository, self.game_repository) for review in reviews]

    async def get_review_by_id(self, review_id: ObjectId) -> ReviewDto:
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with ID: {review_id} not found.")
        return await ReviewDto.from_review(review, self.user_repository, self.game_repository)

    async def create_review(self, review_dto: ReviewDtoCreate) -> ReviewDto:
        review = await self.review_repository.create_review(review_dto.to_review())
        if not review:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating review for user with ID: "
                                       f"{review_dto.user_id} and game with ID: {review_dto.game_id}.")
        return await ReviewDto.from_review(review, self.user_repository, self.game_repository)

    async def update_review(self, review_id: ObjectId, review_dto: ReviewDtoUpdate) -> ReviewDto:
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with ID: {review_id} not found.")
        updated_review = await self.review_repository.update_review(review_id, review_dto.to_review(review).dict())
        if not updated_review:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating review for user with ID: "
                                       f"{review_dto.user_id} and game with ID: {review_dto.game_id}.")
        return await ReviewDto.from_review(updated_review, self.user_repository, self.game_repository)

    async def delete_review(self, review_id: ObjectId) -> bool:
        review = await self.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with ID: {review_id} not found.")
        return await self.review_repository.delete_review(review_id)
