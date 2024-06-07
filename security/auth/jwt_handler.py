from datetime import datetime, timedelta, timezone
from typing import Union
from jose import JWTError, jwt

SECRET_KEY = "LaClaveSecretadelaAPIDe_LaAplicac10ndel7f6DeD4W_EnEl135Lagun4deJ0a7z3l"  # Use a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 2


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception
