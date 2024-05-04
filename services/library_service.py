from typing import List, Optional
from bson import ObjectId
from dto.library_dto import LibraryDto, LibraryDtoCreate
from repositories.library_repository import LibraryRepository
from services.game_service import GameService
from services.user_service import UserService


class LibraryService:
    library_repository = LibraryRepository()
    user_service = UserService()
    game_service = GameService()

    async def get_all_libraries(self) -> List[LibraryDto]:
        libraries = await self.library_repository.get_libraries()
        return [await LibraryDto.from_library(library, self.user_service, self.game_service) for library in libraries]

    async def get_library_by_id(self, library_id: ObjectId) -> Optional[LibraryDto]:
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            return None
        return await LibraryDto.from_library(library, self.user_service, self.game_service)
    
    async def get_library_by_user_id(self, user_id: ObjectId) -> Optional[LibraryDto]:
        library = await self.library_repository.get_library_by_user_id(user_id)
        if not library:
            return None
        return await LibraryDto.from_library(library, self.user_service, self.game_service)

    async def create_library(self, library_dto: LibraryDtoCreate) -> Optional[LibraryDto]:
        library = await self.library_repository.create_library(library_dto.to_library())
        if not library:
            return None
        return await LibraryDto.from_library(library, self.user_service, self.game_service)

    async def add_to_library(self, library_id: ObjectId, game_id: ObjectId) -> Optional[LibraryDto]:
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            return None
        library.add_to_library(game_id)
        updated_library = await self.library_repository.update_library(library_id, library.dict())
        if not updated_library:
            return None
        return await LibraryDto.from_library(updated_library, self.user_service, self.game_service)

    async def delete_library(self, library_id: ObjectId) -> bool:
        library = await self.get_library_by_id(library_id)
        if not library:
            return False
        return await self.library_repository.delete_library(library_id)
