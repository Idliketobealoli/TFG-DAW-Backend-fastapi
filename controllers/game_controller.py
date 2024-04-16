from fastapi import APIRouter, Query
from services.game_service import GameService
from dto.game_dto import GameDtoCreate, GameDtoUpdate
from model.game import Language, Genre
from bson import ObjectId
from typing import Optional


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
    return await game_service.create_game(game)


@game_routes.put("/games/{game_id_str}")
async def post_game(game_id_str: str, game: GameDtoUpdate):
    return await game_service.update_game(ObjectId(game_id_str), game)


@game_routes.delete("/games/{game_id_str}")
async def get_game_by_id(game_id_str: str):
    return await game_service.delete_game(ObjectId(game_id_str))
