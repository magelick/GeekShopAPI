from typing import Optional

from pydantic import Field, PositiveInt
from .base import DTO


class ComicsAuthorsBasic(DTO):
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


class ComicsAuthorsAddForm(ComicsAuthorsBasic):
    """
    Схема добавления нового экземпляра связанной модели Комикса и Автора
    """
    ...


class ComicsAuthorsUpdateForm(ComicsAuthorsBasic):
    """

    """
    ...


class ComicsAuthorsDetail(ComicsAuthorsBasic):
    """
    Схема представления экземпляра связанной модели Комикса и Автора
    """
    id: Optional[int] = Field(
        default=0,
        title="ID экземпляра",
        description="ID конкретного комикса"
    )
