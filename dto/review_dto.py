from bson import ObjectId
from pydantic import BaseModel, SkipValidation
from fastapi import HTTPException, status
import datetime
from dto.game_dto import GameDtoShort
from dto.user_dto import UserDtoShort
from model.review import Review
from repositories.game_repository import GameRepository
from repositories.user_repository import UserRepository
from typing import Optional


class ReviewDto(BaseModel):
    id: str
    game: GameDtoShort
    user: UserDtoShort
    publish_date: SkipValidation[datetime]
    rating: float
    description: str

    @classmethod
    async def from_review(cls, review: Review, user_repository: UserRepository, game_repository: GameRepository):
        game_model = await game_repository.get_game_by_id(review.game_id)
        user_model = await user_repository.get_user_by_id(review.user_id)
        return ReviewDto(
            id=str(review.id),
            game=await GameDtoShort.from_game(game_model),
            user=await UserDtoShort.from_user(user_model),
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

    def validate_fields(self):
        if self.rating > 5:
            self.rating = 5
        elif self.rating < 0:
            self.rating = 0

        if len(self.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {self.description}")
        return

    def to_review(self):
        return Review(
            id=ObjectId(),
            game_id=self.game_id,
            user_id=self.user_id,
            rating=self.rating,
            description=self.description
        )


class ReviewDtoUpdate(BaseModel):
    rating: Optional[float]
    description: Optional[str]

    def validate_fields(self):
        if self.rating is not None:
            if self.rating > 5:
                self.rating = 5
            elif self.rating < 0:
                self.rating = 0

        if self.description is not None and len(self.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {self.description}")
        return

    def to_review(self, review: Review):
        if self.rating is None:
            self.rating = review.rating
        if self.description is None:
            self.description = review.description

        return Review(
            id=review.id,
            game_id=review.game_id,
            user_id=review.user_id,
            rating=self.rating,
            description=self.description
        )
