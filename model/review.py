from pydantic import BaseModel
from bson import ObjectId
import datetime


class Review(BaseModel):
    id: ObjectId
    game_id: ObjectId
    user_id: ObjectId
    publish_date: datetime
    rating: float
    description: str

    #Posible necesario añadir el arbitrary types allowed