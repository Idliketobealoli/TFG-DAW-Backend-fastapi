import os
from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.game import Game
from repositories import file_repository


def get_image_by_name(name: str) -> str:
    return file_repository.get_file_full_path("game_images", name)


def get_game_downloadable_by_name(name: str) -> str:
    return file_repository.get_file_full_path("game_downloadables", name)


class GameRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.game_routes

    async def get_game_by_id(self, game_id: ObjectId) -> Optional[Game]:
        game = await self.collection.find_one({"id": game_id})
        if game:
            return Game(**game)
        return None

    async def get_game_by_name_and_dev(self, name: str, dev: str) -> Optional[Game]:
        game = await self.collection.find_one({"name": name, "developer": dev})
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
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game_data})  # Si no funciona, cambiar por _id
        return await self.get_game_by_id(game_id)

    async def upload_showcase_image(self, file: UploadFile, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        filename, _ = os.path.splitext(file.filename)
        image = await file_repository.upload_file(file, "game_images",
                                                  f"{str(game_id)}-showcase{filename}")
        game.game_showcase_images.add(image)
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dir()})  # Si no funciona, cambiar por _id
        return True

    async def clear_showcase_images(self, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        for image_path in game.game_showcase_images:
            file_repository.delete_file(os.path.join("game_images", image_path))
        game.game_showcase_images = []
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dir()})  # Si no funciona, cambiar por _id
        return True

    async def upload_main_image(self, file: UploadFile, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        image = await file_repository.upload_file(file, "game_images", str(game_id))
        game.main_image = image
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dir()})  # Si no funciona, cambiar por _id
        return True

    async def upload_game_file(self, file: UploadFile, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        image = await file_repository.upload_file(file, "game_downloadables",
                                                  f"{game.name}-{game.developer}".replace(" ", "_"))
        game.main_image = image
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dir()})  # Si no funciona, cambiar por _id
        return True

    async def delete_game(self, game_id: ObjectId) -> Optional[Game]:
        game = await self.get_game_by_id(game_id)
        if not game:
            return None
        game.visible = False
        await self.collection.update_one({"id": game.dict().pop('id', None)}, {"$set": game.dict()})  # Lo mismo aqui
        return await self.get_game_by_id(game_id)
