import bcrypt


def encode(string: str) -> str:
    """
    Función que encripta el string pasado por parámetro usando BCrypt con un salteado de 12 rondas.
    :param string: el string a codificar.
    :return: el string codificado pasado a un string en utf-8
    """
    return bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')


def match(string: str, hashed_str: str) -> bool:
    """
    Función que comprueba si el string pasado por el primer parámetro coincide con
    el string codificado pasado en el segundo parámetro.
    :param string: string sin codificar.
    :param hashed_str: string codificado.
    :return: True si coinciden, False si no coinciden.
    """
    return bcrypt.checkpw(string.encode('utf-8'), hashed_str.encode('utf-8'))