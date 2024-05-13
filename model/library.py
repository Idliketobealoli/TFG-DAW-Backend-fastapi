from pydantic import BaseModel
from bson import ObjectId
from typing import Set


class Library(BaseModel):
    id: ObjectId
    game_ids: Set[ObjectId]

    @classmethod
    def add_to_library(cls, game_id: ObjectId):
        cls.game_ids.add(game_id)

    class Config:
        arbitrary_types_allowed = True
