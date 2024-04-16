from typing import List, Optional

from bson import ObjectId

from dto.library_dto import LibraryDto, LibraryDtoCreate, LibraryDtoUpdate
from repositories.library_repository import LibraryRepository


class LibraryService:
    library_repository = LibraryRepository()

    async def get_all_libraries(self) -> List[LibraryDto]:
        libraries = await self.library_repository.get_libraries()
        return [LibraryDto.from_library(library) for library in libraries]

    async def get_library_by_id(self, library_id: ObjectId) -> Optional[LibraryDto]:
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            return None
        return LibraryDto.from_library(library)
    
    async def get_library_by_user_id(self, user_id: ObjectId) -> Optional[LibraryDto]:
        library = await self.library_repository.get_library_by_user_id(user_id)
        if not library:
            return None
        return LibraryDto.from_library(library)

    async def create_library(self, library_dto: LibraryDtoCreate) -> Optional[LibraryDto]:
        library = await self.library_repository.create_library(library_dto.to_library())
        if not library:
            return None
        return LibraryDto.from_library(library)

    async def update_library(self, library_id: ObjectId, library_dto: LibraryDtoUpdate) -> Optional[LibraryDto]:
        library = await self.library_repository.get_library_by_id(library_id)
        if not library:
            return None
        updated_library = await self.library_repository.update_library(library_id, library_dto.to_library(library).dict())
        if not updated_library:
            return None
        return LibraryDto.from_library(updated_library)

    async def delete_library(self, library_id: ObjectId) -> bool:
        library = await self.get_library_by_id(library_id)
        if not library:
            return False
        return await self.library_repository.delete_library(library_id)
