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


# Example usage:
# To upload an image associated with a user:
# image_data = open("image.jpg", "rb").read()
# image_id = await db.upload_image(image_data)
# user.image_id = image_id
# await user.save()

# To retrieve the image associated with a user:
# image_data = await db.get_image(user.image_id)
# # You can then do whatever you want with the image data, e.g., display it, save it to a file, etc.

db = Database()
