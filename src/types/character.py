from datetime import datetime
from typing import Self

from slugify import slugify
from ulid import new
from pydantic import Field, model_validator, PositiveInt
from .base import DTO
from .custom_types import AlphaStr


class CharacterBasic(DTO):
    """
    Базавая схема представления данных конкретного персонажа
    """
    # Имя персонада
    name: AlphaStr = Field(
        default=...,
        min_length=2,
        max_length=64,
        title="Имя персонажа",
        description="Имя конкретного персонажа",
        examples=["Железный человек", "Человек Паук", "Бэтмен"]
    )
    # Дата создания
    date_created: datetime.year = Field(
        default=...,
        title="Дата создания",
        description="Дата создания конкретного персонажа",
    )
    # Роль персонажа
    role: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Роль",
        description="Роль конкретного персонажа",
        examples=["Герой", "Злодей", "Антигерой"]
    )
    # Способность персонажа
    power: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Способность персонажа",
        description="Способность конкретного персонажа"
    )
    # Автор персонажа
    author_id: PositiveInt = Field(
        default=None,
        title="ID автора",
        description="ID конкретного автора конкретного комикса"
    )
    # Вселенная персонажа
    universe_id: PositiveInt = Field(
        default=None,
        title="ID вселенной",
        description="ID конкретной вселенной конкретного персонажа"
    )


class CharacterAddForm(CharacterBasic):
    """
    Схема добавления конкретного персонажа
    """
    ...


class CharacterDetail(CharacterBasic):
    """
    Схема представления данных о конкретном персонаже
    """
    # ID персонажа
    id: PositiveInt = Field(
        default=None,
        title="ID персонажа",
        description="ID конкретного персонажа"
    )
    # Слаг персонажа
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
            # Генерируем слаг на основании имени конкретного персонажа
            self.slug = slugify(f"{self.name}-{self.date_created.timestamp()}")

        # В другом случае возвращаем валидные данные
        return Self
