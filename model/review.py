from pydantic import BaseModel, SkipValidation, Field
from bson import ObjectId
import datetime


class Review(BaseModel):
    id: ObjectId = Field(default=ObjectId())
    game_id: ObjectId
    user_id: ObjectId
    publish_date: SkipValidation[datetime] = Field(default=datetime.datetime.now())
    rating: float
    description: str

    class Config:
        arbitrary_types_allowed = True
