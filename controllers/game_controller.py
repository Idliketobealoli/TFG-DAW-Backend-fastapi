from fastapi import APIRouter, Query, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
from services.game_service import GameService, get_showcase_image
from dto.game_dto import GameDtoCreate, GameDtoUpdate
from model.game import Language, Genre
from bson import ObjectId
from typing import Optional, List

game_routes = APIRouter()
game_service = GameService()


@game_routes.get("/games")
async def get_all_games(
        genre: Optional[Genre] = Query(None),
        language: Optional[Language] = Query(None),
        name: Optional[str] = Query(None),
        publisher: Optional[str] = Query(None),
        developer: Optional[str] = Query(None),
        rating: Optional[float] = Query(None)
):
    games = await game_service.get_all_games()

    if genre:
        games = [game for game in games if genre in game.genres]

    if language:
        games = [game for game in games if language in game.languages]

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
async def get_game_by_id(game_id_str: str):
    return await game_service.get_game_by_id(ObjectId(game_id_str))


@game_routes.post("/games/")
async def post_game(game: GameDtoCreate):
    game.validate_fields()
    if await game_service.get_game_by_name_and_dev(game.name, game.developer):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Already exists a game with the same name and developer.")
    else:
        return await game_service.create_game(game)


@game_routes.put("/games/{game_id_str}")
async def put_game(game_id_str: str, game: GameDtoUpdate):
    game.validate_fields()
    return await game_service.update_game(ObjectId(game_id_str), game)


@game_routes.put("/games/upload_main_img/{game_id_str}")
async def put_game_main_img(game_id_str: str, file: UploadFile = File(...)):
    return await game_service.upload_main_image(ObjectId(game_id_str), file)


@game_routes.put("/games/upload_showcase_imgs/{game_id_str}")
async def put_game_showcases(game_id_str: str, files: List[UploadFile] = File(...)):
    return await game_service.upload_showcase_images(ObjectId(game_id_str), set(files))


@game_routes.put("/games/clear_showcase_imgs/{game_id_str}")
async def clear_game_showcases(game_id_str: str):
    return await game_service.clear_showcase_images(ObjectId(game_id_str))


@game_routes.delete("/games/{game_id_str}")
async def delete_game_by_id(game_id_str: str):
    return await game_service.delete_game(ObjectId(game_id_str))


@game_routes.get("/games/main_image/{game_id_str}")
async def get_game_main_img_by_id(game_id_str: str):
    return FileResponse(await game_service.get_main_image(ObjectId(game_id_str)))


@game_routes.get("/games/showcase_image/{name}")
async def get_showcase_img_by_name(name: str):
    return FileResponse(get_showcase_image(name))


@game_routes.get("/games/download/{game_id_str}")
async def download_game_by_id(game_id_str: str):
    return FileResponse(await game_service.get_download(ObjectId(game_id_str)),
                        content_disposition_type="attachment")


@game_routes.put("/games/upload/{game_id_str}")
async def download_game_by_id(game_id_str: str, file: UploadFile = File(...)):
    return await game_service.upload_game_file(ObjectId(game_id_str), file)
