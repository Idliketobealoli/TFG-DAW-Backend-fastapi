from enum import Enum
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
    # Añadir price
    id: ObjectId
    name: str
    developer: str
    publisher: str
    genres: [Genre]
    languages: [Language]
    description: str
    release_date: SkipValidation[datetime] = Field(default=datetime.datetime.now())
    sell_number: int = Field(default=0)
    main_image: str = Field(default="base.png")
    game_showcase_images: [str] = Field(default=[])
    file: str = Field(default="")
    visible: bool = Field(default=True)

    class Config:
        arbitrary_types_allowed = True
