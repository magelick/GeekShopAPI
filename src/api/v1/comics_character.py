from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db_session
from src.types.comics_character import ComicsCharacterDetail, ComicsCharacterUpdateForm, ComicsCharacterAddForm
from src.database.models import ComicsCharacters

router = APIRouter(
    prefix="/comics_character",
    tags=["Связь комиксов и персонажей"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ComicsCharacterDetail],
    name="Получение списка между комиксами и персонаами"
)
async def get_comics_characters(session: Session = get_db_session):
    """
    Получение списка между комиксами и персонаами
    :param session:
    :return:
    """
    # Получение списка всех связей между комиксами и персонажами
    comics_characters = session.scalars(select(ComicsCharacters).order_by(ComicsCharacters.id))
    # Возвращаем список всех связей между комиксами и персонажами
    return [ComicsCharacterDetail.model_validate(obj=comic_character, from_attributes=True) for comic_character in
            comics_characters]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ComicsCharacters,
    name="Добавление новой связи между комиксами и персонажами"
)
async def add_new_comics_characters(form: ComicsCharacterAddForm, session: Session = get_db_session):
    """
    Добавление новой связи между комиксами и персонажами
    :param form:
    :param session:
    :return:
    """
    #
    form_comics_characters = ComicsCharacterDetail(**form.model_dump())
    #
    comics_characters = ComicsCharacters(**form_comics_characters.model_dump())
    #
    session.add(comics_characters)
    #
    session.commit()
    #
    session.refresh(comics_characters)
    #
    return ComicsCharacterDetail.model_validate(obj=comics_characters, from_attributes=True)


@router.get(
    path="/{comics_character_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ComicsCharacterDetail,
    name="Получение конкретной связи между комиксами и персонажами"
)
async def get_comics_character(comics_character_id: PositiveInt = Path(default=..., ge=1),
                               session: Session = get_db_session):
    """
    Получение конкретной связи между комиксами и персонажами
    :param comics_character_id:
    :param session:
    :return:
    """
    # Достаём конкретную связь между комиксами и персонажами по её ID
    comics_character = session.scalar(select(ComicsCharacters).filter_by(id=comics_character_id))
    # Если связь не найдена
    if comics_character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи не существует")
    # В другом случае возвращаем валидированные данные
    return ComicsCharacterDetail.model_validate(obj=comics_character, from_attributes=True)


@router.put(
    path="/{comics_character_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ComicsCharacterDetail,
    name="Обновление конкретной связи между комиксами и персонажами"
)
async def update_comics_character(form: ComicsCharacterUpdateForm,
                                  comics_character_id: PositiveInt = Path(default=..., ge=1),
                                  session: Session = get_db_session):
    """
    Обновление конкретной связи между комиксами и персонажами
    :param form:
    :param comics_character_id:
    :param session:
    :return:
    """
    # Достаём конкретную связь между комиксами и персонажами по её ID
    comics_character = session.scalar(select(ComicsCharacters).filter_by(id=comics_character_id))
    # Если связь не найдена
    if comics_character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи не существует")
    # Валидируем полученные данные
    form_comics_character = ComicsCharacterDetail(id=comics_character_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_comics_character:
        # Изменяем полученую по ID связь
        setattr(comics_character, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(comics_character)
    # Возвращаем изменённую связь в виде основной схемы представления связи между комиксоми и персонажами
    return ComicsCharacterDetail.model_validate(obj=comics_character, from_attributes=True)


@router.delete(
    path="/{comics_character_id}/",
    status_code=status.HTTP_200_OK,
    name="Обновление конкретной связи между комиксами и персонажами"
)
async def delete_comics_character(comics_character_id: PositiveInt = Path(default=..., ge=1),
                                  session: Session = get_db_session):
    """
    Обновление конкретной связи между комиксами и персонажами
    :param comics_character_id:
    :param session:
    :return:
    """
    # Достаём конкретную связь между комиксами и персонажами по её ID
    comics_character = session.scalar(select(ComicsCharacters).filter_by(id=comics_character_id))
    # Если связь не найдена
    if comics_character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи не существует")
    # Удаляем выбранную связь между комиксами и персонажами
    session.delete(comics_character)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретной связи сежду комиксами и персонажами
    return {"msg": "Done"}

