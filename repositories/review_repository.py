from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from db.database import db
from model.review import Review


class ReviewRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.review_routes

    async def get_review_by_id(self, review_id: ObjectId) -> Optional[Review]:
        """
        Función para obtener una review por su ID.
        :param review_id: ID de la review a buscar.
        :return: La review si existe, o None en caso contrario.
        """
        review = await self.collection.find_one({"id": review_id})
        if review:
            return Review(**review)
        return None

    async def get_reviews(self) -> List[Review]:
        """
        Función para obtener todas las reviews de la base de datos.
        :return: Lista con todas las reviews existentes.
        """
        reviews = await self.collection.find({}).to_list(length=None)
        return [Review(**review) for review in reviews]
    
    async def get_reviews_from_user(self, user_id: ObjectId) -> List[Review]:
        """
        Función para obtener todas las reviews realizadas por el usuario cuyo ID
        coincida con el pasado por parámetro.
        :param user_id: ID del usuario cuyas reviews queremos buscar.
        :return: Lista con todas las reviews asociadas a ese usuario.
        """
        reviews = await self.collection.find({"user_id": user_id}).to_list(length=None)
        return [Review(**review) for review in reviews]

    async def get_reviews_from_user_and_game(self, user_id: ObjectId, game_id: ObjectId) -> Optional[Review]:
        """
        Función para obtener una review asociada a un usuario y juego específicos.
        :param user_id: ID del usuario a filtrar.
        :param game_id: ID del juego a filtrar.
        :return: La review si existe, o None en caso contrario.
        """
        review = await self.collection.find_one({"user_id": user_id, "game_id": game_id})
        if review:
            return Review(**review)
        return None
    
    async def get_reviews_from_game(self, game_id: ObjectId) -> List[Review]:
        """
        Función para obtener todas las reviews asociadas a un juego.
        :param game_id: ID del juego a filtrar.
        :return: Lista con todas las reviews asociadas a ese juego.
        """
        reviews = await self.collection.find({"game_id": game_id}).to_list(length=None)
        return [Review(**review) for review in reviews]

    async def create_review(self, review: Review) -> Optional[Review]:
        """
        Función para crear una nueva review.
        :param review: Datos de la nueva review.
        :return: Review insertada, o None si no se pudo insertar.
        """
        await self.collection.insert_one(review.dict())
        return await self.get_review_by_id(review.id)

    async def update_review(self, review_id: ObjectId, review_data: dict) -> Optional[Review]:
        """
        Función para actualizar los datos de una review existente.
        :param review_id: ID de la review a actualizar.
        :param review_data: Datos de la review.
        :return: Review modificada, o None si no existía.
        """
        review = await self.get_review_by_id(review_id)
        if not review:
            return None
        await self.collection.update_one({"id": review.dict().pop('id', None)}, {"$set": review_data})
        return await self.get_review_by_id(review_id)

    async def delete_review(self, review_id: ObjectId) -> bool:
        """
        Función para borrar físicamente una review.
        :param review_id: ID de la review a borrar.
        :return: True si consiguió borrarla, False en caso contrario.
        """
        await self.collection.delete_one({"id": review_id})
        review = await self.get_review_by_id(review_id)
        return review is None
