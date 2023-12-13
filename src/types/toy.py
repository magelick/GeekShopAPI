import decimal
from typing import Self

from pydantic import Field, model_validator, PositiveInt
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class ToyBasic(DTO):
    """
    Базовая схема предсатвления конкретной игрушки
    """
    # Название игрушки
    title: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Название игрушки",
        description="Название конкретной игрушки"
    )
    # Возраст для игрушки
    age: PositiveInt = Field(
        default=...,
        title="Возраст для игрушки",
        description="Возраст для конкретной игрушки"
    )
    # Тип игрушки
    type_of_toy: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Тип игрушки",
        description="Тип кокнретной игрушки"
    )
    # Цена игрушки
    price: decimal = Field(
        default=...,
        # max_digits=4,
        # decimal_places=2,
        title="Цена игрушки",
        description="Цена конкретной игрушки"
    )
    # Персонаж игрушки
    character: PositiveInt = Field(
        default=...,
        title="Персонаж игрушки",
        description="Персонаж, к которому относится конкретная игрушка"
    )
    # Вселенная игрушки
    universe: PositiveInt = Field(
        default=...,
        title="Вселенная игрушки",
        description="ВСеленная, к которой относится конкретная игрушка"
    )


class ToyAddForm(ToyBasic):
    """
    Схема добавления конкретной игрушки
    """
    ...


class ToyDetail(ToyBasic):
    """
    Схема представления данных о конкретной игрушке
    """
    # ID игрушки
    id: PositiveInt = Field(
        default=None,
        title="ID игрушки",
        description="ID конкретной игрушки"
    )
    # Слаг игрушки
    slug: str = Field(
        default=None,
        min_length=4,
        max_length=128,
        title="Слаг игрушки",
        description="Слаг конкретной игрушки"
    )

    @model_validator(mode="after")
    def validator(self) -> Self:
        """
        Валидатор полей схемы
        :return:
        """
        # Если слаг не передан
        if self.slug is None:
            # Генерируем слаг на основании имени, весе и цене конкретной игрушки
            self.slug = slugify(f"{self.title}-{self.weight}-{self.price}")

        # В другом случае возвращаем валидные данные
        return Self