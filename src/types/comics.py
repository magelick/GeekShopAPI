import datetime
from decimal import Decimal
from typing import Optional, Self, List

from sqlalchemy import select

from pydantic import Field, PositiveInt, model_validator, field_validator
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class ComicsBasic(DTO):
    """
    Базовая схема конкретного комикса
    """
    # Название комикса
    title: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Название комикса",
        description="Название конкретного комикса"
    )
    # Том комикса
    volume: PositiveInt = Field(
        default=...,
        title="Том комикса",
        description="Том конкретного комикса"
    )
    # Дата создания комикса
    date_created: datetime.date = Field(
        default=...,
        title="Дата создания комикса",
        description="Дата создания конкретного комикса",
    )
    # Цена комикса
    price: Decimal = Field(
        default=...,
        max_digits=4,
        decimal_places=2,
        title="Цена комикса",
        description="Цена конкретного комикса"
    )
    # Страна выпуска комикса
    country: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Страна выпуска комикса",
        description="Страна выпуска конкретного комикса",
        examples=["Америка", "Германия", "Норвегия"]
    )
    # # Персонажи комикса
    # characters: List[PositiveInt] = Field(
    #     default=...,
    #     title="Персонажи комикса",
    #     description="Персонажи конкретного комикса"
    # )
    # # Авторы комикса
    # authors: List[PositiveInt] = Field(
    #     default=...,
    #     title="Авторы комикса",
    #     description="Авторы конкретного комикса"
    # )


class ComicsAddForm(ComicsBasic):
    """
    Схема добавления конкретного комикса
    """
    ...

    @field_validator("title", mode="after")
    def title_validator(cls, title: str) -> str:
        """
        Валидатор названия комикса
        :param title:
        :return:
        """
        from src.database.models import Comics
        # Открываем сессию
        with Comics.session() as session:
            # Достаём комикс по названию
            comics = session.scalar(select(Comics).filter_by(title=title))
            # Если комикс найден
            if comics is not None:
                # Выдаём ошибку
                raise ValueError("Такой комикс уже существует")
            # В другом случае возвращаем валидные данные
            return title


class ComicsDetail(ComicsBasic):
    """
    Схема представления данных конкретного комикса
    """
    # ID комикса
    id: Optional[PositiveInt] = Field(
        default=None,
        title="ID комикса",
        description="ID конкретного комикса"
    )
    # Слаг комикса
    slug: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=128,
        title="Слаг комикса",
        description="Слаг конкретного комикса"
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        """
        Валидатор полей схемы
        :return:
        """
        # Если слаг не передан
        if self.slug is None:
            # Генерируем слаг на основании названия, тома и даты создания конкретного комикса
            self.slug = slugify(f"{self.title}-{self.volume}-{self.date_created}")

        # В другом случае возвращаем валидные данные
        return self
