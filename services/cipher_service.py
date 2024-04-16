import bcrypt


def encode(str: str) -> str:
    return bcrypt.hashpw(str, bcrypt.gensalt(12))


def match(str: str, hashed_str: str) -> bool:
    return bcrypt.checkpw(str, hashed_str)