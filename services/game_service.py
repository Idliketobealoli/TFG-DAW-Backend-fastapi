import os
from typing import List, Set, Optional
import aiofiles
from bson import ObjectId
from fastapi import UploadFile, HTTPException, status
from dto.game_dto import GameDto, GameDtoCreate, GameDtoUpdate
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
    
    async def upload_main_image(self, game_id: ObjectId, file: UploadFile):
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            return None
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Uploaded file is not an image.")
        image_data = await file.read()
        _, extension = os.path.splitext(file.filename)
        save_path = os.path.join("..", "resources", "game_images", f"{game_id}.{extension}")

        async with aiofiles.open(save_path, "wb") as image_file:
            await image_file.write(image_data)

        game.main_image = os.path.join("resources", "game_images", f"{game_id}.{extension}")
        updated_game = await self.game_repository.update_game(game_id, game.dict())
        if not updated_game:
            return None
        return GameDto.from_user(updated_game)
    
    async def upload_showcase_images(self, game_id: ObjectId, files: Set[UploadFile]):
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            return None
        for file in files:
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Uploaded file is not an image.")
            image_data = await file.read()
            _, extension = os.path.splitext(file.filename)
            save_path = os.path.join("..", "resources", "game_images", f"{game_id}-img{ObjectId()}.{extension}")

            async with aiofiles.open(save_path, "wb") as image_file:
                await image_file.write(image_data)

            game.game_showcase_images.add(
                os.path.join("resources", "game_images", f"{game_id}-img{ObjectId()}.{extension}"))

        updated_game = await self.game_repository.update_game(game_id, game.dict())
        if not updated_game:
            return None
        return GameDto.from_game(updated_game)

    async def clear_showcase_images(self, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        game.game_showcase_images.clear()
        updated_game = await self.game_repository.update_game(game_id, game.dict())
        return updated_game is not None

    async def delete_game(self, game_id: ObjectId) -> bool:
        game = await self.get_game_by_id(game_id)
        if not game:
            return False
        return await self.game_repository.delete_game(game_id)
