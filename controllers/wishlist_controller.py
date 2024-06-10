from fastapi import APIRouter
from services.wishlist_service import WishlistService
from bson import ObjectId

wishlist_routes = APIRouter()
wishlist_service = WishlistService()


@wishlist_routes.get("/wishlists")
async def get_all_wishlists():
    return await wishlist_service.get_all_wishlists()


@wishlist_routes.get("/wishlists/{wishlist_id_str}")
async def get_wishlist_by_id(wishlist_id_str: str):
    return await wishlist_service.get_wishlist_by_id(ObjectId(wishlist_id_str))


@wishlist_routes.get("/wishlists/exists/{user_id}")
async def get_wishlist_by_id(user_id: str, game_id: str):
    wishlist = await wishlist_service.get_wishlist_by_id(ObjectId(user_id))
    print(f"{ObjectId("60a7b2f7c0f2b441d4f6e9b1") == "60a7b2f7c0f2b441d4f6e9b1"}")
    print(f"{ObjectId("60a7b2f7c0f2b441d4f6e9b1").__str__() == "60a7b2f7c0f2b441d4f6e9b1"}")
    game_exists = any(game.id.__str__() == game_id for game in wishlist.games)
    return {"exists": game_exists}


@wishlist_routes.put("/wishlists/add_game/{wishlist_id_str}")
async def add_to_wishlist(wishlist_id_str: str, game_id_str: str):
    return await wishlist_service.add_to_wishlist(ObjectId(wishlist_id_str), ObjectId(game_id_str))


@wishlist_routes.put("/wishlists/remove_game/{wishlist_id_str}")
async def remove_from_wishlist(wishlist_id_str: str, game_id_str: str):
    return await wishlist_service.remove_from_wishlist(ObjectId(wishlist_id_str), ObjectId(game_id_str))
