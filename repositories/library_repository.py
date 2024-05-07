from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.library import Library


class LibraryRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.library_routes

    async def get_library_by_id(self, library_id: ObjectId) -> Optional[Library]:
        library = await self.collection.find_one({"id": library_id})
        if library:
            return Library(**library)
        return None

    async def get_libraries(self) -> List[Library]:
        libraries = await self.collection.find({}).to_list(length=None)
        return [Library(**library) for library in libraries]

    async def create_library(self, user_id: ObjectId) -> Optional[Library]:
        library = Library(id=user_id, game_ids=set())
        await self.collection.insert_one(library.dict())
        return await self.get_library_by_id(library.id)

    async def update_library(self, library_id: ObjectId, library_data: dict) -> Optional[Library]:
        library = await self.get_library_by_id(library_id)
        if not library:
            return None
        await self.collection.update_one({"id": library.pop('id', None)}, {"$set": library_data})
        return await self.get_library_by_id(library_id)

    # async def delete_library(self, library_id: ObjectId) -> bool:
    #    await self.collection.delete_one({"id": library_id})
    #    library = await self.get_library_by_id(library_id)
    #    return library is None
