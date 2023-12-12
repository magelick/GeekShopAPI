from typing import Self

from pydantic import Field, EmailStr, model_validator
from ulid import new

from .base import DTO
from .custom_types import PasswordStr, AlphaStr


class UserBasic(DTO):
    """
    Базовая схема представления данных конкретного пользователя
    """
    # Адрес электронной почты
    email: EmailStr = Field(
        default=...,
        title="Адрес электронной почты",
        description="Адрес электронной почты конкретного пользователя",
        examples=["vasay277@gmail.com", "fcdm2004@gmail.com"]
    )
    # Пароль конкретного пользователя
    password: PasswordStr = Field(
        default=...,
        title="Пароль",
        description="Пароль конкретного пользователя"
    )


class UserLoginForm(UserBasic):
    """
    Схема авторизации конкретного пользователя
    """
    ...


class UserRegisterForm(UserBasic):
    """
    Схема решгистарции конкретного пользователя
    """
    # Имя конкретного пользователя
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Имя пользователя",
        description="Имя конкретного пользователя"
    )
    # Потверждение пароля
    confirm_password: PasswordStr = Field(
        default=...,
        title="Потверждение пароля",
        description="Потверждение пароля кокнретного пользователя"
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        """
        Валидатор полей схемы
        :return:
        """
        # Если пароль не содержится в потверждение пароля
        if self.password != self.confirm_password:
            # Выдаём ошибку
            raise ValueError("Пароль не совпадает")

        # Если адрес электронной почты находится в пароле
        if self.email.lower().split("@")[0] in self.password.lower():
            # Выдаём ошибку
            raise ValueError("Почта не может содержаться в пароле")

        # Если имя пользователя содержиться в пароле
        if self.name.lower() in self.password.lower():
            # Выдаём ошибку
            raise ValueError("Имя не олжно осдержаться в пароле")

        return self


class UserDetail(UserBasic):
    """
    Схема представления всех данных пользователя
    """
    # ID пользователя
    id: str = Field(
        default_factory=lambda: new().str,
        min_length=26,
        max_length=26,
        title="ID пользователя",
        description="ID конкретного пользователя"
    )
    # Имя конкретного пользователя
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Имя пользователя",
        description="Имя конкретного пользователя"
    )
