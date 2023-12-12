
from re import compile

# Регулярка на проверку пароля
PASSWORD_REGEX = compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,64}$")


def password_validator(password: str) -> str:
    """
    Валидатор для проверки пароля на соответствие регулярке
    :param password:
    :return:
    """
    # Если пароль не соответсвует регулярке
    if PASSWORD_REGEX.fullmatch(password) is None:
        # Выдаём ошибку
        raise ValueError('Невалидный пароль')
    # В другом случаи возвращаем валидный пароль
    return password


def is_alpha_validator(value: str) -> str:
    """
    Валидатор, проверяющий строку на буквы
    :param value:
    :return:
    """
    # Если строка содержит мисволы, отличающиеся от букв
    if not value.isalpha():
        # Выдаём ошибку
        raise ValueError('Невалидное значение')
    # В другом случае возращаем валидную строку
    return value

