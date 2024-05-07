from enum import Enum
from pydantic import BaseModel, SkipValidation
from bson import ObjectId
import datetime
from typing import Optional


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


class Game(BaseModel):
    id: ObjectId
    name: str
    developer: str
    publisher: str
    genres: [Genre]
    languages: [Language]
    rating: float
    description: str
    release_date: SkipValidation[datetime]
    sell_number: int
    main_image: Optional[str] = None
    game_showcase_images: [str]
    visible: bool

    class Config:
        arbitrary_types_allowed = True
