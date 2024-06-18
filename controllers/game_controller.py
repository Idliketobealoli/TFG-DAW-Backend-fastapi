from fastapi import APIRouter, Query, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from services.authentication_service import check_role
from services.game_service import GameService, get_showcase_image
from dto.game_dto import GameDtoCreate, GameDtoUpdate
from model.game import Language, Genre, transform_genres, transform_languages
from bson import ObjectId
from typing import Optional, List
from services.library_service import LibraryService

game_routes = APIRouter()
game_service = GameService()
library_service = LibraryService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@game_routes.get("/games")
async def get_all_games(
        genre: Optional[str] = Query(None),
        language: Optional[str] = Query(None),
        name: Optional[str] = Query(None),
        publisher: Optional[str] = Query(None),
        developer: Optional[str] = Query(None),
        rating: Optional[float] = Query(None),
        visible: Optional[bool] = Query(None),
        token: str = Depends(oauth2_scheme)
):
    """
    Endpoint para obtener todos los juegos, o todos aquellos que cumplan con todos los filtros, si están.
    :param genre: Género por el que filtrar.
    :param language: Lenguaje por el que filtrar.
    :param name: Nombre por el que filtrar.
    :param publisher: Publisher por el que filtrar.
    :param developer: Desarrollador por el que filtrar.
    :param rating: Calificación mínima por la que filtrar.
    :param visible: Estado por el que filtrar.
    :param token: Token del usuario.
    :return: Lista de todos los juegos, o de todos aquellos que cumplen todos los filtros.
    """
    check_role(["ADMIN", "USER"], token)
    games = await game_service.get_all_games()

    if visible:
        games = [game for game in games if visible == game.visible]

    if genre:
        games = [game for game in games if transform_genres([genre])[0] in game.genres]

    if language:
        games = [game for game in games if transform_languages([language])[0] in game.languages]

    if name is not None and name.strip():
        games = [game for game in games if name.strip().lower() in game.name.strip().lower()]

    if publisher is not None and publisher.strip():
        games = [game for game in games if publisher.strip().lower() in game.publisher.strip().lower()]

    if developer is not None and developer.strip():
        games = [game for game in games if developer.strip().lower() in game.developer.strip().lower()]

    if rating is not None:
        games = [game for game in games if game.rating >= rating]

    return games


@game_routes.get("/games/{game_id_str}")
async def get_game_by_id(game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener un juego por su ID.
    :param game_id_str: ID del juego a buscar.
    :param token: Token del usuario.
    :return: El juego encontrado, o una Response de error.
    """
    check_role(["ADMIN", "USER"], token)
    return await game_service.get_game_by_id(ObjectId(game_id_str))


@game_routes.post("/games/")
async def post_game(game: GameDtoCreate, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para crear un nuevo juego.
    :param game: DTO con los datos necesarios para crear un juego.
    :param token: Token del usuario.
    :return: El juego creado, o una Response de error.
    """
    check_role(["ADMIN"], token)
    game.validate_fields()
    if await game_service.get_game_by_name_and_dev(game.name, game.developer):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already exists a game with the same name and developer.")
    else:
        return await game_service.create_game(game)


@game_routes.put("/games/{game_id_str}")
async def put_game(game_id_str: str, game: GameDtoUpdate, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para modificar un juego existente.
    :param game_id_str: ID del juego a modificar.
    :param game: DTO con los datos a modificar.
    :param token: Token del usuario.
    :return: El juego modificado, o una Response de error.
    """
    check_role(["ADMIN"], token)
    game.validate_fields()
    return await game_service.update_game(ObjectId(game_id_str), game)


@game_routes.put("/games/upload_main_img/{game_id_str}")
async def put_game_main_img(game_id_str: str, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    """
    Endpoint para subir o modificar la imágen principal de un juego.
    :param game_id_str: ID del juego cuya imágen principal queremos modificar.
    :param file: Imágen principal.
    :param token: Token del usuario.
    :return: True si se modificó exitosamente, False en caso contrario o una Response de error.
    """
    check_role(["ADMIN"], token)
    return await game_service.upload_main_image(ObjectId(game_id_str), file)


@game_routes.put("/games/upload_showcase_imgs/{game_id_str}")
async def put_game_showcases(game_id_str: str, files: List[UploadFile] = File(...),
                             token: str = Depends(oauth2_scheme)):
    """
    Endpoint para subir una lista de imágenes de muestra para un juego.
    :param game_id_str: ID del juego al cual le queremos agregar imágenes de muestra.
    :param files: Lista de imágenes de muestra.
    :param token: Token del usuario.
    :return: El juego actualizado, o una Response de error.
    """
    check_role(["ADMIN"], token)
    return await game_service.upload_showcase_images(ObjectId(game_id_str), set(files))


@game_routes.delete("/games/clear_showcase_imgs/{game_id_str}")
async def clear_game_showcases(game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para borrar todas las imágenes de la lista de imágenes de muestra de un juego.
    :param game_id_str: ID del juego.
    :param token: Token del usuario.
    :return: True si fueron eliminadas con éxito, False si no se pudieron eliminar o una Response de error.
    """
    print("entra")
    check_role(["ADMIN"], token)
    return await game_service.clear_showcase_images(ObjectId(game_id_str))


@game_routes.delete("/games/{game_id_str}")
async def delete_game_by_id(game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para habilitar/deshabilitar un juego por su ID. Borrado lógico.
    :param game_id_str: ID del juego.
    :param token: Token del usuario.
    :return: El juego modificado, o una Response de error.
    """
    check_role(["ADMIN"], token)
    return await game_service.delete_game(ObjectId(game_id_str))


@game_routes.get("/games/main_image/{game_id_str}")
async def get_game_main_img_by_id(game_id_str: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener la imágen principal de un juego.
    :param game_id_str: ID del juego.
    :param token: Token del usuario.
    :return: La imágen principal del juego, o una por defecto, o una Response de error.
    """
    check_role(["ADMIN", "USER"], token)
    return FileResponse(await game_service.get_main_image(ObjectId(game_id_str)))


@game_routes.get("/games/showcase_image/{name}")
async def get_showcase_img_by_name(name: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener la imágen de muestra de un juego por el nombre de la imágen.
    :param name: Nombre de la imágen a buscar.
    :param token: Token del usuario.
    :return: La imágen de muestra, o una por defecto, o una Response de error.
    """
    check_role(["ADMIN", "USER"], token)
    return FileResponse(get_showcase_image(name))


@game_routes.get("/games/download/{game_id_str}")
async def download_game_by_id(game_id_str: str, user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener el archivo de un juego y agregarlo a la librería del usuario.
    :param game_id_str: ID del juego.
    :param user_id: ID del usuario.
    :param token: Token del usuario.
    :return: El archivo del juego, o una Response de error.
    """
    check_role(["ADMIN", "USER"], token)
    fileResponse = FileResponse(await game_service.get_download(ObjectId(game_id_str)),
                                content_disposition_type="attachment")

    # Si lo descargamos correctamente, lo agregamos a la libreria
    if fileResponse.status_code >= 200 & fileResponse.status_code < 300:
        await library_service.add_to_library(ObjectId(user_id), ObjectId(game_id_str))

    return fileResponse


@game_routes.put("/games/upload/{game_id_str}")
async def upload_game_by_id(game_id_str: str, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    """
    Endpoint para subir un archivo y asociarlo con un juego.
    :param game_id_str: ID del juego.
    :param file: Archivo del juego.
    :param token: Token del usuario.
    :return: True si se subió correctamente, False si no se pudo, o una Response de error.
    """
    check_role(["ADMIN"], token)
    return await game_service.upload_game_file(ObjectId(game_id_str), file)


@game_routes.get("/genres")
def get_genres(token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener todos los géneros de videojuegos soportados.
    :param token: Token del usuario.
    :return: Lista con todos los géneros disponibles.
    """
    check_role(["ADMIN", "USER"], token)
    return list(Genre)


@game_routes.get("/languages")
def get_languages(token: str = Depends(oauth2_scheme)):
    """
    Endpoint para obtener todos los lenguajes de videojuegos soportados.
    :param token: Token del usuario.
    :return: Lista con todos los lenguajes disponibles.
    """
    check_role(["ADMIN", "USER"], token)
    return list(Language)
