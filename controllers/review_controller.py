from fastapi import APIRouter, Query, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from services.authentication_service import check_role, decode_access_token, check_role_and_myself
from services.library_service import LibraryService
from services.review_service import ReviewService
from dto.review_dto import ReviewDtoCreate, ReviewDtoUpdate
from bson import ObjectId
from typing import Optional
import datetime

review_routes = APIRouter()
review_service = ReviewService()
library_service = LibraryService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@review_routes.get("/reviews")
async def get_all_reviews(
        user_id: Optional[str] = Query(None),
        game_id: Optional[str] = Query(None),
        rating: Optional[float] = Query(None),
        publish_date: Optional[datetime.datetime] = Query(None),
        token: str = Depends(oauth2_scheme)
):
    check_role(["ADMIN", "USER"], token)
    payload = decode_access_token(token)
    # De esta forma, la review del usuario que está solicitando este endpoint siempre será la primera
    # en mostrarse (si existe), y después estarán el resto de reviews ordenadas por fecha de publicación.
    reviews = sorted(await review_service.get_all_reviews(), key=lambda r: r.user.id == payload["id"])

    if user_id:  # and ObjectId(user_id):
        # poniendo esta linea comentada arriba se asegura que solo entre si es un guid valido,
        # pero podria llevar a casos inesperados como que si solo esta el param user_id y es invalido,
        # devuelva todas las reviews existentes.
        reviews = [review for review in reviews if user_id == review.user.id]

    if game_id:
        reviews = [review for review in reviews if game_id == review.game.id]

    if rating is not None:
        reviews = [review for review in reviews if review.rating >= rating]

    if publish_date:
        reviews = [review for review in reviews if review.publish_date >= publish_date]

    return reviews


@review_routes.get("/reviews/{review_id_str}")
async def get_review_by_id(review_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role(["ADMIN", "USER"], token)
    return await review_service.get_review_by_id(ObjectId(review_id_str))


@review_routes.get("/reviews/user/{user_id_str}")
async def get_reviews_from_user(user_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role(["ADMIN", "USER"], token)
    return await review_service.get_all_reviews_from_user(ObjectId(user_id_str))


@review_routes.get("/reviews/game/{game_id_str}")
async def get_reviews_from_game(game_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role(["ADMIN", "USER"], token)
    return await review_service.get_all_reviews_from_game(ObjectId(game_id_str))


@review_routes.post("/reviews/")
async def post_review(review: ReviewDtoCreate, token: str = Depends(oauth2_scheme)):
    review.validate_fields()
    check_role_and_myself(["ADMIN", "USER"], token, review.user_id)
    g_id = ObjectId(review.game_id)
    u_id = ObjectId(review.user_id)
    if await library_service.is_in_library(u_id, g_id):
        found_review = await review_service.get_review_from_user_and_game(u_id, g_id)
        if found_review is None:
            return await review_service.create_review(review)
        else:
            return await review_service.update_review(ObjectId(found_review.id), review.to_dto_update())
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You cannot create a review for a game you have not downloaded.")


@review_routes.delete("/reviews/{review_id_str}")
async def delete_review_by_id(review_id_str: str, token: str = Depends(oauth2_scheme)):
    check_role_and_myself(["ADMIN", "USER"], token, review_id_str)
    return await review_service.delete_review(ObjectId(review_id_str))