from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.wishlist import Wishlist


class WishlistRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.wishlist_routes

    async def get_wishlist_by_id(self, wishlist_id: ObjectId) -> Optional[Wishlist]:
        """
        Función para buscar una lista de deseados por el ID del usuario al que corresponde.
        :param wishlist_id: ID del usuario a quien pertenece la lista de deseados.
        :return: La lista de deseados del usuario, o None si no existe.
        """
        wishlist = await self.collection.find_one({"id": wishlist_id})
        if wishlist:
            return Wishlist(**wishlist)
        return None

    async def get_wishlists(self) -> List[Wishlist]:
        """
        Función para obtener todas las listas de deseados.
        :return: Una lista con todas las listas de deseados.
        """
        wishlists = await self.collection.find({}).to_list(length=None)
        return [Wishlist(**wishlist) for wishlist in wishlists]

    async def create_wishlist(self, user_id: ObjectId) -> Optional[Wishlist]:
        """
        Función para crear una lista de deseados para el usuario con el ID correspondiente.
        :param user_id: ID del usuario para el cual queremos crear la lista.
        :return: La lista de deseados creada, o None si no se pudo crear.
        """
        wishlist = Wishlist(id=user_id, game_ids=[])
        await self.collection.insert_one(wishlist.dict())
        return await self.get_wishlist_by_id(wishlist.id)

    async def update_wishlist(self, wishlist_id: ObjectId, wishlist_data: dict) -> Optional[Wishlist]:
        """
        Función para actualizar la información de la lista de deseados del usuario
        cuyo ID corresponda con el pasado por parámetro.
        :param wishlist_id: ID del usuario cuya lista de deseados queremos actualizar.
        :param wishlist_data: Datos nuevos de la lista de deseados.
        :return: La lista de deseados actualizada, o None si no se pudo actualizar o no existía.
        """
        wishlist = await self.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return None
        await self.collection.update_one({"id": wishlist.dict().pop('id', None)}, {"$set": wishlist_data})
        return await self.get_wishlist_by_id(wishlist_id)
