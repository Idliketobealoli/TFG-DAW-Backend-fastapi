from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List, Optional
from pydantic import EmailStr
from db.database import db
from model.user import User
from repositories import file_repository


def get_pfp_by_name(name: str) -> str:
    """
    Función para conseguir la ruta absoluta de la foto de perfil deseada.
    :param name: Nombre de la foto de perfil.
    :return: String con la ruta absoluta de la foto de perfil, o la ruta a una foto por defecto
    si no se hubiera encontrado.
    """
    return file_repository.get_file_full_path("user_pfp", name)


class UserRepository:
    collection: AsyncIOMotorCollection = db.client.vgameshop_db.user_routes

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[User]:
        """
        Función para obtener un usuario por su ID.
        :param user_id: ID del usuario a buscar.
        :return: Usuario encontrado, o None si no existe.
        """
        user = await self.collection.find_one({"id": user_id})
        if user:
            return User(**user)
        return None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Función para encontrar un usuario por su username.
        :param username: Username del usuario a buscar.
        :return: Usuario encontrado, o None si no existe.
        """
        user = await self.collection.find_one({"username": username})
        if user:
            return User(**user)
        return None

    async def user_exists_by_username_or_email(self, username: str, email: EmailStr) -> bool:
        """
        Función para determinar si existe un usuario en la base de datos con el mismo username o email.
        :param username: Username del usuario a buscar.
        :param email: Email del usuario a buscar.
        :return: True si existe un usuario con el mismo username o email; False en caso contrario.
        """
        user_by_username = await self.collection.find_one({"username": username})
        user_by_email = await self.collection.find_one({"email": email})
        if user_by_username or user_by_email:
            return True
        return False

    async def get_users(self) -> List[User]:
        """
        Función para obtener todos los usuarios de la base de datos.
        :return: Lista con todos los usuarios existentes.
        """
        users = await self.collection.find({}).to_list(length=None)
        return [User(**user) for user in users]

    async def get_users_active(self, active: bool) -> List[User]:
        """
        Función para obtener todos los usuarios de la base de datos
        cuya condición de actividad coincida con la pasada por parámetro.
        :param active: Si están habilitados o deshabilitados.
        :return: Lista con todos los usuarios existentes que cumplan el criterio especificado.
        """
        users = await self.collection.find({"active": active}).to_list(length=None)
        return [User(**user) for user in users]

    async def create_user(self, user: User) -> Optional[User]:
        """
        Función para insertar un nuevo usuario.
        :param user: Datos del usuario a crear.
        :return: El usuario creado, o None si no lo pudo crear.
        """
        await self.collection.insert_one(user.dict())
        return await self.get_user_by_id(user.id)

    async def update_user(self, user_id: ObjectId, user_data: dict) -> Optional[User]:
        """
        Función para actualizar los datos de un usuario existente.
        :param user_id: ID del usuario a modificar.
        :param user_data: Datos a actualizar.
        :return: El usuario actualizado, o None si no existía.
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        await self.collection.update_one({"id": user.dict().pop('id', None)},
                                         {"$set": user_data})
        return await self.get_user_by_id(user_id)

    async def upload_image_for_user(self, file: UploadFile, user_id: ObjectId) -> bool:
        """
        Función para subir una foto de perfil y enlazarla a un usuario.
        :param file: Foto de perfil.
        :param user_id: ID del usuario a quien corresponderá la foto de perfil.
        :return: True si se pudo actualizar el usuario y la foto se subió correctamente;
        False en caso de que el usuario no existiera.
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        pfp = await file_repository.upload_file(file, "user_pfp", str(user_id))
        user.profile_picture = pfp
        await self.collection.update_one({"id": user.dict().pop('id', None)},
                                         {"$set": user.dict()})
        return True

    async def delete_user(self, user_id: ObjectId) -> Optional[User]:
        """
        Función para el borrado lógico del usuario. No lo borra, sino que cambia su estado de actividad.
        :param user_id: ID del usuario.
        :return: El usuario modificado, o None si no existía.
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        user.active = not user.active
        await self.collection.update_one({"id": user.dict().pop('id', None)}, {"$set": user.dict()})
        return await self.get_user_by_id(user_id)
