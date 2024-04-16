from fastapi import APIRouter, Query
from services.user_service import UserService
from dto.user_dto import UserDtoCreate, UserDtoUpdate
from bson import ObjectId
from typing import Optional


user_routes = APIRouter()
user_service = UserService()


@user_routes.get("/prueba")
def hello_world():
    return "hello world!"


@user_routes.get("/users")
async def get_all_users(active: Optional[bool] = Query(None)):
    if (active is None):
        return await user_service.get_all_users()
    else:
        return await user_service.get_all_users_active(active)


@user_routes.get("/users/{user_id_str}")
async def get_user_by_id(user_id_str: str):
    return await user_service.get_user_by_id(ObjectId(user_id_str))


@user_routes.post("/users/")
async def post_user(user: UserDtoCreate):
    #user.
    return await user_service.create_user(user)


@user_routes.put("/users/{user_id_str}")
async def post_user(user_id_str: str, user: UserDtoUpdate):
    return await user_service.update_user(ObjectId(user_id_str), user)


@user_routes.delete("/users/{user_id_str}")
async def get_user_by_id(user_id_str: str):
    return await user_service.delete_user(ObjectId(user_id_str))
