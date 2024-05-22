from bson import ObjectId
from pydantic import BaseModel, SkipValidation
from fastapi import HTTPException, status
import datetime
from model.review import Review
from repositories.game_repository import GameRepository
from repositories.user_repository import UserRepository
from typing import Optional


class ReviewDto(BaseModel):
    id: str
    game: str
    user: str
    publish_date: SkipValidation[datetime]
    rating: float
    description: str

    @classmethod
    async def from_review(cls, review: Review, user_repository: UserRepository, game_repository: GameRepository):
        game_model = await game_repository.get_game_by_id(review.game_id)
        user_model = await user_repository.get_user_by_id(review.user_id)
        return ReviewDto(
            id=str(review.id),
            game=game_model.name,
            user=user_model.username,
            publish_date=review.publish_date,
            rating=review.rating,
            description=review.description
        )

    class Config:
        arbitrary_types_allowed = True


class ReviewDtoCreate(BaseModel):
    game_id: ObjectId
    user_id: ObjectId
    rating: float
    description: str

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def validate_fields(cls):
        if cls.rating > 5:
            cls.rating = 5
        elif cls.rating < 0:
            cls.rating = 0

        if len(cls.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {cls.description}")
        return

    @classmethod
    def to_review(cls):
        return Review(
            game_id=cls.game_id,
            user_id=cls.user_id,
            rating=cls.rating,
            description=cls.description
        )


class ReviewDtoUpdate(BaseModel):
    rating: Optional[float]
    description: Optional[str]

    @classmethod
    def validate_fields(cls):
        if cls.rating is not None:
            if cls.rating > 5:
                cls.rating = 5
            elif cls.rating < 0:
                cls.rating = 0

        if cls.description is not None and len(cls.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {cls.description}")
        return

    @classmethod
    def to_review(cls, review: Review):
        if cls.rating is None:
            cls.rating = review.rating
        if cls.description is None:
            cls.description = review.description

        return Review(
            id=review.id,
            game_id=review.game_id,
            user_id=review.user_id,
            rating=cls.rating,
            description=cls.description
        )
