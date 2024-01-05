from decimal import Decimal
from typing import Self, Optional

from pydantic import Field, model_validator, PositiveInt, field_validator
from slugify import slugify
from sqlalchemy import select

from .base import DTO
from .custom_types import AlphaStr, TitleStr


class SweetBasic(DTO):
    """
    Базовая схема представления кокнретной сладости
    """
    # Название сладости
    title: TitleStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Название сладости",
        description="Название конкретной сладости",
        examples=["Желатин Человека-Паука, Конфета Железного Человека, Напиток Джокера"]
    )
    # Цена сладости
    price: Decimal = Field(
        default=...,
        max_digits=4,
        decimal_places=2,
        title="Цена сладости",
        description="Цена конкретной сладости",
        examples=["20.99, 19,99, 99.99"]
    )
    # Вес сладости
    weight: PositiveInt = Field(
        default=...,
        title="Вес сладости",
        description="Вес конкретной сладости",
        examples=["1, 23, 456, 7890"]
    )
    # Персонаж сладости
    character_id: PositiveInt = Field(
        default=...,
        title="Персонаж сладости",
        description="Персонаж, к которому относиться конкретная сладость",
        examples=["1, 2, 3, 4"]
    )


class SweetAddForm(SweetBasic):
    """
    Схема добавления конкретной сладости
    """
    ...

    @field_validator("title", mode="after")
    def title_validator(cls, title: str) -> str:
        """
        Валидатор названия сладости
        :param title:
        :return:
        """
        from src.database.models import Sweet
        # Открываем сессию
        with Sweet.session() as session:
            # Достаём сладость по названию
            sweet = session.scalar(select(Sweet).filter_by(title=title))
            # Если сладость найдена
            if sweet is not None:
                # Выдаём ошибку
                raise ValueError("Такая сладость уже существует")
            # В другом случае возвращаем валидные данные
            return title


class SweetUpdateForm(SweetBasic):
    """
    Схема обновления конкретной сладости
    """
    ...


class SweetDetail(SweetBasic):
    """
    Схема представления данных о конкретной сладости
    """
    # ID сладости
    id: Optional[PositiveInt] = Field(
        default=None,
        title="ID девайса",
        description="ID конкретного девайса"
    )
    # Слаг сладости
    slug: Optional[str] = Field(
        default=None,
        min_length=4,
        max_length=128,
        title="Слаг девайса",
        description="Слаг конкретного девайса"
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        """
        Валидатор полей схемы
        :return:
        """
        # Если слаг не передан
        if self.slug is None:
            # Генерируем слаг на основании названия, веса и цены конкретной сладости
            self.slug = slugify(f"{self.title}-{self.weight}-{self.price}")

        # В другом случае возвращаем валидные данные
        return self
