import uvicorn
from bson import ObjectId
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import user_routes
from controllers.game_controller import game_routes
from controllers.review_controller import review_routes
from controllers.wishlist_controller import wishlist_routes
from controllers.library_controller import library_routes
from db.database import db
from model.user import User, Role
from model.game import Game, Language, Genre
from repositories.library_repository import LibraryRepository
from repositories.user_repository import UserRepository
from repositories.game_repository import GameRepository
import datetime
import asyncio

from repositories.wishlist_repository import WishlistRepository

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(game_routes)
app.include_router(review_routes)
app.include_router(wishlist_routes)
app.include_router(library_routes)

user_repository = UserRepository()
library_repository = LibraryRepository()
wishlist_repository = WishlistRepository()


@app.on_event("startup")
async def load_initial_data():
    await db.init_database()
    await asyncio.gather(load_users(), load_games())


async def load_users():
    initial_users = [
        User(id=ObjectId(), name="Marina Guanghua", surname="Pintado", username="darkhuo10", email="admin1@gmail.com",
             password="admin1234", birthdate=datetime.datetime(2003, 12, 10), role=Role.ADMIN,
             profile_picture="darkhuo10.png"),

        User(id=ObjectId(), name="Daniel", surname="Rodríguez", username="Idliketobealoli", email="admin2@gmail.com",
             password="loli1707", birthdate=datetime.datetime(2002, 5, 26), role=Role.ADMIN,
             profile_picture="Idliketobealoli.png"),

        User(id=ObjectId(), name="User 1", surname="Apellido", username="usuario1", email="user1@gmail.com",
             password="password1", birthdate=datetime.datetime(2002, 5, 26),
             profile_picture="asdf.png"),

        User(id=ObjectId(), name="User 2", surname="Apellido 2", username="usuario2", email="user2@gmail.com",
             password="password2", birthdate=datetime.datetime(2002, 5, 26)),

        User(id=ObjectId(), name="User 3", surname="Apellido 3", username="usuario3", email="user4@gmail.com",
             password="password4", birthdate=datetime.datetime(2002, 5, 26))
    ]

    # Los usuarios con sus libraries y wishlists se crean a la vez (en hilos distintos), pero dentro de la creación
    # de cada usuario, primero se crea el usuario, luego la wishlist y luego la library, para evitar problemas.
    await asyncio.gather(*[create_user_with_library_and_wishlist(user) for user in initial_users])


async def create_user_with_library_and_wishlist(user):
    await user_repository.create_user(user)
    await wishlist_repository.create_wishlist(user.id)
    await library_repository.create_library(user.id)


async def load_games():
    initial_games = [
        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b1"), name="Dark Souls", developer="From Software",
             publisher="From Software",
             genres=[genre for genre in {Genre.ARPG, Genre.SOULSLIKE, Genre.SINGLEPLAYER, Genre.MULTIPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.GM}],
             description="Es Dark Souls, ¿de verdad necesitas leer la descripción de este juego?",
             release_date=datetime.datetime(2011, 9, 22), sell_number=35_000_000, price=70,
             main_image="60a7b2f7c0f2b441d4f6e9b1.png"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b2"), name="Portal", developer="Valve", publisher="Valve",
             genres=[genre for genre in {Genre.PUZZLE, Genre.PLATFORMER, Genre.SINGLEPLAYER, Genre.MULTIPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.KR, Language.FR}],
             description="Estás en un laboratorio siendo el sujeto de pruebas de una IA llamada GlaDOS, " +
                         "pero tienes una pistola de portales. Podrás escapar?",
             release_date=datetime.datetime(2007, 10, 9), sell_number=4_000_000, price=20,
             main_image="60a7b2f7c0f2b441d4f6e9b2.png"),

        Game(id=ObjectId("60a7b2f7c0f2b441d4f6e9b3"), name="Ratchet & Clank", developer="Insomniac Games",
             publisher="Sony", genres=[genre for genre in {Genre.RPG, Genre.PUZZLE, Genre.PLATFORMER, Genre.CASUAL,
                                                           Genre.TPS, Genre.SINGLEPLAYER}],
             languages=[language for language in {Language.EN, Language.ES, Language.JP, Language.RU, Language.CN}],
             description="Es literalmente el juego de mi infancia. Cómpralo.",
             release_date=datetime.datetime(2002, 11, 8), sell_number=4_008_499, price=40,
             main_image="60a7b2f7c0f2b441d4f6e9b3.png")
    ]

    game_repository = GameRepository()
    await asyncio.gather(*[game_repository.create_game(game) for game in initial_games])


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=80)
