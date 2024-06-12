from typing import List
from bson import ObjectId
from fastapi import UploadFile, HTTPException, status
from dto.user_dto import UserDto, UserDtoCreate, UserDtoUpdate, UserDtoShort, UserDtoLogin, UserDtoToken
from repositories.library_repository import LibraryRepository
from repositories.user_repository import UserRepository, get_pfp_by_name
from repositories.wishlist_repository import WishlistRepository
from services import authentication_service, cipher_service


class UserService:
    user_repository = UserRepository()
    library_repository = LibraryRepository()
    wishlist_repository = WishlistRepository()

    async def login(self, user: UserDtoLogin):
        user_from_db = await self.user_repository.get_user_by_username(user.username)
        if user_from_db is None or not cipher_service.match(user.password, user_from_db.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"Unauthorized.")

        token = authentication_service.create_access_token(user_from_db)
        return UserDtoToken(user=await UserDto.from_user(user_from_db), token=token)

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

    async def get_user_by_id_short(self, user_id: ObjectId) -> UserDtoShort:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        return await UserDtoShort.from_user(user)

    async def get_user_pfp_by_id(self, user_id: ObjectId) -> str:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        return get_pfp_by_name(user.profile_picture)

    async def create_user(self, user_dto: UserDtoCreate) -> UserDtoToken:
        user_from_db = await self.user_repository.user_exists_by_username_or_email(user_dto.username, user_dto.email)
        if user_from_db:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User with username ${user_dto.username} or email ${user_dto.email} already "
                                       f"exists.")
        user = await self.user_repository.create_user(user_dto.to_user())
        if not user:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating user: {user_dto.name} {user_dto.surname}.")
        await self.library_repository.create_library(user.id)
        await self.wishlist_repository.create_wishlist(user.id)

        token = authentication_service.create_access_token(user)
        return UserDtoToken(user=await UserDto.from_user(user), token=token)

    async def update_user(self, user_id: ObjectId, user_dto: UserDtoUpdate) -> UserDto:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        updated_user = await self.user_repository.update_user(user_id, user_dto.to_user(user).dict())
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when updating user: {user.name} {user.surname}.")
        return await UserDto.from_user(updated_user)

    async def upload_profile_picture(self, user_id: ObjectId, file: UploadFile) -> bool:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Uploaded file is not an image.")

        return await self.user_repository.upload_image_for_user(file, user_id)

    async def delete_user(self, user_id: ObjectId) -> UserDto:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User with ID: {user_id} not found.")
        deleted_user = await self.user_repository.delete_user(user_id)
        if not deleted_user:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when deleting user: {user.name} {user.surname}.")
        return await UserDto.from_user(deleted_user)