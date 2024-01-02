from decimal import Decimal
from typing import Self, Optional

from sqlalchemy import select

from pydantic import Field, PositiveInt, model_validator, field_validator
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class DeviceBasic(DTO):
    """
    Базовая схема представления кокнретного девайса
    """
    # Название девайса
    title: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=128,
        title="Название девайса",
        description="Название конкретного девайса"
    )
    # Тип девайса
    type_of_device: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title="Тип девайса",
        description="Тип конкретного девайса"
    )
    # Цена девайса
    price: Decimal = Field(
        default=...,
        max_digits=5,
        decimal_places=2,
        title="Цена девайса",
        description="Цена конкретного девайса"
    )
    # Персонаж девайса
    character: PositiveInt = Field(
        default=...,
        title="Персонаж девайса",
        description="Персонаж, к которому относится данный девайс"
    )
    # Вселенная девайса
    universe: PositiveInt = Field(
        default=...,
        title="Вселенная девайса",
        description="Вселенная, к которой относиться данный девайс"
    )


class DeviceAddFrom(DeviceBasic):
    """
    Схема добавления конкретного девайса
    """
    ...

    @field_validator("title", mode="after")
    def title_validator(cls, title: str) -> str:
        """
        Валидатор названия девайса
        :param title:
        :return:
        """
        from src.database.models import Device
        # Открываем сессию
        with Device.session() as session:
            # Достаём девайс по названию
            device = session.scalar(select(Device).filter_by(title=title))
            # Если девайс найден
            if device is not None:
                # Выдаём ошибку
                raise ValueError("Такой девайс уже существует")
            # В другом случае возвращаем валидные значения
            return title


class DeviceUpdateForm(DeviceBasic):
    """
    Схема обновления конкретного девайса
    """
    ...


class DeviceDetail(DeviceBasic):
    """
    Схема представления данных о конкретном девайсе
    """
    # ID девайса
    id: Optional[PositiveInt] = Field(
        default=None,
        title="ID девайса",
        description="ID конкретного девайса"
    )
    # Слаг девайса
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
            # Генерируем слаг на основании названия, типа и цены конкретного девайса
            self.slug = slugify(f"{self.title}-{self.type_of_device}-{self.price}")

        # В другом случае возвращаем валидные данные
        return self
