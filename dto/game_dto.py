from bson import ObjectId
from pydantic import BaseModel
from fastapi import HTTPException, status
import datetime
import base64
from typing import Set, Optional
from model.game import Genre, Language, Game


class GameDto(BaseModel):
    id: str
    name: str
    developer: str
    publisher: str
    genres: Set[Genre]
    languages: Set[Language]
    rating: float
    description: str
    release_date: datetime
    sell_number: int
    main_image: Optional[str] = None
    game_showcase_images: Set[str]

    @classmethod
    def from_game(cls, game: Game, main_image_data: bytes = None, game_showcase_images_data: Set[bytes] = set()):
        main_image_data_base64 = None
        if main_image_data:
            main_image_data_base64 = base64.b64encode(main_image_data).decode('utf-8')
        showcase_images_base64 = []
        for image_data in game_showcase_images_data:
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')
            showcase_images_base64.append(image_data_base64)

        return GameDto(
            id=str(game.id),
            name=game.name,
            developer=game.developer,
            publisher=game.publisher,
            genres=game.genres,
            languages=game.languages,
            rating=game.rating,
            description=game.description,
            release_date=game.release_date,
            sell_number=game.sell_number,
            main_image=main_image_data_base64,
            game_showcase_images=showcase_images_base64
        )
    

class GameDtoCreate(BaseModel):
    name: str
    developer: str
    publisher: str
    genres: Set[Genre]
    languages: Set[Language]
    description: str
    release_date: datetime

    @classmethod
    def validate_fields(cls):
        #hacer validador
        return

    @classmethod
    def to_game(cls):
        return Game(
            id=ObjectId(),
            name=cls.name,
            developer=cls.developer,
            publisher=cls.publisher,
            genres=cls.genres,
            languages=cls.languages,
            rating=0,
            description=cls.description,
            release_date=cls.release_date,
            sell_number=0
        )
    

class GameDtoUpdate(BaseModel):
    name: str
    developer: str
    publisher: str
    genres: Set[Genre]
    languages: Set[Language]
    description: str

    @classmethod
    def validate_fields(cls):
        #hacer validador
        return

    @classmethod
    def to_game(cls, game: Game):
        return Game(
            id=game.id,
            name=cls.name,
            developer=cls.developer,
            publisher=cls.publisher,
            genres=cls.genres,
            languages=cls.languages,
            rating=game.rating,
            description=cls.description,
            release_date=game.release_date,
            sell_number=game.sell_number
        )
