from typing import List, Optional

from bson import ObjectId

from dto.user_dto import UserDto, UserDtoCreate, UserDtoUpdate
from model.user import Role
from repositories.user_repository import UserRepository


class UserService:
    user_repository = UserRepository()

    async def get_all_users(self) -> List[UserDto]:
        users = await self.user_repository.get_users()
        return [UserDto.from_user(user) for user in users]

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[UserDto]:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        return UserDto.from_user(user)

    async def create_user(self, user_dto: UserDtoCreate) -> Optional[UserDto]:
        user = await self.user_repository.create_user(user_dto.to_user(user_dto))
        if not user:
            return None
        return UserDto.from_user(user)

    async def update_user(self, user_id: ObjectId, user_dto: UserDtoUpdate) -> Optional[UserDto]:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = await self.user_repository.update_user(user_id, user_dto.to_user(user, user_dto).dict())
        if not updated_user:
            return None
        return UserDto.from_user(updated_user)

    async def delete_user(self, user_id: ObjectId) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user or user.role == Role.ADMIN:
            return False
        return await self.user_repository.delete_user(user_id)
