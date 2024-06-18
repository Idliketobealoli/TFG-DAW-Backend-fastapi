from typing import List
import jwt
from datetime import datetime, timedelta
from decouple import config
from starlette import status
from starlette.exceptions import HTTPException
from model.user import User

SECRET_KEY = config("SECRET_KEY", default="El_br4inr0t_de_Jujutsu_Ka1sen_me_ha_c0nsum1do_la_v1d4")


def create_access_token(user: User):
    """
    Función que crea y devuelve el token.
    :param user: Usuario para el cual se va a generar el token.
    :return: El token (un string).
    """
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
    """
    Función que decodifica el token si es válido.
    :param token: Token que queremos descifrar y comprobar su validez.
    :return: El token decodificado o None si no es válido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_role(desired_roles: List[str], token: str):
    """
    Función que valida si el token contiene uno de los roles deseados.
    :param desired_roles: Lista de strings con los roles permitidos.
    :param token: Token del usuario cuyos roles queremos chequear.
    :return: None si el usuario tiene uno de los roles permitidos, 401 si el token es inválido o
    403 si no tiene uno de los roles permitidos.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
    if payload["role"] not in desired_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")


def check_role_and_myself(desired_roles: List[str], token: str, id_str: str):
    """
    Función que valida si el token contiene uno de los roles deseados o
    el usuario cuyo ID ha sido pasado por parámetro es el mismo que el del token.
    :param desired_roles: Lista de strings con los roles permitidos.
    :param token: token del usuario cuyos roles queremos chequear.
    :param id_str: ID del usuario que queremos comprobar.
    :return: None si el usuario tiene uno de los roles permitidos o es el mismo que el del ID pasado por parámetro,
    401 si el token es inválido o 403 si no tiene uno de los roles permitidos.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

    if (payload["role"] not in desired_roles) or (payload["id"] != id_str and payload["role"] != "ADMIN"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
