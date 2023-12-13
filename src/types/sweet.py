import decimal
from typing import Self

from pydantic import Field, model_validator, PositiveInt
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class SweetBasic(DTO):
    """
    Базовая схема представления кокнретной сладости
    """
    # Название сладости
    title: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Название сладости",
        description="Название конкретной сладости"
    )
    # Цена сладости
    price: decimal = Field(
        default=...,
        # max_digits=4,
        # decimal_places=2,
        title="Цена сладости",
        description="Цена конкретной сладости"
    )
    # Вес сладости
    weight: PositiveInt = Field(
        default=...,
        title="Вес сладости",
        description="Вес конкретной сладости"
    )
    # Персонаж сладости
    character: PositiveInt = Field(
        default=...,
        title="Персонаж сладости",
        description="Персонаж, к которому относиться конкретная сладость"
    )


class SweetAddForm(SweetBasic):
    """
    Схема добавления конкретной сладости
    """
    ...


class SweetDetail(SweetBasic):
    """
    Схема представления данных о конкретной сладости
    """
    # ID сладости
    id: PositiveInt = Field(
        default=None,
        title="ID девайса",
        description="ID конкретного девайса"
    )
    # Слаг сладости
    slug: str = Field(
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
        return Self