from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFS
from bson import ObjectId
from PIL import Image
import io


class Database:
    client: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://localhost:27017")
    database_name = "vgameshop_db"
    database = client.get_database(database_name)
    fs = GridFS(database) # GridFS instance for storing images

    def get_database(self):
        return self.database

    async def init_database(self):
        await self.client.drop_database(self.database_name)
        self.database = self.client.get_database(self.database_name)
    
    async def upload_image(self, image_data: bytes) -> ObjectId:
        # Upload image to GridFS and return the generated ObjectId
        with io.BytesIO(image_data) as image_stream:
            image_id = self.fs.put(image_stream)
        return image_id

    async def get_image(self, image_id: ObjectId) -> bytes:
        # Retrieve image data from GridFS using the provided ObjectId
        image_data = self.fs.get(image_id).read()
        return image_data

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
