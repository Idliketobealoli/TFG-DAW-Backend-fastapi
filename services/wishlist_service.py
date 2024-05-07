from typing import List, Optional
from bson import ObjectId
from dto.wishlist_dto import WishlistDto, WishlistDtoCreate
from repositories.wishlist_repository import WishlistRepository
from services.game_service import GameService
from services.user_service import UserService


class WishlistService:
    wishlist_repository = WishlistRepository()
    user_service = UserService()
    game_service = GameService()

    async def get_all_wishlists(self) -> List[WishlistDto]:
        wishlists = await self.wishlist_repository.get_wishlists()
        return [await WishlistDto.from_wishlist(wishlist, self.user_service, self.game_service)
                for wishlist in wishlists]

    async def get_wishlist_by_id(self, wishlist_id: ObjectId) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return None
        return await WishlistDto.from_wishlist(wishlist, self.user_service, self.game_service)

    async def add_to_wishlist(self, wishlist_id: ObjectId, game_id: ObjectId) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return None
        wishlist.add_to_wishlist(game_id)
        updated_wishlist = await self.wishlist_repository.update_wishlist(wishlist_id, wishlist.dict())
        if not updated_wishlist:
            return None
        return await WishlistDto.from_wishlist(updated_wishlist, self.user_service, self.game_service)
    
    async def remove_from_wishlist(self, wishlist_id: ObjectId, game_id: ObjectId) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return None
        wishlist.remove_from_wishlist(game_id)
        updated_wishlist = await self.wishlist_repository.update_wishlist(wishlist_id, wishlist.dict())
        if not updated_wishlist:
            return None
        return await WishlistDto.from_wishlist(updated_wishlist, self.user_service, self.game_service)

    # async def delete_wishlist(self, wishlist_id: ObjectId) -> bool:
    #    wishlist = await self.get_wishlist_by_id(wishlist_id)
    #    if not wishlist:
    #        return False
    #    return await self.wishlist_repository.delete_wishlist(wishlist_id)
