from bson import ObjectId
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException, status
import datetime
from typing import Set
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

    @classmethod
    def from_game(cls, game: Game):
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
            sell_number=game.sell_number
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
