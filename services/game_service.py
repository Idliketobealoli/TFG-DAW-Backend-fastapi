from typing import List, Optional

from bson import ObjectId

from dto.game_dto import GameDto, GameDtoCreate, GameDtoUpdate
from model.game import Language, Genre
from repositories.game_repository import GameRepository


class GameService:
    game_repository = GameRepository()

    async def get_all_games(self) -> List[GameDto]:
        games = await self.game_repository.get_games()
        return [GameDto.from_game(game) for game in games]

    async def get_game_by_id(self, game_id: ObjectId) -> Optional[GameDto]:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            return None
        return GameDto.from_game(game)

    async def create_game(self, game_dto: GameDtoCreate) -> Optional[GameDto]:
        game = await self.game_repository.create_game(game_dto.to_game())
        if not game:
            return None
        return GameDto.from_game(game)

    async def update_game(self, game_id: ObjectId, game_dto: GameDtoUpdate) -> Optional[GameDto]:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            return None
        updated_game = await self.game_repository.update_game(game_id, game_dto.to_game(game).dict())
        if not updated_game:
            return None
        return GameDto.from_game(updated_game)

    async def delete_game(self, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        return await self.game_repository.delete_game(game_id)
