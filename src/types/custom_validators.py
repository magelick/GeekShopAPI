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


def title_validator(value: str) -> str:
    """
    Валидатор названия
    :param value:
    :return:
    """
    # Если значение имеет или - или пробел или состоит из букв и цифр
    if value.replace("-", "").replace(" ", "").isalnum():
        # Возвращаем его
        return value
    # В противном случае выдаём ошибку о неправильно введенном значении
    raise ValueError("Строка содержит символы, отличающиеся от пробелов, тире, букв и цифр")


def age_validator(age: int) -> int:
    """
    Валидатор возраста
    :param age:
    :return:
    """
    # Возвраст указан верно
    if age + "+":
        # Возвращаем его
        return age
    # В противном случае выдаём оибку о том, что возраст введен неправильно
    raise ValueError("Укажите правильный возраст")
