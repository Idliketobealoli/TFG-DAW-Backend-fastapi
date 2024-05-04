import os
from typing import List, Optional
import aiofiles
from bson import ObjectId
from fastapi import UploadFile, HTTPException, status
from dto.user_dto import UserDto, UserDtoCreate, UserDtoUpdate
from repositories.user_repository import UserRepository


class UserService:
    user_repository = UserRepository()

    async def get_all_users(self) -> List[UserDto]:
        users = await self.user_repository.get_users()
        return [UserDto.from_user(user) for user in users]

    async def get_all_users_active(self, active: bool) -> List[UserDto]:
        users = await self.user_repository.get_users_active(active)
        return [UserDto.from_user(user) for user in users]

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[UserDto]:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        return UserDto.from_user(user)

    async def create_user(self, user_dto: UserDtoCreate) -> Optional[UserDto]:
        user = await self.user_repository.create_user(user_dto.to_user())
        if not user:
            return None
        return UserDto.from_user(user)

    async def update_user(self, user_id: ObjectId, user_dto: UserDtoUpdate) -> Optional[UserDto]:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = await self.user_repository.update_user(user_id, user_dto.to_user(user).dict())
        if not updated_user:
            return None
        return UserDto.from_user(updated_user)

    async def upload_profile_picture(self, user_id: ObjectId, file: UploadFile):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Uploaded file is not an image.")
        image_data = await file.read()
        _, extension = os.path.splitext(file.filename)
        save_path = os.path.join("..", "resources", "user_pfp", f"{user_id}.{extension}")

        async with aiofiles.open(save_path, "wb") as image_file:
            await image_file.write(image_data)

        user.profile_picture = os.path.join("resources", "user_pfp", f"{user_id}.{extension}")
        updated_user = await self.user_repository.update_user(user_id, user.dict())
        if not updated_user:
            return None
        return UserDto.from_user(updated_user)
        # image_id = await db.upload_file(image_data)
        # user.profile_picture = image_id
        # updated_user = await self.user_repository.update_user(user_id, user.dict())
        # if not updated_user:
        #    return None
        # return UserDto.from_user(updated_user)

    async def delete_user(self, user_id: ObjectId) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        return await self.user_repository.delete_user(user_id)
