from pydantic import BaseModel
from bson import ObjectId
from typing import Set


class Wishlist(BaseModel):
    id: ObjectId
    user_id: ObjectId
    game_ids: Set[ObjectId]

    @classmethod
    def add_to_wishlist(cls, game_id: ObjectId):
        cls.game_ids.add(game_id)

    @classmethod
    def remove_from_wishlist(cls, game_id: ObjectId):
        cls.game_ids.discard(game_id)

    class Config:
        arbitrary_types_allowed = True
