from datetime import datetime
from typing import Self

from pydantic import Field, PositiveInt, model_validator
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class UniverseBasic(DTO):
    """
    Базовая схема конкретной вселенной персонажей
    """
    # Название вселенной
    title: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Название вселенной",
        description="Название вселенной персонажей"
    )
    # Дата создания
    date_created: datetime.year = Field(
        default=...,
        title="Дата создания",
        description="Дата создания конкретной вселенной"
    )


class UniverseAddForm(UniverseBasic):
    """
    Схема добавления конкретной вселенной персонажей
    """
    ...


class UniverseDetail(UniverseBasic):
    """
    Схема представления конкретной вселенной персонажей
    """
    # ID вселенной
    id: PositiveInt = Field(
        default=None,
        title="ID вселенной",
        description="ID конкретной вселенной"
    )
    # Слаг вселенной
    slug: str = Field(
        default=None,
        min_length=4,
        max_length=128,
        title="Слаг персонажа",
        description="Слаг конкретного персонажа"
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        """
        Валидатор полей схемы
        :return:
        """
        # Если слаг не передан
        if self.slug is None:
            # Генерируем слаг на основании названия и даты создания конкретной вселенной
            self.slug = slugify(f"{self.title}-{self.date_created.timestamp()}")

        # В другом случае возвращаем валидные данные
        return Self