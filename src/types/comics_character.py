from typing import List, Optional, Self

from pydantic import Field, PositiveInt, model_validator
from .base import DTO


class ComicsCharacterBasic(DTO):
    """
    Базовая схема представления связанной модели Комиска и Автора
    """
    comics_id: PositiveInt = Field(
        default=...,
        title="ID комиксов",
        examples=[1]
    )
    character_id: PositiveInt = Field(
        default=...,
        title="ID персонажей",
        examples=[1]
    )


class ComicsCharacterAddForm(ComicsCharacterBasic):
    """
    Схема добавления нового экземпляра связанной модели Комикса и Автора
    """
    ...


class ComicsCharacterUpdateForm(ComicsCharacterBasic):
    """

    """
    ...


class ComicsCharacterDetail(ComicsCharacterBasic):
    """
    Схема представления экземпляра связанной модели Комикса и Автора
    """
    id: Optional[int] = Field(
        default=0,
        title="ID экземпляра",
        description="ID конкретного комикса"
    )