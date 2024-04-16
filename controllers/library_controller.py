from fastapi import APIRouter, Query
from services.library_service import LibraryService
from dto.library_dto import LibraryDtoCreate, LibraryDtoUpdate
from bson import ObjectId
from typing import Optional
import datetime


library_routes = APIRouter()
library_service = LibraryService()


@library_routes.get("/libraries")
async def get_all_libraries():
    return await library_service.get_all_libraries()


@library_routes.get("/libraries/{library_id_str}")
async def get_library_by_id(library_id_str: str):
    return await library_service.get_library_by_id(ObjectId(library_id_str))


@library_routes.get("/libraries/user/{user_id_str}")
async def get_library_by_user_id(user_id_str: str):
    return await library_service.get_library_by_user_id(ObjectId(user_id_str))


@library_routes.post("/libraries/")
async def post_library(library: LibraryDtoCreate):
    return await library_service.create_library(library)


@library_routes.put("/libraries/{library_id_str}")
async def put_library(library_id_str: str, library: LibraryDtoUpdate):
    return await library_service.update_library(ObjectId(library_id_str), library)


@library_routes.delete("/libraries/{library_id_str}")
async def delete_library_by_id(library_id_str: str):
    return await library_service.delete_library(ObjectId(library_id_str))
