from typing import List, Optional
from bson import ObjectId
from fastapi import UploadFile, HTTPException, status
from dto.user_dto import UserDto, UserDtoCreate, UserDtoUpdate
from repositories.library_repository import LibraryRepository
from repositories.user_repository import UserRepository, get_pfp_by_name
from repositories.wishlist_repository import WishlistRepository


class UserService:
    user_repository = UserRepository()
    library_repository = LibraryRepository()
    wishlist_repository = WishlistRepository()

    async def get_all_users(self) -> List[UserDto]:
        users = await self.user_repository.get_users()
        return [await UserDto.from_user(user) for user in users]

    async def get_all_users_active(self, active: bool) -> List[UserDto]:
        users = await self.user_repository.get_users_active(active)
        return [await UserDto.from_user(user) for user in users]

    async def get_user_by_id(self, user_id: ObjectId) -> UserDto:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        return await UserDto.from_user(user)

    async def get_user_pfp_by_id(self, user_id: ObjectId) -> str:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        return get_pfp_by_name(user.profile_picture)

    async def create_user(self, user_dto: UserDtoCreate) -> Optional[UserDto]:
        user = await self.user_repository.create_user(user_dto.to_user())
        if not user:
            return None
        await self.library_repository.create_library(user.id)
        await self.wishlist_repository.create_wishlist(user.id)
        return await UserDto.from_user(user)

    async def update_user(self, user_id: ObjectId, user_dto: UserDtoUpdate) -> Optional[UserDto]:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = await self.user_repository.update_user(user_id, user_dto.to_user(user).dict())
        if not updated_user:
            return None
        return await UserDto.from_user(updated_user)

    async def upload_profile_picture(self, user_id: ObjectId, file: UploadFile):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return False
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Uploaded file is not an image.")

        return await self.user_repository.upload_image_for_user(file, user_id)

    async def delete_user(self, user_id: ObjectId) -> Optional[UserDto]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        deleted_user = await self.user_repository.delete_user(user_id)
        if not deleted_user:
            return None
        return await UserDto.from_user(deleted_user)
