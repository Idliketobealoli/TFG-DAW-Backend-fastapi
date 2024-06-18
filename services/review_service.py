from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, status
from dto.review_dto import ReviewDto, ReviewDtoCreate, ReviewDtoUpdate
from repositories.game_repository import GameRepository
from repositories.review_repository import ReviewRepository
from repositories.user_repository import UserRepository
from services.authentication_service import check_role_and_myself


class ReviewService:
    review_repository = ReviewRepository()
    user_repository = UserRepository()
    game_repository = GameRepository()

    async def get_all_reviews(self) -> List[ReviewDto]:
        """
        Función para obtener todas las reviews existentes, ordenadas por fecha de publicación.
        :return: Lista de ReviewDto ordenada por fecha de publicación.
        """
        reviews = await self.review_repository.get_reviews()
        return [await ReviewDto.from_review(review, self.user_repository, self.game_repository, self.review_repository)
                for review in sorted(reviews, key=lambda r: r.publish_date)]
    
    async def get_all_reviews_from_user(self, user_id: ObjectId) -> List[ReviewDto]:
        """
        Función para obtener todas las reviews pertenecientes al usuario cuyo ID coincida
        con el pasado por parámetro, ordenadas por fecha de publicación.
        :param user_id: ID del usuario cuyas reviews queremos buscar.
        :return: Lista de ReviewDto ordenada por fecha de publicación.
        """
        reviews = await self.review_repository.get_reviews_from_user(user_id)
        return [await ReviewDto.from_review(review, self.user_repository, self.game_repository, self.review_repository)
                for review in sorted(reviews, key=lambda r: r.publish_date)]

    async def get_review_from_user_and_game(self, user_id: ObjectId, game_id: ObjectId) -> Optional[ReviewDto]:
        """
        Función para obtener una review hecha por el usuario cuyo ID coincida con el pasado por parámetro para el
        jugo cuyo ID coincida con el pasado por parámetro.
        :param user_id: ID del usuario cuya review queremos buscar.
        :param game_id: ID del juego cuya review queremos buscar.
        :return: El DTO de la review, o None si no existe.
        """
        review = await self.review_repository.get_reviews_from_user_and_game(user_id, game_id)
        if review:
            return await ReviewDto.from_review(review, self.user_repository, self.game_repository,
                                               self.review_repository)
        return None

    async def get_all_reviews_from_game(self, game_id: ObjectId) -> List[ReviewDto]:
        """
        Función para obtener todas las reviews pertenecientes al juego cuyo ID coincida
        con el pasado por parámetro, ordenadas por fecha de publicación.
        :param game_id: ID del juego cuyas reviews queremos buscar.
        :return: Lista de ReviewDto ordenada por fecha de publicación.
        """
        reviews = await self.review_repository.get_reviews_from_game(game_id)
        return [await ReviewDto.from_review(review, self.user_repository, self.game_repository, self.review_repository)
                for review in sorted(reviews, key=lambda r: r.publish_date)]

    async def get_review_by_id(self, review_id: ObjectId) -> ReviewDto:
        """
        Función para obtener una review por ID.
        :param review_id: ID de la review que queremos buscar.
        :return: El DTO de la review, o 404 si no existe.
        """
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with ID: {review_id} not found.")
        return await ReviewDto.from_review(review, self.user_repository, self.game_repository, self.review_repository)

    async def create_review(self, review_dto: ReviewDtoCreate) -> ReviewDto:
        """
        Función para crear una nueva review a partir de un DTO de creación.
        :param review_dto: DTO con la información necesaria para crear una nueva review.
        :return: DTO de la review creada, o 503 si no se pudo crear.
        """
        review = await self.review_repository.create_review(review_dto.to_review())
        if not review:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating review for user with ID: "
                                       f"{review_dto.user_id} and game with ID: {review_dto.game_id}.")
        return await ReviewDto.from_review(review, self.user_repository, self.game_repository, self.review_repository)

    async def update_review(self, review_id: ObjectId, review_dto: ReviewDtoUpdate) -> ReviewDto:
        """
        Función para actualizar una review ya existente a partir de un DTO de edición.
        :param review_id: ID de la review a modificar.
        :param review_dto: DTO con la información necesaria para modificar una review.
        :return: DTO de la review modificada, 404 si no existía previamente o 503 si no se pudo modificar.
        """
        review = await self.review_repository.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with ID: {review_id} not found.")
        updated_review = await self.review_repository.update_review(review_id, review_dto.to_review(review).dict())
        if not updated_review:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating review for user with ID: "
                                       f"{review_dto.user_id} and game with ID: {review_dto.game_id}.")
        return await ReviewDto.from_review(updated_review, self.user_repository,
                                           self.game_repository, self.review_repository)

    async def delete_review(self, review_id: ObjectId, token: str) -> bool:
        """
        Función para el borrado físico de una review.
        :param review_id: ID de la review que queremos borrar.
        :param token: Token del usuario que ha realizado la llamada.
        :return: True si la review fue borrada exitosamente, False si no se pudo borrar,
        404 si la review no existe, 401 si el token es inválido o 403 si no tiene uno de los roles permitidos.
        """
        review = await self.get_review_by_id(review_id)
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Review with ID: {review_id} not found.")

        # ES NECESARIO LLEVARSE EL TOKEN A DENTRO DEL MÉTODO DEL SERVICIO PORQUE PARA CHEQUEAR SI ERES EL MISMO
        # USUARIO QUE EL QUE HIZO LA REVIEW PRIMERO TIENES QUE BUSCAR LA REVIEW POR ID.
        check_role_and_myself(["ADMIN", "USER"], token, review.user.id)
        return await self.review_repository.delete_review(review_id)
