from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db_session
from src.types.аuthor import AuthorDetail, AuthorAddForm, AuthorUpdateForm
from src.types.character import CharacterDetail
from src.types.comics import ComicsDetail
from src.database.models import Author, Comics

# Роутер персонажей
router = APIRouter(
    prefix="/authors",
    tags=["Авторы комиксов и персонажей"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[AuthorDetail],
    name="Получение списка всех авторов"
)
async def get_list_authors(session: Session = get_db_session):
    """
    Получение списка всех авторов
    :param session:
    :return:
    """
    # Достаём все вселенные
    authors = session.scalars(select(Author).order_by(Author.id))
    # Возвращаем их, провалидировав через схему
    return [AuthorDetail.model_validate(obj=author, from_attributes=True) for author in authors]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthorDetail,
    name="Добавление нового автора"
)
async def add_new_author(form: AuthorAddForm, session: Session = get_db_session):
    """
    Добавление нового автора
    :param form:
    :param session:
    :return:
    """
    # Создаём нового автора, валидировав через основную схему представления автора
    form_author = AuthorDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    author = Author(**form_author.model_dump())
    # Добавляем нового автора в БД
    session.add(author)
    # Сохраняем изменения
    session.commit()
    # Дописываем id, если это не обходимо
    session.refresh(author)
    # Возвращаем нового автора в виде основной схемы представления автора
    return AuthorDetail.model_validate(obj=author, from_attributes=True)


@router.get(
    path="/{author_id}/",
    status_code=status.HTTP_200_OK,
    response_model=AuthorDetail,
    name="Получение конкретного автора"
)
async def get_author(author_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение конкретного автора
    :param author_id:
    :param session:
    :return:
    """
    # Получение конкретного автора по его ID
    author = session.scalar(select(Author).filter_by(id=author_id))
    # Если автор не найден
    if author is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого автора не существует")
    # В другом случае возвращаем валидированные данные
    return AuthorDetail.model_validate(obj=author, from_attributes=True)


@router.put(
    path="/{author_id}/",
    status_code=status.HTTP_200_OK,
    response_model=AuthorDetail,
    name="Обновление конкретного автора"
)
async def update_author(form: AuthorUpdateForm, author_id: PositiveInt = Path(default=..., ge=1),
                        session: Session = get_db_session):
    """
    Обновление конкретного автора
    :param form:
    :param author_id:
    :param session:
    :return:
    """
    # Достаём автора по его ID
    author = session.scalar(select(Author).filter_by(id=author_id))
    # Если автор не найден
    if author is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого автора не существует")
    # Валидируем полученные данные
    form_author = AuthorDetail(id=author_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_author:
        # Изменяем полученого по ID автора
        setattr(author, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем изменённого автора в виде основной схемы представления автора
    return AuthorDetail.model_validate(obj=author, from_attributes=True)


@router.delete(
    path="/{author_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретного автора"
)
async def delete_author(author_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретного автора
    :param author_id:
    :param session:
    :return:
    """
    # Достаём автора по его ID
    author = session.scalar(select(Author).filter_by(id=author_id))
    # Удаляем выбранного автора
    session.delete(author)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретного автора
    return {"msg": "Done"}


@router.get(
    path="/{author_id}/characters/",
    status_code=status.HTTP_200_OK,
    response_model=List[CharacterDetail],
    name="Получение списка всех персонажей конкретного автора"
)
async def get_list_characters_of_author(author_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение списка персонажей конкретного автора
    :param author_id:
    :param session:
    :return:
    """
    # Достаём автора по его ID
    author = session.scalar(select(Author).filter_by(id=author_id))
    # Если автор не найден
    if author is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого автора не существует")
    # Возвращаем список персонажей конкретного автора
    return [CharacterDetail.model_validate(obj=character, from_attributes=True) for character in author.characters]


@router.get(
    path="/{author_id}/comics/",
    status_code=status.HTTP_200_OK,
    response_model=List[ComicsDetail],
    name="Получение всех комиксов конкретного автора"
)
async def get_list_comics_of_author(author_id: PositiveInt = Path(default=...,ge=1), session: Session = get_db_session):
    """
    Получение списка комиксов конкретного автора
    :param author_id:
    :param session:
    :return:
    """
    # Достаём автора по его ID
    author = session.scalar(select(Author).filter_by(id=author_id))
    # Если автор не найден
    if author is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого автора не существует")
    # Возвращаем список комиксов кокнретного автора
    return [ComicsDetail.model_validate(obj=comics, from_attributes=True) for comics in author.comics]
