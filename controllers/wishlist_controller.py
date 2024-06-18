from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from services.authentication_service import check_role, check_role_and_myself
from services.wishlist_service import WishlistService
from bson import ObjectId

wishlist_routes = APIRouter()
wishlist_service = WishlistService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@wishlist_routes.get("/wishlists")
async def get_all_wishlists(token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener todas las listas de deseados.
    ESTE ENDPOINT NO LO USAMOS, PERO SE DEJA POR MOTIVOS DE ESCALABILIDAD,
    POR SI EN UN FUTURO PUDIERA SER NECESARIO.
    :param token: Token del usuario.
    :return: Todas las listas de deseados existentes, o un error de autenticación o autorización.
    """
    check_role(["ADMIN"], token)
    return await wishlist_service.get_all_wishlists()


@wishlist_routes.get("/wishlists/{wishlist_id_str}")
async def get_wishlist_by_id(wishlist_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener una lista de deseados por el ID del usuario al que está asociada.
    :param wishlist_id_str: ID del usuario al que pertenece la lista de deseados.
    :param token: Token del usuario.
    :return: La lista de deseados encontrada, 404 si no existe, o un error de autenticación o autorización.
    """
    check_role_and_myself(["ADMIN", "USER"], token, wishlist_id_str)
    return await wishlist_service.get_wishlist_by_id(ObjectId(wishlist_id_str))


@wishlist_routes.get("/wishlists/exists/{user_id}")
async def wishlist_exists_by_id(user_id: str, game_id: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para comprobar si un juego está presente en la lista de deseados de un usuario.
    :param user_id: ID del usuario.
    :param game_id: ID del juego.
    :param token: Token del usuario.
    :return: {"exists": True} si está presente, {"exists": False} si no lo está,
    404 si la lista de deseados no existe, o un error de autenticación o autorización.
    """
    check_role_and_myself(["ADMIN", "USER"], token, user_id)
    wishlist = await wishlist_service.get_wishlist_by_id(ObjectId(user_id))
    game_exists = any(game.id.__str__() == game_id for game in wishlist.games)
    return {"exists": game_exists}


@wishlist_routes.put("/wishlists/add_game/{wishlist_id_str}")
async def add_to_wishlist(wishlist_id_str: str, game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para añadir un juego a la lista de deseados de un usuario.
    :param wishlist_id_str: ID del usuario.
    :param game_id_str: ID del juego.
    :param token: Token del usuario.
    :return: La lista de deseados actualizada, o una Response de error.
    """
    check_role_and_myself(["ADMIN", "USER"], token, wishlist_id_str)
    return await wishlist_service.add_to_wishlist(ObjectId(wishlist_id_str), ObjectId(game_id_str))


@wishlist_routes.put("/wishlists/remove_game/{wishlist_id_str}")
async def remove_from_wishlist(wishlist_id_str: str, game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para eliminar un juego de la lista de deseados de un usuario.
    :param wishlist_id_str: ID del usuario.
    :param game_id_str: ID del juego.
    :param token: Token del usuario.
    :return: La lista de deseados actualizada, o una Response de error.
    """
    check_role_and_myself(["ADMIN", "USER"], token, wishlist_id_str)
    return await wishlist_service.remove_from_wishlist(ObjectId(wishlist_id_str), ObjectId(game_id_str))
