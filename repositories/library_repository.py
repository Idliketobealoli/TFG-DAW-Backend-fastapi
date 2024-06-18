from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.library import Library


class LibraryRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.library_routes

    async def get_library_by_id(self, library_id: ObjectId) -> Optional[Library]:
        """
        Función para obtener una librería por el ID del usuario al que está asignada.
        :param library_id: ID del usuario cuya librería queremos encontrar.
        :return: La librería si existe, o None en caso contrario.
        """
        library = await self.collection.find_one({"id": library_id})
        if library:
            return Library(**library)
        return None

    async def get_libraries(self) -> List[Library]:
        """
        Función para obtener todas las librerías existentes.
        :return: Lista con todas las librerías.
        """
        libraries = await self.collection.find({}).to_list(length=None)
        return [Library(**library) for library in libraries]

    async def create_library(self, user_id: ObjectId) -> Optional[Library]:
        """
        Función para crear una librería y asociarla con el usuario cuyo ID coincida con el pasado por parámetro.
        :param user_id: ID del usuario a quien asignar la librería.
        :return: La librería creada, o None si no se pudo crear.
        """
        library = Library(id=user_id, game_ids=[])
        await self.collection.insert_one(library.dict())
        return await self.get_library_by_id(library.id)

    async def update_library(self, library_id: ObjectId, library_data: dict) -> Optional[Library]:
        """
        Función para modificar la librería asociada con el usuario cuyo ID coincida con el pasado por parámetro.
        :param library_id: ID del usuario cuya librería queremos modificar.
        :param library_data: Datos de la librería.
        :return: La librería modificada, o None si no existía.
        """
        library = await self.get_library_by_id(library_id)
        if not library:
            return None
        await self.collection.update_one({"id": library.dict().pop('id', None)}, {"$set": library_data})
        return await self.get_library_by_id(library_id)
