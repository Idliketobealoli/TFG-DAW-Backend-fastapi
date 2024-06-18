from enum import Enum
from typing import List
from fastapi import HTTPException, status
from pydantic import BaseModel, SkipValidation, Field
from bson import ObjectId
import datetime


class Genre(str, Enum):
    ARPG = "ARPG"
    RPG = "RPG"
    STRATEGY = "Strategy"
    FPS = "FPS"
    TPS = "TPS"
    ROGUELIKE = "Rogue-like"
    METROIDVANIA = "Metroidvania"
    PUZZLE = "Puzzle"
    PLATFORMER = "Platformer"
    PLUS18 = "18+"
    FAMILY = "Family"
    RACING = "Racing"
    SPORTS = "Sports"
    MOBA = "Moba"
    SINGLEPLAYER = "Singleplayer"
    MULTIPLAYER = "Multiplayer"
    FARMING = "Farming"
    MMO = "MMO"
    VN = "Visual Novel"
    GACHA = "Gacha"
    CASUAL = "Casual"
    SOULSLIKE = "Souls-like"


def transform_genres(genres: List[str]) -> List[Genre]:
    """
    Función para, dada una lista de strings, transformarlos en Enums de géneros.
    :param genres: Lista de Strings de los géneros.
    :return: Lista de Enums de géneros, o error 400 si alguno no tiene el formato correcto.
    """
    transformed_genres = []
    for genre in genres:
        try:
            transformed_genres.append(Genre(genre))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Unexpected genre.")
    return transformed_genres


class Language(str, Enum):
    ES = "Spanish"
    EN = "English"
    FR = "French"
    GM = "German"
    IT = "Italian"
    CN = "Chinese"
    JP = "Japanese"
    KR = "Korean"
    RU = "Russian"
    GR = "Greek"
    PG = "Portuguese"


def transform_languages(languages: List[str]) -> List[Language]:
    """
    Función para, dada una lista de strings, transformarlos en Enums de lenguajes.
    :param languages: Lista de Strings de los lenguajes.
    :return: Lista de Enums de lenguajes, o error 400 si alguno no tiene el formato correcto.
    """
    transformed_languages = []
    for language in languages:
        try:
            transformed_languages.append(Language(language))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Unexpected language.")
    return transformed_languages


class Game(BaseModel):
    id: ObjectId
    name: str
    developer: str
    publisher: str
    genres: [Genre]
    languages: [Language]
    description: str
    price: float
    release_date: SkipValidation[datetime] = Field(default=datetime.datetime.now())
    sell_number: int = Field(default=0)
    main_image: str = Field(default="base.png")
    game_showcase_images: [str] = Field(default=[])
    file: str = Field(default="")
    visible: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True
