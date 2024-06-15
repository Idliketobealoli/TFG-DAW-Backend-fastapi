from typing import List
import jwt
from datetime import datetime, timedelta
from decouple import config
from starlette import status
from starlette.exceptions import HTTPException
from model.user import User

SECRET_KEY = config("SECRET_KEY", default="El_br4inr0t_de_Jujutsu_Ka1sen_me_ha_c0nsum1do_la_v1d4")


def create_access_token(user: User):
    expiration = datetime.utcnow() + timedelta(days=1)
    payload = {
        "id": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_role(desired_roles: List[str], token: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
    if payload["role"] not in desired_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")


def check_role_and_myself(desired_roles: List[str], token: str, id_str: str):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

    if (payload["role"] not in desired_roles) or (payload["id"] != id_str and payload["role"] != "ADMIN"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
