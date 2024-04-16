from typing import List, Optional

from bson import ObjectId

from dto.wishlist_dto import WishlistDto, WishlistDtoCreate, WishlistDtoUpdate
from repositories.wishlist_repository import WishlistRepository


class WishlistService:
    wishlist_repository = WishlistRepository()

    async def get_all_wishlists(self) -> List[WishlistDto]:
        wishlists = await self.wishlist_repository.get_wishlists()
        return [WishlistDto.from_wishlist(wishlist) for wishlist in wishlists]

    async def get_wishlist_by_id(self, wishlist_id: ObjectId) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return None
        return WishlistDto.from_wishlist(wishlist)
    
    async def get_wishlist_by_user_id(self, user_id: ObjectId) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.get_wishlist_by_user_id(user_id)
        if not wishlist:
            return None
        return WishlistDto.from_wishlist(wishlist)

    async def create_wishlist(self, wishlist_dto: WishlistDtoCreate) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.create_wishlist(wishlist_dto.to_wishlist())
        if not wishlist:
            return None
        return WishlistDto.from_wishlist(wishlist)

    async def update_wishlist(self, wishlist_id: ObjectId, wishlist_dto: WishlistDtoUpdate) -> Optional[WishlistDto]:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return None
        updated_wishlist = await self.wishlist_repository.update_wishlist(wishlist_id, wishlist_dto.to_wishlist(wishlist).dict())
        if not updated_wishlist:
            return None
        return WishlistDto.from_wishlist(updated_wishlist)

    async def delete_wishlist(self, wishlist_id: ObjectId) -> bool:
        wishlist = await self.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            return False
        return await self.wishlist_repository.delete_wishlist(wishlist_id)
