from pydantic import BaseModel
from bson import ObjectId
from typing import Set


class Library(BaseModel):
    id: ObjectId
    user_id: ObjectId
    game_ids: Set[ObjectId]

    class Config:
        arbitrary_types_allowed = True
