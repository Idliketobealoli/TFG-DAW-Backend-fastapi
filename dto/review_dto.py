from bson import ObjectId
from pydantic import BaseModel
from fastapi import HTTPException, status
import datetime
from model.review import Review
from dto.game_dto import GameDto
from dto.user_dto import UserDto
from services.game_service import GameService
from services.user_service import UserService


class ReviewDto(BaseModel):
    id: str
    game: GameDto
    user: UserDto
    publish_date: datetime
    rating: float
    description: str

    @classmethod
    def from_review(cls, review: Review, user_service: UserService, game_service: GameService):
        return ReviewDto(
            id=str(review.id),
            game=game_service.get_game_by_id(review.game_id),
            user=user_service.get_user_by_id(review.user_id),
            publish_date=review.publish_date,
            rating=review.rating,
            description=review.description
        )


class ReviewDtoCreate(BaseModel):
    game_id: ObjectId
    user_id: ObjectId
    publish_date: datetime
    rating: float
    description: str

    @classmethod
    def validate_fields(cls):
        #hacer validador
        return

    @classmethod
    def to_review(cls):
        return Review(
            id=ObjectId(),
            game_id=cls.game_id,
            user_id=cls.user_id,
            publish_date=cls.publish_date,
            rating=cls.rating,
            description=cls.description
        )


class ReviewDtoUpdate(BaseModel):
    rating: float
    description: str

    @classmethod
    def validate_fields(cls):
        #hacer validador
        return
    
    @classmethod
    def to_review(cls, review: Review):
        return Review(
            id=review.id,
            game_id=review.game_id,
            user_id=review.user_id,
            publish_date=datetime.now(),
            rating=cls.rating,
            description=cls.description
        )
    