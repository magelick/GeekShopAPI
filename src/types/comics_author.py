from typing import List, Optional

from pydantic import Field, PositiveInt
from .base import DTO


class ComicsAuthorBasic(DTO):
    """
    Базовая схема представления связанной модели Комиска и Автора
    """
    comics_id: PositiveInt = Field(
        default=...,
        title="ID комиксов",
        examples=[1]
    )
    author_id: PositiveInt = Field(
        default=...,
        title="ID авторов",
        examples=[1]
    )


class ComicsAuthorAddForm(ComicsAuthorBasic):
    """
    Схема добавления нового экземпляра связанной модели Комикса и Автора
    """
    ...


class ComicsAuthorDetail(ComicsAuthorBasic):
    """
    Схема представления экземпляра связанной модели Комикса и Автора
    """
    id: PositiveInt = Field(
        default=None,
        title="ID экземпляра",
        description="ID конкретного комикса"
    )
