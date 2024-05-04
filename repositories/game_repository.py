from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.game import Game


class GameRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.game_routes

    async def get_game_by_id(self, game_id: ObjectId) -> Optional[Game]:
        game = await self.collection.find_one({"id": game_id})
        if game:
            return Game(**game)
        return None

    async def get_games(self) -> List[Game]:
        games = await self.collection.find({}).to_list(length=None)
        return [Game(**game) for game in games]

    async def create_game(self, game: Game) -> Optional[Game]:
        await self.collection.insert_one(game.dict())
        return await self.get_game_by_id(game.id)

    async def update_game(self, game_id: ObjectId, game_data: dict) -> Optional[Game]:
        game = await self.collection.find_one({"id": game_id})
        await self.collection.update_one({"_id": game.pop('_id', None)}, {"$set": game_data})
        return await self.get_game_by_id(game_id)

    async def delete_game(self, game_id: ObjectId) -> bool:
        await self.collection.delete_one({"id": game_id})
        game = await self.get_game_by_id(game_id)
        return game is None
