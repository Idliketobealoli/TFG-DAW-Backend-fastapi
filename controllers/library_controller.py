from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from services.authentication_service import check_role, check_role_and_myself
from services.library_service import LibraryService
from bson import ObjectId


library_routes = APIRouter()
library_service = LibraryService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@library_routes.get("/libraries")
async def get_all_libraries(token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener todas las librerías.
    ESTE ENDPOINT NO LO USAMOS, PERO SE DEJA POR MOTIVOS DE ESCALABILIDAD,
    POR SI EN UN FUTURO PUDIERA SER NECESARIO.
    :param token: Token del usuario.
    :return: Todas las librerías existentes.
    """
    check_role(["ADMIN"], token)
    return await library_service.get_all_libraries()


@library_routes.get("/libraries/{library_id_str}")
async def get_library_by_id(library_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener una librería por el ID del usuario al que está asociada.
    :param library_id_str: ID del usuario al que está asociada la librería.
    :param token: Token del usuario.
    :return: La librería, o una Response de error.
    """
    check_role_and_myself(["ADMIN", "USER"], token, library_id_str)
    return await library_service.get_library_by_id(ObjectId(library_id_str))


@library_routes.put("/libraries/add_game/{library_id_str}")
async def add_to_library(library_id_str: str, game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para añadir un juego a una librería.
    :param library_id_str: ID del usuario asociado a la librería.
    :param game_id_str: ID del juego.
    :param token: Token del usuario.
    :return: La librería actualizada, o una Response de error.
    """
    check_role_and_myself(["ADMIN", "USER"], token, library_id_str)
    return await library_service.add_to_library(ObjectId(library_id_str), ObjectId(game_id_str))
