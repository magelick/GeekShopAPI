from decimal import Decimal
from typing import Self

from pydantic import Field, model_validator, PositiveInt, field_validator
from slugify import slugify
from sqlalchemy import select

from .base import DTO
from .custom_types import AlphaStr, TitleStr, AgeInt


class ToyBasic(DTO):
    """
    Базовая схема предсатвления конкретной игрушки
    """
    # Название игрушки
    title: TitleStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Название игрушки",
        description="Название конкретной игрушки",
        examples=["Робот Человека-Паука, Кунай Наруто, Меч Блэйда"]
    )
    # Возраст для игрушки
    age: AgeInt = Field(
        default=...,
        title="Возраст для игрушки",
        description="Возраст для конкретной игрушки",
        examples=["6+, 12+, 18+, 21+"]
    )
    # Тип игрушки
    type_of_toy: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Тип игрушки",
        description="Тип кокнретной игрушки",
        examples=["Машинка, Конструктор, Пазл"]
    )
    # Цена игрушки
    price: Decimal = Field(
        default=...,
        max_digits=4,
        decimal_places=2,
        title="Цена игрушки",
        description="Цена конкретной игрушки",
        examples=["20.99, 19,99, 99.99"]
    )
    # Персонаж игрушки
    character_id: PositiveInt = Field(
        default=...,
        title="Персонаж игрушки",
        description="Персонаж, к которому относится конкретная игрушка",
        examples=["1, 2, 3, 4"]
    )


class ToyAddForm(ToyBasic):
    """
    Схема добавления конкретной игрушки
    """
    ...

    @field_validator("title", mode="after")
    def title_validator(cls, title: str) -> str:
        """
        Валидатор названия игрушки
        :param title:
        :return:
        """
        from src.database.models import Toy
        # Открываем сессию
        with Toy.session() as session:
            # Достаём игрушку по названию
            toy = session.scalar(select(Toy).filter_by(title=title))
            # Если игрушка найдена
            if toy is not None:
                # Выдаём ошибку
                raise ValueError("Такая игрушка уже существует")
            # В другом случае возвращаем валидные данные
            return title


class ToyUpdateForm(ToyBasic):
    """
    Схема обновления конкретной игрушки
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
            self.slug = slugify(f"{self.title}-{self.type_of_toy}-{self.price}")

        # В другом случае возвращаем валидные данные
        return Self
