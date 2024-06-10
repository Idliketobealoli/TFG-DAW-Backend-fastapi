from pydantic import BaseModel
from typing import Set
from model.library import Library
from dto.game_dto import GameDto
from dto.user_dto import UserDto
from services.game_service import GameService
from services.user_service import UserService


class LibraryDto(BaseModel):
    user: UserDto
    games: [GameDto]

    @classmethod
    async def from_library(cls, library: Library, user_service: UserService, game_service: GameService):
        games: [GameDto] = []
        for game_id in library.game_ids:
            game_to_add = await game_service.get_game_by_id(game_id)
            if game_to_add is not None:
                games.append(game_to_add)

        return LibraryDto(
            user=await user_service.get_user_by_id(library.id),
            games=games
        )

    class Config:
        arbitrary_types_allowed = True
