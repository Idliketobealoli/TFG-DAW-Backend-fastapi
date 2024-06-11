import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import user_routes
from controllers.game_controller import game_routes
from controllers.review_controller import review_routes
from controllers.wishlist_controller import wishlist_routes
from controllers.library_controller import library_routes
from db.database import db
import asyncio
from services.init_service import load_users, load_games, load_reviews, load_wishlists

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


@app.on_event("startup")
async def load_initial_data():
    await db.init_database()
    await asyncio.gather(load_users(), load_games(), load_reviews())

    # Esta última después de que se creen las demás porque requiere tanto de juegos como de users.
    await load_wishlists()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=80)
