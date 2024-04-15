import uvicorn
from bson import ObjectId
from fastapi import FastAPI
from controllers.user_controller import user_routes
from controllers.game_controller import game_routes
from db.database import db
from model.user import User, Role
from model.game import Game, Language, Genre
from repositories.user_repository import UserRepository
from repositories.game_repository import GameRepository
import datetime
import asyncio


app = FastAPI()

# Include CORS middleware to allow cross-origin requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # You can restrict this to specific origins if needed
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )
app.include_router(user_routes)
app.include_router(game_routes)


@app.on_event("startup")
async def load_initial_data():
    await db.init_database()
    await asyncio.gather(load_users(), load_games())
    # load_users()
    # load_games()

async def load_users():
    initial_users = [
        User(id=ObjectId(), name="Admin 1", email="admin1@gmail.com", password="admin1234", role=Role.ADMIN),
        User(id=ObjectId(), name="Admin 2", email="admin2@gmail.com", password="loli1707", role=Role.ADMIN),
        User(id=ObjectId(), name="User 1", email="user1@gmail.com", password="password1", role=Role.USER),
        User(id=ObjectId(), name="User 2", email="user2@gmail.com", password="password2", role=Role.USER),
        User(id=ObjectId(), name="User 3", email="user4@gmail.com", password="password4", role=Role.USER)
    ]

    user_repository = UserRepository()

    await asyncio.gather(*[user_repository.create_user(user) for user in initial_users])
    # for user in initial_users:
    #     await user_repository.create_user(user)


async def load_games():
    initial_games = [
        Game(id=ObjectId(), name="Dark Souls", developer="From Software", publisher="From Software", 
             genres={Genre.ARPG, Genre.SOULSLIKE, Genre.SINGLEPLAYER, Genre.MULTIPLAYER},
             languages={Language.EN, Language.ES, Language.JP, Language.GM}, rating=4.9,
             description="Es Dark Souls, ¿de verdad necesitas leer la descripción de este juego?", 
             release_date=datetime(year=2011, month=9, day=22), sell_number=35_000_000),

        Game(id=ObjectId(), name="Portal", developer="Valve", publisher="Valve", 
             genres={Genre.PUZZLE, Genre.PLATFORMER, Genre.SINGLEPLAYER, Genre.MULTIPLAYER},
             languages={Language.EN, Language.ES, Language.JP, Language.KR, Language.FR}, rating=4.1,
             description="Estás en un laboratorio siendo el sujeto de pruebas de una IA llamada GlaDOS, pero tienes una pistola de portales. Podrás escapar?", 
             release_date=datetime(year=2007, month=10, day=9), sell_number=4_000_000),

        Game(id=ObjectId(), name="Ratchet & Clank", developer="Insomniac Games", publisher="Sony", 
             genres={Genre.RPG, Genre.PUZZLE, Genre.PLATFORMER, Genre.CASUAL, Genre.TPS, Genre.SINGLEPLAYER},
             languages={Language.EN, Language.ES, Language.JP, Language.RU, Language.CN}, rating=4.5,
             description="Es literalmente el juego de mi infancia. Cómpralo.", 
             release_date=datetime(year=2002, month=11, day=8), sell_number=4_008_499)
    ]

    game_repository = GameRepository()

    await asyncio.gather(*[game_repository.create_game(game) for game in initial_games])
    # for game in initial_games:
    #     await game_repository.create_game(game)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=80)

