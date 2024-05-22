import base64
import os

from fastapi import UploadFile, File
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.game import Game
from repositories import file_repository


async def get_game_image_by_name(name: str) -> bytes:
    return await file_repository.get_file(os.path.join("game_images", name))


async def get_showcase_images_by_names(names: [str]) -> [bytes]:
    result = []
    for name in names:
        # result.append(base64.b64encode(await file_repository.get_file(
        #    os.path.join("game_images", name))).decode('utf-8'))
        result.append(await file_repository.get_file(os.path.join("game_images", name)))
    return result


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
        game = await self.get_game_by_id(game_id)
        if not game:
            return None
        await self.collection.update_one({"id": game.pop('id', None)},
                                         {"$set": game_data})  # Si no funciona, cambiar por _id
        return await self.get_game_by_id(game_id)

    async def upload_showcase_image(self, file: UploadFile, game_id: ObjectId):
        game = await self.get_game_by_id(game_id)
        if not game:
            return
        image = await file_repository.upload_file(file, "game_images",
                                                  f"{str(game_id)}-showcase{str(ObjectId())}")
        game.game_showcase_images.append(image)
        await self.collection.update_one({"id": game.pop('id', None)},
                                         {"$set": game.dir()})  # Si no funciona, cambiar por _id

    async def clear_showcase_images(self, game_id: ObjectId):
        game = await self.get_game_by_id(game_id)
        if not game:
            return

    async def upload_main_image(self, file: UploadFile, game_id: ObjectId) -> Optional[Game]:
        game = await self.get_game_by_id(game_id)
        if not game:
            return None
        image = await file_repository.upload_file(file, "game_images", str(game_id))
        game.main_image = image
        await self.collection.update_one({"id": game.pop('id', None)},
                                         {"$set": game.dir()})  # Si no funciona, cambiar por _id
        return await self.get_game_by_id(game_id)

    async def delete_game(self, game_id: ObjectId) -> Optional[Game]:
        game = await self.get_game_by_id(game_id)
        if not game:
            return None
        game.visible = False
        await self.collection.update_one({"id": game.pop('id', None)}, {"$set": game})  # Lo mismo aqui
        return await self.get_game_by_id(game_id)
        # await self.collection.delete_one({"id": game_id})
        # game = await self.get_game_by_id(game_id)
        # return game is None
