from bson import ObjectId
from pydantic import BaseModel, SkipValidation
from fastapi import HTTPException, status
import datetime
from model.review import Review
from dto.game_dto import GameDto
from dto.user_dto import UserDto
from services.game_service import GameService
from services.user_service import UserService
from typing import Optional


class ReviewDto(BaseModel):
    id: str
    game: GameDto
    user: UserDto
    publish_date: SkipValidation[datetime]
    rating: float
    description: str

    @classmethod
    async def from_review(cls, review: Review, user_service: UserService, game_service: GameService):
        return ReviewDto(
            id=str(review.id),
            game=await game_service.get_game_by_id(review.game_id),
            user=await user_service.get_user_by_id(review.user_id),
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
            id=ObjectId(),
            game_id=cls.game_id,
            user_id=cls.user_id,
            publish_date=datetime.datetime.now(),
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
            publish_date=datetime.datetime.now(),
            rating=cls.rating,
            description=cls.description
        )
    