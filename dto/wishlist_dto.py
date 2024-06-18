from pydantic import BaseModel
from model.wishlist import Wishlist
from dto.game_dto import GameDtoShort
from dto.user_dto import UserDtoShort
from services.game_service import GameService
from services.user_service import UserService


class WishlistDto(BaseModel):
    user: UserDtoShort
    games: [GameDtoShort]

    @classmethod
    async def from_wishlist(cls, wishlist: Wishlist, user_service: UserService, game_service: GameService):
        games: [GameDtoShort] = []
        for game_id in wishlist.game_ids:
            game_to_add = await game_service.get_game_by_id_short(game_id)
            if game_to_add is not None:
                games.append(game_to_add)

        return WishlistDto(
            user=await user_service.get_user_by_id_short(wishlist.id),
            games=games
        )

    class Config:
        arbitrary_types_allowed = True
