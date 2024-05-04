from pydantic import BaseModel, SkipValidation
from bson import ObjectId
import datetime


class Review(BaseModel):
    id: ObjectId
    game_id: ObjectId
    user_id: ObjectId
    publish_date: SkipValidation[datetime]
    rating: float
    description: str

    class Config:
        arbitrary_types_allowed = True
