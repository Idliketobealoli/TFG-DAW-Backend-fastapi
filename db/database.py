from motor.motor_asyncio import AsyncIOMotorClient


class Database:
    client: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://localhost:27017")
    database_name = "vgameshop_db"
    database = client.get_database(database_name)

    def get_database(self):
        return self.database

    async def init_database(self):
        await self.client.drop_database(self.database_name)
        self.database = self.client.get_database(self.database_name)


db = Database()
