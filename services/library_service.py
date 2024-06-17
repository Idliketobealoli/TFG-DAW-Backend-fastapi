from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from dto.library_dto import LibraryDto
from repositories.library_repository import LibraryRepository
from services.game_service import GameService
from services.user_service import UserService
from services.wishlist_service import WishlistService


class LibraryService:
    library_repository = LibraryRepository()
    user_service = UserService()
    game_service = GameService()
    wishlist_service = WishlistService()

    async def get_all_libraries(self) -> List[LibraryDto]:
        """
        Función encargada de devolver todas las librerías existentes.
        :return: Lista con todas las librerías existentes como DTOs.
        """
        libraries = await self.library_repository.get_libraries()
        return [await LibraryDto.from_library(library, self.user_service, self.game_service) for library in libraries]

    async def get_library_by_id(self, library_id: ObjectId) -> LibraryDto:
        """
        Función encargada de conseguir la librería del usuario cuyo ID coincide con el pasado por parámetro.
        :param library_id: ID del usuario cuya librería queremos buscar.
        :return: DTO de la librería del usuario, o 404 si no existe.
        """
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Library with ID: {library_id} not found.")
        return await LibraryDto.from_library(library, self.user_service, self.game_service)

    async def add_to_library(self, library_id: ObjectId, game_id: ObjectId) -> LibraryDto:
        """
        Función para añadir el juego cuyo ID coincide con el pasado por parámetro a la librería del usuario
        cuyo ID coincide con el pasado por parámetro.
        :param library_id: ID del usuario cuya librería queremos buscar.
        :param game_id: ID del juego que queremos añadir.
        :return: DTO de la librería actualizada, 404 si no existe o 503 si no se pudo modificar.
        """
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Library with ID: {library_id} not found.")
        library.add_to_library(game_id)
        updated_library = await self.library_repository.update_library(library_id, library.dict())
        if not updated_library:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when adding game with ID: {game_id}.")
        await self.wishlist_service.remove_from_wishlist(library_id, game_id)
        return await LibraryDto.from_library(updated_library, self.user_service, self.game_service)

    async def is_in_library(self, library_id: ObjectId, game_id: ObjectId) -> bool:
        """
        Función para determinar si el juego cuyo ID coincide con el pasado por parámetro está presente en la
        librería del usuario cuyo ID coincide con el pasado por parámetro.
        :param library_id: ID del usuario cuya librería queremos buscar.
        :param game_id: ID del juego que queremos buscar.
        :return: True si el juego está en la librería, False si no lo está, o 404 si no existe la librería.
        """
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Library with ID: {library_id} not found.")

        return any(gameId == game_id for gameId in library.game_ids)
