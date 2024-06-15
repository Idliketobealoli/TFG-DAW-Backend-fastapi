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
        libraries = await self.library_repository.get_libraries()
        return [await LibraryDto.from_library(library, self.user_service, self.game_service) for library in libraries]

    async def get_library_by_id(self, library_id: ObjectId) -> LibraryDto:
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Library with ID: {library_id} not found.")
        return await LibraryDto.from_library(library, self.user_service, self.game_service)

    async def add_to_library(self, library_id: ObjectId, game_id: ObjectId) -> LibraryDto:
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
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Library with ID: {library_id} not found.")

        print(len(library.game_ids))
        return any(gameId == game_id for gameId in library.game_ids)