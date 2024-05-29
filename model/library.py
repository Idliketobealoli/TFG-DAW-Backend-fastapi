from pydantic import BaseModel
from bson import ObjectId


class Library(BaseModel):
    id: ObjectId
    game_ids: [ObjectId]

    def add_to_library(self, game_id: ObjectId):
        if game_id not in self.game_ids:
            self.game_ids.append(game_id)

    class Config:
        arbitrary_types_allowed = True
