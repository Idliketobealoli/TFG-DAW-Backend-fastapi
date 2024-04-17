from bson import ObjectId
from pydantic import BaseModel
from typing import Set
from model.wishlist import Wishlist
from dto.game_dto import GameDto
from dto.user_dto import UserDto
from services.game_service import GameService
from services.user_service import UserService


class WishlistDto(BaseModel):
    id: str
    user: UserDto
    games: Set[GameDto]

    @classmethod
    def from_wishlist(cls, wishlist: Wishlist, user_service: UserService, game_service: GameService):
        game_set: Set[GameDto] = set()
        for id in wishlist.game_ids:
            game_to_add = game_service.get_game_by_id(id)
            if game_to_add is not None:
                game_set.add(game_to_add)

        return WishlistDto(
            id=str(wishlist.id),
            user=user_service.get_user_by_id(wishlist.user_id),
            games=game_set
        )


class WishlistDtoCreate(BaseModel):
    user_id: ObjectId

    @classmethod
    def to_wishlist(cls):
        return Wishlist(
            id=ObjectId(),
            user_id=cls.user_id,
            game_ids=set()
        )
