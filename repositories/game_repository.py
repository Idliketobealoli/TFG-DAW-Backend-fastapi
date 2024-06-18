import os
from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.game import Game
from repositories import file_repository


def get_image_by_name(name: str) -> str:
    """
    Función para obtener la ruta absoluta de la imágen cuyo nombre coincida con el pasado por parámetro.
    :param name: Nombre de la imágen del juego a buscar.
    :return: String de la ruta absoluta de la imágen encontrada, o la ruta de una imágen por defecto si no
    se hubiera encontrado la imágen.
    """
    return file_repository.get_file_full_path("game_images", name)


def get_game_downloadable_by_name(name: str) -> str:
    """
    Función para obtener la ruta absoluta del archivo descargable cuyo nombre coincida con el pasado por parámetro.
    :param name: Nombre del archivo del juego a buscar.
    :return: String de la ruta absoluta del archivo encontrado.
    """
    return file_repository.get_file_full_path("game_downloadables", name)


class GameRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.game_routes

    async def get_game_by_id(self, game_id: ObjectId) -> Optional[Game]:
        """
        Función para obtener un juego por su ID.
        :param game_id: ID del juego a buscar.
        :return: El juego encontrado, o None si no existe.
        """
        game = await self.collection.find_one({"id": game_id})
        if game:
            return Game(**game)
        return None

    async def get_game_by_name_and_dev(self, name: str, dev: str) -> Optional[Game]:
        """
        Función para buscar un juego por su nombre y desarrollador.
        :param name: Nombre del juego.
        :param dev: Desarrollador del juego.
        :return: El juego encontrado, o None si no existe ningún juego con ese nombre y desarrollador.
        """
        game = await self.collection.find_one({"name": name, "developer": dev})
        if game:
            return Game(**game)
        return None

    async def get_games(self) -> List[Game]:
        """
        Función para encontrar todos los juegos existentes en la base de datos.
        :return: Lista con todos los juegos.
        """
        games = await self.collection.find({}).to_list(length=None)
        return [Game(**game) for game in games]

    async def create_game(self, game: Game) -> Optional[Game]:
        """
        Función para crear un juego.
        :param game: Información del juego a crear.
        :return: El juego creado, o None si no se pudo crear.
        """
        await self.collection.insert_one(game.dict())
        res = await self.get_game_by_id(game.id)
        return res

    async def update_game(self, game_id: ObjectId, game_data: dict) -> Optional[Game]:
        """
        Función para actualizar la información de un juego existente.
        :param game_id: ID del juego a actualizar.
        :param game_data: Información a actualizar.
        :return: El juego actualizado, o None si no existía.
        """
        game = await self.get_game_by_id(game_id)
        if not game:
            return None
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game_data})
        return await self.get_game_by_id(game_id)

    async def upload_showcase_image(self, file: UploadFile, game_id: ObjectId) -> bool:
        """
        Función para subir una foto de muestra asociada a un juego.
        :param file: Foto de muestra.
        :param game_id: ID del juego al que asociar la foto.
        :return: True si se pudo guardar la imágen y asociarla al juego,
        o False si no se pudo o el juego no existe.
        """
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        filename, _ = os.path.splitext(file.filename)
        image = await file_repository.upload_file(file, "game_images",
                                                  f"{str(game_id)}-showcase{filename}")
        game.game_showcase_images.append(image)
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dict()})
        return True

    async def clear_showcase_images(self, game_id: ObjectId) -> bool:
        """
        Función para borrar todas las fotos de muestra de un juego.
        :param game_id: ID del juego cuyas fotos de muestra queremos eliminar.
        :return: True si se eliminaron exitosamente, o False en caso contrario.
        """
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        for image_path in game.game_showcase_images:
            file_repository.delete_file(os.path.join("game_images", image_path))
        game.game_showcase_images = []
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dict()})
        return True

    async def upload_main_image(self, file: UploadFile, game_id: ObjectId) -> bool:
        """
        Función para subir una nueva foto principal asociada a un juego. Si ya existía, la actualiza.
        :param file: La foto principal.
        :param game_id: El ID del juego al cual asociarla.
        :return: True si se subió correctamente, False si el juego no existe.
        """
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        image = await file_repository.upload_file(file, "game_images", str(game_id))
        game.main_image = image
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dict()})
        return True

    async def upload_game_file(self, file: UploadFile, game_id: ObjectId) -> bool:
        """
        Función para subir un archivo asociado a un juego. Si ya existía, lo actualiza.
        :param file: El archivo del juego.
        :param game_id: El ID del juego al cual asociarlo.
        :return: True si se subió correctamente, False si el juego no existe.
        """
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        image = await file_repository.upload_file(file, "game_downloadables",
                                                  f"{game.name}-{game.developer}".replace(" ", "_"))
        game.file = image
        await self.collection.update_one({"id": game.dict().pop('id', None)},
                                         {"$set": game.dict()})
        return True

    async def delete_game(self, game_id: ObjectId) -> Optional[Game]:
        """
        Función para el borrado lógico de un juego. Si estaba habilitado lo deshabilita,
        y si estaba deshabilitado lo habilita.
        :param game_id: ID del juego a habilitar/deshabilitar.
        :return: El juego modificado, o None si no existía.
        """
        game = await self.get_game_by_id(game_id)
        if not game:
            return None
        game.visible = not game.visible
        await self.collection.update_one({"id": game.dict().pop('id', None)}, {"$set": game.dict()})
        return await self.get_game_by_id(game_id)
