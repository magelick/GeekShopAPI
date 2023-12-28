from typing import List

from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db_session
from src.types.comics import ComicsDetail, ComicsAddForm, ComicsUpdateForm
from src.types.аuthor import AuthorDetail
from src.types.character import CharacterDetail
from src.database.models import Comics
from fastapi import APIRouter, status, Path, HTTPException

# Роутер комиксов
router = APIRouter(
    prefix="/comics",
    tags=["Комиксы авторов и персонажей"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ComicsDetail],
    name="Получение списка всех комиксов"
)
async def get_list_comics(session: Session = get_db_session):
    """
    Получение списка всех комиксов
    :param session:
    :return:
    """
    # Достаём все комиксы
    all_comics = session.scalars(select(Comics).order_by(Comics.id))
    # Возвращаем их, провалидировав через схему
    return [ComicsDetail.model_validate(obj=comics, from_attributes=True) for comics in all_comics]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ComicsDetail,
    name="Добавление нового комикса"
)
async def add_new_comics(id: PositiveInt, form: ComicsAddForm, session: Session = get_db_session):
    """
    Добавление нового комикса
    :param form:
    :param session:
    :return:
    """
    # Создаём новый комикс,валидировав через основную схему представления комиксов
    form_comics = ComicsDetail(id=None, **form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    comics = Comics(**form_comics.model_dump())
    # Добавляем новый комикс в БД
    session.add(comics)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это не обходимо
    session.refresh(comics)
    # Возвращаем новую вселенную в виде основной схемы представления вселенной
    return ComicsDetail.model_validate(obj=comics, from_attributes=True)


@router.get(
    path="/{comics_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ComicsDetail,
    name="Получение конкретный комикс"
)
async def get_comics(comics_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение кокнретный комикс
    :param comics_id:
    :param session:
    :return:
    """
    # Получение кокнретного комикса по его ID
    comics = session.scalar(select(Comics).filter_by(id=comics_id))
    # Если комикс не найден
    if comics is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого комикса не существует")
    # В другом случае возвращаем валидированные данные
    return ComicsDetail.model_validate(obj=comics, from_attributes=True)


@router.put(
    path="/{comics_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ComicsDetail,
    name="Обновление конкретного комикса"
)
async def update_comics(form: ComicsUpdateForm, comics_id: PositiveInt = Path(default=..., ge=1),
                        session: Session = get_db_session):
    """
    Обновление кокнретного комикса
    :param comics_id:
    :param form:
    :param session:
    :return:
    """
    # Получение кокнретного комикса по его ID
    comics = session.scalar(select(Comics).filter_by(id=comics_id))
    # Если комикс не найден
    if comics is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого комикса не существует")
    # Валидируем полученные данные
    form_comics = ComicsDetail(id=comics_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_comics:
        # Изменяем полученную по ID комикса
        setattr(comics, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(comics)
    # Возвращаем изменённый комикс в виде основной схемы представления комикса
    return ComicsDetail.model_validate(obj=comics, from_attributes=True)


@router.delete(
    path="/{comics_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретного комикса"
)
async def delete_comics(comics_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретного комикса
    :param comics_id:
    :param session:
    :return:
    """
    # Получение кокнретного комикса по его ID
    comics = session.scalar(select(Comics).filter_by(id=comics_id))
    # Если комикс не найден
    if comics is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого комикса не существует")
    # Удаляем выбранный комикс
    session.delete(comics)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретного комикса
    return {"msg": "Done"}


@router.get(
    path="/{comics_id}/authors/",
    status_code=status.HTTP_200_OK,
    response_model=List[AuthorDetail],
    name="Получение списка авторов конкретного автора"
)
async def get_list_authors_of_comics(comics_id: PositiveInt = Path(default=..., ge=1),
                                     session: Session = get_db_session):
    """
    Получение списка авторов конкретного автора
    :param comics_id:
    :param session:
    :return:
    """
    # Получение кокнретного комикса по его ID
    comics = session.scalar(select(Comics).filter_by(id=comics_id))
    # Если комикс не найден
    if comics is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого комикса не существует")
    # Возвращаем список авторов конкретного комикса
    return [AuthorDetail.model_validate(obj=author, from_attributes=True) for author in comics.authors]


@router.get(
    path="/{comics_id}/characters/",
    status_code=status.HTTP_200_OK,
    response_model=List[CharacterDetail],
    name="Получение списка персонажей конкретного комикса"
)
async def get_list_characters_of_comics(comics_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение списка персонажей конкретного комикса
    :param comics_id:
    :param session:
    :return:
    """
    # Получение кокнретного комикса по его ID
    comics = session.scalar(select(Comics).filter_by(id=comics_id))
    # Если комикс не найден
    if comics is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого комикса не существует")
    # Возвращаем список персонажей конкретного комикса
    return [CharacterDetail.model_validate(obj=character, from_attributes=True) for character in comics.characters]