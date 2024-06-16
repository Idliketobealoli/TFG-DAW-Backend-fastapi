from bson import ObjectId
from pydantic import BaseModel, SkipValidation
from fastapi import HTTPException, status
import datetime
from typing import Set, Optional
from model.game import Genre, Language, Game, transform_genres, transform_languages
from repositories.review_repository import ReviewRepository


class GameDto(BaseModel):
    id: str
    name: str
    developer: str
    publisher: str
    genres: Set[Genre]
    languages: Set[Language]
    rating: float
    description: str
    price: float
    release_date: SkipValidation[datetime]
    sell_number: int
    game_showcase_images: Set[str]
    visible: bool

    @classmethod
    async def from_game(cls, game: Game, review_repository: ReviewRepository):
        reviews = await review_repository.get_reviews_from_game(game.id)
        rating = 0

        if reviews:
            rating = round(sum(review.rating for review in reviews) / len(reviews), 2)

        return GameDto(
            id=str(game.id),
            name=game.name,
            developer=game.developer,
            publisher=game.publisher,
            genres=game.genres,
            languages=game.languages,
            rating=rating,
            description=game.description,
            price=game.price,
            release_date=game.release_date,
            sell_number=game.sell_number,
            game_showcase_images=game.game_showcase_images,
            visible=game.visible
        )

    class Config:
        arbitrary_types_allowed = True


class GameDtoShort(BaseModel):
    id: str
    name: str
    developer: str
    publisher: str
    rating: float
    description: str
    price: float

    @classmethod
    async def from_game(cls, game: Game, review_repository: ReviewRepository):
        reviews = await review_repository.get_reviews_from_game(game.id)
        rating = 0

        if reviews:
            rating = round(sum(review.rating for review in reviews) / len(reviews), 2)

        return GameDtoShort(
            id=str(game.id),
            name=game.name,
            developer=game.developer,
            publisher=game.publisher,
            rating=rating,
            description=game.description,
            price=game.price
        )


class GameDtoCreate(BaseModel):
    name: str
    developer: str
    publisher: str
    genres: list[str]
    languages: list[str]
    description: str
    release_date: str
    price: float

    def validate_fields(self):
        if len(self.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {self.name}")

        if len(self.developer) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Developer name must be longer than 4 characters: {self.developer}")

        if len(self.publisher) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Publisher name must be longer than 4 characters: {self.publisher}")

        if len(self.genres) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one genre: {self.genres}")

        if len(self.languages) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one language: {self.languages}")

        if len(self.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {self.description}")

        if datetime.datetime.fromisoformat(self.release_date) > datetime.datetime.today():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Release date must not be in the future.")

        if self.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Price must be higher than 0.")

        return

    def to_game(self):
        genres_list = transform_genres(self.genres)
        languages_list = transform_languages(self.languages)

        return Game(
            id=ObjectId(),
            name=self.name,
            developer=self.developer,
            publisher=self.publisher,
            genres=genres_list,
            languages=languages_list,
            description=self.description,
            release_date=datetime.datetime.fromisoformat(self.release_date),
            price=self.price
        )

    class Config:
        arbitrary_types_allowed = True


class GameDtoUpdate(BaseModel):
    name: Optional[str]
    developer: Optional[str]
    publisher: Optional[str]
    price: Optional[float]
    genres: Optional[list[Genre]]
    languages: Optional[list[Language]]
    description: Optional[str]

    def validate_fields(self):
        if self.name is not None and len(self.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {self.name}")

        if self.developer is not None and len(self.developer) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Developer name must be longer than 4 characters: {self.developer}")

        if self.publisher is not None and len(self.publisher) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Publisher name must be longer than 4 characters: {self.publisher}")

        if self.price is not None and self.price <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Price must be a positive number: {self.publisher}")

        if self.genres is not None and len(self.genres) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one genre: {self.genres}")

        if self.languages is not None and len(self.languages) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one language: {self.languages}")

        if self.description is not None and len(self.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {self.description}")
        return

    def to_game(self, game: Game):
        if self.name is None:
            self.name = game.name
        if self.developer is None:
            self.developer = game.developer
        if self.publisher is None:
            self.publisher = game.publisher
        if self.price is None:
            self.price = game.price
        if self.genres is None:
            self.genres = game.genres
        if self.languages is None:
            self.languages = game.languages
        if self.description is None:
            self.description = game.description

        return Game(
            id=game.id,
            name=self.name,
            developer=self.developer,
            publisher=self.publisher,
            genres=self.genres,
            languages=self.languages,
            description=self.description,
            price=self.price,
            release_date=game.release_date,
            sell_number=game.sell_number,
            main_image=game.main_image,
            game_showcase_images=game.game_showcase_images,
            visible=game.visible
        )
