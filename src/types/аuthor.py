from datetime import datetime
from typing import List, Self

from pydantic import Field, PositiveInt, model_validator, field_validator
from slugify import slugify
from sqlalchemy import select

from .base import DTO
from .custom_types import AlphaStr
from src.database.models import Author


class AuthorBasic(DTO):
    """
    Базовая схема представления конкретного автора
    """
    # Имя автора
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Имя автора",
        description="Имя конкретного автора"
    )
    # Фамилия автора
    surname: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Фамилия автора",
        description="Фамилия конкретного автора"
    )
    # Дата рождения автора
    birthday: datetime = Field(
        default=...,
        title="Дата рождения автора",
        description="Дата рождения конкретного автора"
    )
    # Комиксы автора
    comics: List[PositiveInt] = Field(
        default=...,
        title="Комиксы автора",
        description="Комиксы конкретного автора"
    )


class AuthorAddForm(AuthorBasic):
    """
    Схема добоваления конкретного автора
    """
    ...

    @field_validator("", mode="after")
    def name_validator(cls, name: str) -> str:
        """
        Валидатор имени автора
        :param name:
        :return:
        """
        # Открываем сессию
        with Author.session() as session:
            # Достаём автора по имени
            author = session.scalar(select(Author).filter_by(name=name))
            # Если автор найден
            if author is not None:
                # Выдаём ошибку
                raise ValueError("Такой автор уже существует")
            # В другом случае возвращаем валлидные данные
            return name


class AuthorDetail(AuthorBasic):
    """
    Схема представления данных конкретного автора
    """
    # ID автора
    id: PositiveInt = Field(
        default=None,
        title="ID автора",
        description="ID конкретного автора"
    )
    # Слаг автора
    slug: str = Field(
        default=None,
        min_length=4,
        max_length=128,
        title="Слаг автора",
        description="Слаг конкретного автора"
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        """
        Валидатор полей схемы
        :return:
        """
        # Если слаг не передан
        if self.slug is None:
            # Генерируем слаг на основании имени, фамилии и даты рождения конкретного автора
            self.slug = slugify(f"{self.name}-{self.surname}-{self.birthday.timestamp()}")

        # В другом случае возвращаем валидные данные
        return Self