from fastapi import APIRouter, Query, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from services.authentication_service import decode_access_token, check_role, check_role_and_myself
from services.user_service import UserService
from dto.user_dto import UserDtoCreate, UserDtoUpdate, UserDtoLogin
from bson import ObjectId
from typing import Optional

user_routes = APIRouter()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_routes.get("/prueba")
def hello_world():
    return "hello world!"


@user_routes.get("/users")
async def get_all_users(active: Optional[bool] = Query(None), token: str = Depends(oauth2_scheme)):
    check_role(["ADMIN"], token)

    if active is None:
        return await user_service.get_all_users()
    else:
        return await user_service.get_all_users_active(active)


@user_routes.get("/users/{user_id_str}")
async def get_user_by_id(user_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role(["ADMIN", "USER"], token)
    return await user_service.get_user_by_id(ObjectId(user_id_str))


@user_routes.get("/users/pfp/{user_id_str}")
async def get_user_pfp_by_id(user_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role(["ADMIN", "USER"], token)
    return FileResponse(await user_service.get_user_pfp_by_id(ObjectId(user_id_str)))


@user_routes.post("/register")
async def post_user(user: UserDtoCreate):
    user.validate_fields()
    return await user_service.create_user(user)


@user_routes.post("/login")
async def login(user: UserDtoLogin):
    return await user_service.login(user)


@user_routes.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

    return await user_service.get_user_by_id(ObjectId(payload["id"]))


@user_routes.put("/users/{user_id_str}")
async def put_user(user_id_str: str, user: UserDtoUpdate, token: str = Depends(oauth2_scheme)):
    check_role_and_myself(["ADMIN", "USER"], token, user_id_str)
    user.validate_fields()
    return await user_service.update_user(ObjectId(user_id_str), user)


@user_routes.put("/users/upload_pfp/{user_id_str}")
async def put_user_pfp(user_id_str: str, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    check_role_and_myself(["ADMIN", "USER"], token, user_id_str)
    return await user_service.upload_profile_picture(ObjectId(user_id_str), file)


@user_routes.delete("/users/{user_id_str}")
async def delete_user_by_id(user_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role_and_myself(["ADMIN", "USER"], token, user_id_str)
    return await user_service.delete_user(ObjectId(user_id_str))
