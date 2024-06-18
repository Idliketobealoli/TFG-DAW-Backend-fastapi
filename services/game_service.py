import os.path
from typing import List, Set
from bson import ObjectId
from fastapi import UploadFile, HTTPException, status
from dto.game_dto import GameDto, GameDtoCreate, GameDtoUpdate, GameDtoShort
from repositories.game_repository import GameRepository, get_game_downloadable_by_name, get_image_by_name
from repositories.review_repository import ReviewRepository


def get_showcase_image(name: str):
    """
    Función que devuelve el path completo de la imágen guardada que coincida con ese nombre,
    o el de una imágen por defecto si no existe.
    :param name: el nombre de la imágen que queremos.
    :return: string con la ruta absoluta de la imágen.
    """
    return get_image_by_name(name)


class GameService:
    game_repository = GameRepository()
    review_repository = ReviewRepository()

    async def get_all_games(self) -> List[GameDto]:
        """
        Función que obtiene todos los juegos de la base de datos como una lista de DTO de juegos,
        ordenados por su fecha de lanzamiento.
        :return: Lista de GameDto ordenada por fecha de lanzamiento.
        """
        games = await self.game_repository.get_games()
        return sorted([await GameDto.from_game(game, self.review_repository) for game in games],
                      key=lambda game_dto: game_dto.release_date, reverse=True)

    async def get_game_by_id(self, game_id: ObjectId) -> GameDto:
        """
        Función que obtiene el juego cuyo ID coincida con el pasado por parámetro.
        :param game_id: ID del juego que queremos buscar.
        :return: El DTO del juego, o 404 si no existe.
        """
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return await GameDto.from_game(game, self.review_repository)

    async def get_game_by_id_short(self, game_id: ObjectId) -> GameDtoShort:
        """
        Función que obtiene el juego cuyo ID coincida con el pasado por parámetro,
        pero con una cantidad reducida de campos.
        :param game_id: ID del juego que queremos buscar.
        :return: El DTO corto del juego, o 404 si no existe.
        """
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return await GameDtoShort.from_game(game, self.review_repository)

    async def get_game_by_name_and_dev(self, name: str, dev: str) -> GameDto | None:
        """
        Función que busca un juego por nombre y desarrollador.
        :param name: Nombre del juego
        :param dev: Desarrollador del juego
        :return: El DTO del juego encontrado, o None si no encontró ninguno.
        """
        game = await self.game_repository.get_game_by_name_and_dev(name, dev)
        if not game:
            return None
        return await GameDto.from_game(game, self.review_repository)

    async def create_game(self, game_dto: GameDtoCreate) -> GameDto:
        """
        Función que inserta un juego en la base de datos.
        :param game_dto: DTO de creación del juego.
        :return: DTO del juego creado, o 503 si hay un error al crear el juego.
        """
        game = await self.game_repository.create_game(game_dto.to_game())
        if not game:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail=f"There was an error when creating game: {game_dto.name} -"
                                       f" {game_dto.developer}.")
        return await GameDto.from_game(game, self.review_repository)

    async def update_game(self, game_id: ObjectId, game_dto: GameDtoUpdate) -> GameDto:
        """
        Función que actualiza los datos del juego cuyo ID coincida con el pasado por parámetro.
        :param game_id: ID del juego que queremos modificar.
        :param game_dto: Datos a modificar del juego.
        :return: DTO del juego modificado, o 404 si el juego no existe, o 503 si no se pudo modificar.
        """
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
        """
        Función para subir la imágen principal del juego cuyo ID coincida con el pasado por parámetro.
        :param game_id: ID del juego al cual le queremos asignar la imágen.
        :param file: Imágen del juego.
        :return: True si ha subido la imágen exitosamente, False si no se pudo subir correctamente,
        404 si el juego no existe o 400 si el archivo no es una imágen.
        """
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Uploaded file is not an image.")

        return await self.game_repository.upload_main_image(file, game_id)
    
    async def upload_showcase_images(self, game_id: ObjectId, files: Set[UploadFile]) -> GameDto:
        """
        Función para subir las imágenes de muestra del juego cuyo ID coincida con el pasado por parámetro.
        :param game_id: ID del juego al cual le queremos asignar las imágenes.
        :param files: Imágenes del juego.
        :return: DTO con los datos actualizados, 404 si el juego no existe, 400 si algún archivo no es una imágen
        o 503 si no pudo actualizar el juego.
        """
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
        """
        Función para quitar todas las imágenes de muestra del juego cuyo ID coincida con el pasado por parámetro.
        :param game_id: ID del juego cuyas imágenes de muestra queremos eliminar.
        :return: True si las imágenes fueron correctamente eliminadas, 404 si el juego no existe o 503 si hubo un error
        a la hora de eliminar las imágenes (como no poder conectar con la base de datos).
        """
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
        """
        Función para subir el archivo del juego cuyo ID coincida con el pasado por parámetro.
        :param game_id: ID del juego al cual le queremos asignar la imágen.
        :param file: Archivo del juego.
        :return: True si ha subido el archivo exitosamente, False si no se pudo subir correctamente,
        o 404 si el juego no existe.
        """
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return await self.game_repository.upload_game_file(file, game_id)

    async def delete_game(self, game_id: ObjectId) -> GameDto:
        """
        Función que realiza un borrado lógico del juego cuyo ID coincida con el pasado por parámetro.
        Si ya estaba deshabilitado, lo rehabilita en su lugar.
        :param game_id: ID del juego que queremos deshabilitar/habilitar.
        :return: DTO del juego una vez actualizado, 404 si no existe, o 503 si hubo un error al modificarlo.
        """
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
        """
        Función que devuelve el archivo del juego para su posterior descarga.
        :param game_id: ID del juego cuyo archivo queremos conseguir.
        :return: La ruta absoluta del archivo a descargar, 404 si el juego o el archivo no existen.
        """
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
        """
        Función que devuelve el path completo de la imágen principal del juego cuyo ID
        coincida con el pasado por parámetro, o el de una imágen por defecto si no existe.
        :param game_id: ID del juego cuya imágen principal queremos conseguir.
        :return: La ruta absoluta de la imágen, o 404 si el juego no existe.
        """
        game = await self.game_repository.get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Game with ID: {game_id} not found.")
        return get_image_by_name(game.main_image)
