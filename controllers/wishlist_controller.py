from fastapi import APIRouter, Query
from services.wishlist_service import WishlistService
from dto.wishlist_dto import WishlistDtoCreate, WishlistDtoUpdate
from bson import ObjectId
from typing import Optional
import datetime


wishlist_routes = APIRouter()
wishlist_service = WishlistService()


@wishlist_routes.get("/wishlists")
async def get_all_wishlists():
    return await wishlist_service.get_all_wishlists()


@wishlist_routes.get("/wishlists/{wishlist_id_str}")
async def get_wishlist_by_id(wishlist_id_str: str):
    return await wishlist_service.get_wishlist_by_id(ObjectId(wishlist_id_str))


@wishlist_routes.get("/wishlists/user/{user_id_str}")
async def get_wishlist_by_user_id(user_id_str: str):
    return await wishlist_service.get_wishlist_by_user_id(ObjectId(user_id_str))


@wishlist_routes.post("/wishlists/")
async def post_wishlist(wishlist: WishlistDtoCreate):
    return await wishlist_service.create_wishlist(wishlist)


@wishlist_routes.put("/wishlists/{wishlist_id_str}")
async def put_wishlist(wishlist_id_str: str, wishlist: WishlistDtoUpdate):
    return await wishlist_service.update_wishlist(ObjectId(wishlist_id_str), wishlist)


@wishlist_routes.delete("/wishlists/{wishlist_id_str}")
async def delete_wishlist_by_id(wishlist_id_str: str):
    return await wishlist_service.delete_wishlist(ObjectId(wishlist_id_str))
