import uvicorn
from bson import ObjectId
from fastapi import FastAPI
from controllers.user_controller import user_routes
from db.database import db
from model.user import User, Role
from repositories.user_repository import UserRepository


app = FastAPI()
app.include_router(user_routes)


@app.on_event("startup")
async def load_initial_data():
    await db.init_database()
    initial_users = [
        User(id=ObjectId(), name="Admin 1", email="admin1@gmail.com", password="admin1234", role=Role.ADMIN),
        User(id=ObjectId(), name="Admin 2", email="admin2@gmail.com", password="loli1707", role=Role.ADMIN),
        User(id=ObjectId(), name="User 1", email="user1@gmail.com", password="password1", role=Role.USER),
        User(id=ObjectId(), name="User 2", email="user2@gmail.com", password="password2", role=Role.USER),
        User(id=ObjectId(), name="User 3", email="user4@gmail.com", password="password4", role=Role.USER)
    ]
    user_repository = UserRepository()

    for user in initial_users:
        await user_repository.create_user(user)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=80)

