from pydantic import BaseModel
from typing import Set
from model.wishlist import Wishlist
from dto.game_dto import GameDto
from dto.user_dto import UserDto
from services.game_service import GameService
from services.user_service import UserService


class WishlistDto(BaseModel):
    user: UserDto
    games: [GameDto]

    @classmethod
    async def from_wishlist(cls, wishlist: Wishlist, user_service: UserService, game_service: GameService):
        games: [GameDto] = []
        for game_id in wishlist.game_ids:
            game_to_add = await game_service.get_game_by_id(game_id)
            if game_to_add is not None:
                games.append(game_to_add)

        return WishlistDto(
            user=await user_service.get_user_by_id(wishlist.id),
            games=games
        )

    class Config:
        arbitrary_types_allowed = True
