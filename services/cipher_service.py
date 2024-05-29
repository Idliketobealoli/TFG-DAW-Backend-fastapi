import bcrypt


def encode(string: str) -> str:
    return bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')


def match(string: str, hashed_str: str) -> bool:
    return bcrypt.checkpw(string.encode('utf-8'), hashed_str.encode('utf-8'))
