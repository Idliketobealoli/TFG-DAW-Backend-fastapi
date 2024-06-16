import os.path
from typing import List, Set
from bson import ObjectId
from fastapi import UploadFile, HTTPException, status
from dto.game_dto import GameDto, GameDtoCreate, GameDtoUpdate, GameDtoShort
from repositories.game_repository import GameRepository, get_game_downloadable_by_name, get_image_by_name
from repositories.review_repository import ReviewRepository


def get_showcase_image(name: str):
    return get_image_by_name(name)


class GameService:
    game_repository = GameRepository()
    review_repository = ReviewRepository()

    async def get_all_games(self) -> List[GameDto]:
        games = await self.game_repository.get_games()
        return sorted([await GameDto.from_game(game, self.review_repository) for game in games],
                      key=lambda game_dto: game_dto.release_date, reverse=True)

    async def get_game_by_id(self, game_id: ObjectId) -> GameDto:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return await GameDto.from_game(game, self.review_repository)

    async def get_game_by_id_short(self, game_id: ObjectId) -> GameDtoShort:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return await GameDtoShort.from_game(game, self.review_repository)

    async def get_game_by_name_and_dev(self, name: str, dev: str) -> GameDto | None:
        game = await self.game_repository.get_game_by_name_and_dev(name, dev)
        if not game:
            return None
        return await GameDto.from_game(game, self.review_repository)

    async def create_game(self, game_dto: GameDtoCreate) -> GameDto:
        game = await self.game_repository.create_game(game_dto.to_game())
        if not game:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating game: {game_dto.name} -"
                                       f" {game_dto.developer}.")
        print("ha creado el juego")
        return await GameDto.from_game(game, self.review_repository)

    async def update_game(self, game_id: ObjectId, game_dto: GameDtoUpdate) -> GameDto:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        updated_game = await self.game_repository.update_game(game_id, game_dto.to_game(game).dict())
        if not updated_game:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when updating game: {game_dto.name} -"
                                       f" {game_dto.developer}.")
        return await GameDto.from_game(game, self.review_repository)
    
    async def upload_main_image(self, game_id: ObjectId, file: UploadFile) -> bool:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Uploaded file is not an image.")

        return await self.game_repository.upload_main_image(file, game_id)
    
    async def upload_showcase_images(self, game_id: ObjectId, files: Set[UploadFile]) -> GameDto:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        for file in files:
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Uploaded file is not an image.")

            await self.game_repository.upload_showcase_image(file, game_id)

        updated_game = await self.game_repository.get_game_by_id(game_id)
        if not updated_game:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when updating game with ID: {game_id}.")
        return await GameDto.from_game(updated_game, self.review_repository)

    async def clear_showcase_images(self, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        deleted_images = await self.game_repository.clear_showcase_images(game_id)
        if deleted_images:
            game.game_showcase_images.clear()
            updated_game = await self.game_repository.update_game(game_id, game.dict())
            return updated_game is not None
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when clearing the showcase images of "
                                       f"game with ID: {game_id}.")
    
    async def upload_game_file(self, game_id: ObjectId, file: UploadFile) -> bool:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return await self.game_repository.upload_game_file(file, game_id)

    async def delete_game(self, game_id: ObjectId) -> GameDto:
        game = await self.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        deleted_game = await self.game_repository.delete_game(game_id)
        if not deleted_game:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when deleting game with ID: {game_id}.")
        return await GameDto.from_game(deleted_game, self.review_repository)

    async def get_download(self, game_id: ObjectId) -> str:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        file = get_game_downloadable_by_name(game.file)
        if os.path.isfile(file):
            game.sell_number += 1
            await self.game_repository.update_game(game_id, game.dict())
            return file
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"File for game with ID: {game_id} not found. {file} is not a file.")

    async def get_main_image(self, game_id: ObjectId) -> str:
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return get_image_by_name(game.main_image)
