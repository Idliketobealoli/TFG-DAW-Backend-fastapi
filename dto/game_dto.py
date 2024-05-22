from pydantic import BaseModel, SkipValidation
from fastapi import HTTPException, status
import datetime
from typing import Set, Optional
from model.game import Genre, Language, Game
from repositories.game_repository import get_game_image_by_name, get_showcase_images_by_names
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
    release_date: SkipValidation[datetime]
    sell_number: int
    main_image: bytes
    game_showcase_images: Set[bytes]
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
            release_date=game.release_date,
            sell_number=game.sell_number,
            main_image=await get_game_image_by_name(game.main_image),
            game_showcase_images=await get_showcase_images_by_names(game.game_showcase_images),
            visible=game.visible
        )

    class Config:
        arbitrary_types_allowed = True


class GameDtoCreate(BaseModel):
    name: str
    developer: str
    publisher: str
    genres: Set[Genre]
    languages: Set[Language]
    description: str
    release_date: SkipValidation[datetime]

    @classmethod
    def validate_fields(cls):
        if len(cls.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {cls.name}")

        if len(cls.developer) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Developer name must be longer than 4 characters: {cls.developer}")

        if len(cls.publisher) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Publisher name must be longer than 4 characters: {cls.publisher}")

        if len(cls.genres) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one genre: {cls.genres}")

        if len(cls.languages) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one language: {cls.languages}")

        if len(cls.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {cls.description}")

        if cls.release_date > datetime.datetime.today:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Release date must not be in the future.")
        return

    @classmethod
    def to_game(cls):
        return Game(
            name=cls.name,
            developer=cls.developer,
            publisher=cls.publisher,
            genres=cls.genres,
            languages=cls.languages,
            description=cls.description,
            release_date=cls.release_date
        )

    class Config:
        arbitrary_types_allowed = True


class GameDtoUpdate(BaseModel):
    name: Optional[str]
    developer: Optional[str]
    publisher: Optional[str]
    genres: Optional[Set[Genre]]
    languages: Optional[Set[Language]]
    description: Optional[str]

    @classmethod
    def validate_fields(cls):
        if cls.name is not None and len(cls.name) < 2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Name must be longer than 1 character: {cls.name}")

        if cls.developer is not None and len(cls.developer) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Developer name must be longer than 4 characters: {cls.developer}")

        if cls.publisher is not None and len(cls.publisher) < 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Publisher name must be longer than 4 characters: {cls.publisher}")

        if cls.genres is not None and len(cls.genres) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one genre: {cls.genres}")

        if cls.languages is not None and len(cls.languages) < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"There must be at least one language: {cls.languages}")

        if cls.description is not None and len(cls.description) < 10:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Description must be longer than 9 characters: {cls.description}")
        return

    @classmethod
    def to_game(cls, game: Game):
        if cls.name is None:
            cls.name = game.name
        if cls.developer is None:
            cls.developer = game.developer
        if cls.publisher is None:
            cls.publisher = game.publisher
        if cls.genres is None:
            cls.genres = game.genres
        if cls.languages is None:
            cls.languages = game.languages
        if cls.description is None:
            cls.description = game.description

        return Game(
            id=game.id,
            name=cls.name,
            developer=cls.developer,
            publisher=cls.publisher,
            genres=cls.genres,
            languages=cls.languages,
            description=cls.description,
            release_date=game.release_date,
            sell_number=game.sell_number,
            main_image=game.main_image,
            game_showcase_images=game.game_showcase_images,
            visible=game.visible
        )
