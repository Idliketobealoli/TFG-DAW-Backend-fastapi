from typing import List
from bson import ObjectId
from fastapi import HTTPException, status
from dto.wishlist_dto import WishlistDto
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

    async def get_wishlist_by_id(self, wishlist_id: ObjectId) -> WishlistDto:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Wishlist with ID: {wishlist_id} not found.")
        return await WishlistDto.from_wishlist(wishlist, self.user_service, self.game_service)

    async def add_to_wishlist(self, wishlist_id: ObjectId, game_id: ObjectId) -> WishlistDto:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Wishlist with ID: {wishlist_id} not found.")
        wishlist.add_to_wishlist(game_id)
        updated_wishlist = await self.wishlist_repository.update_wishlist(wishlist_id, wishlist.dict())
        if not updated_wishlist:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when adding game with ID: {game_id}.")
        return await WishlistDto.from_wishlist(updated_wishlist, self.user_service, self.game_service)
    
    async def remove_from_wishlist(self, wishlist_id: ObjectId, game_id: ObjectId) -> WishlistDto:
        wishlist = await self.wishlist_repository.get_wishlist_by_id(wishlist_id)
        if not wishlist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Wishlist with ID: {wishlist_id} not found.")
        wishlist.remove_from_wishlist(game_id)
        updated_wishlist = await self.wishlist_repository.update_wishlist(wishlist_id, wishlist.dict())
        if not updated_wishlist:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when removing game with ID: {game_id}.")
        return await WishlistDto.from_wishlist(updated_wishlist, self.user_service, self.game_service)
