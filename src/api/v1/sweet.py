from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Sweet
from src.dependencies import get_db_session
from src.types import UniverseDetail
from src.types.sweet import SweetDetail, SweetAddForm, SweetUpdateForm
from src.types.character import CharacterDetail

# Роутер сладостей
router = APIRouter(
    prefix="/sweets",
    tags=["Сладости персонажей"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[SweetDetail],
    name="Получение списка сладостей"
)
async def get_list_of_sweets(session: Session = get_db_session):
    """
    Получение списка сладостей
    :param session:
    :return:
    """
    # Достаём все сладости
    sweets = session.scalars(select(Sweet).order_by(Sweet.id))
    # Возвращаем список всех сладостей
    return [CharacterDetail.model_validate(obj=sweet, from_attributes=True) for sweet in sweets]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=SweetDetail,
    name="Добавление новой сладости"
)
async def add_new_sweet(form: SweetAddForm, session: Session = get_db_session):
    """
    Добавление новой сладости
    :param form:
    :param session:
    :return:
    """
    # Создаём новую сладость, валидировав через основную схему представления сладости
    form_sweet = SweetDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    sweet = Sweet(**form_sweet.model_dump())
    # Добавляем новой сладости в БД
    session.add(sweet)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем id, если это не обходимо
    session.refresh(sweet)
    # Возвращаем новую сладость в виде основной схемы представления сладости
    return SweetDetail.model_validate(obj=sweet, from_attributes=True)


@router.get(
    path="/{sweet_id}/",
    status_code=status.HTTP_200_OK,
    response_model=SweetDetail,
    name="Получение конкретной сладости"
)
async def get_sweet(sweet_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение конкретной сладости
    :param sweet_id:
    :param session:
    :return:
    """
    # Достаём конкретную сладость по его ID
    sweet = session.scalar(select(Sweet).filter_by(id=sweet_id))
    # Если сладость не найдена
    if sweet is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой сладости не существует")
    # В другом случае возвращаем валидированные данные
    return SweetDetail.model_validate(obj=sweet, from_attributes=True)


@router.put(
    path="/{sweet_id}/",
    status_code=status.HTTP_200_OK,
    response_model=SweetDetail,
    name="Обновление конкретной сладости"
)
async def update_sweet(form: SweetUpdateForm, sweet_id: PositiveInt = Path(default=..., ge=1),
                       session: Session = get_db_session):
    """
    Обновление конкретной сладости
    :param form:
    :param sweet_id:
    :param session:
    :return:
    """
    # Достаём конкретную сладость
    sweet = session.scalar(select(Sweet).filter_by(id=sweet_id))
    # Если сладость не найдена
    if sweet is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой сладости не существует")
    # Валидируем полученные данные
    form_sweet = SweetDetail(**form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_sweet:
        # Изменяем полученную по ID сладость
        setattr(sweet, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(sweet)
    # Возвращаем изменённую сладость в виде основной схемы представления сладости
    return SweetDetail.model_validate(obj=sweet, from_attributes=True)


@router.delete(
    path="/{sweet_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретной сладости"
)
async def delete_sweet(sweet_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретной сладости
    :param sweet_id:
    :param session:
    :return:
    """
    # Достаём конкретную сладость
    sweet = session.scalar(select(Sweet).filter_by(id=sweet_id))
    # Если сладость не найдена
    if sweet is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой сладости не существует")
    # Удаляем выбранную сладость
    session.delete(sweet)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретной сладости
    return {"msg": "Done"}


@router.get(
    path="/{sweet_id}/character/",
    status_code=status.HTTP_200_OK,
    response_model=CharacterDetail,
    name="Получение персонажа конкретной сладости"
)
async def get_character_of_sweet(sweet_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение персонажа конкретной сладости
    :param sweet_id:
    :param session:
    :return:
    """
    # Достаём конкретную сладость
    sweet = session.scalar(select(Sweet).filter_by(id=sweet_id))
    # Если сладость не найдена
    if sweet is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой сладости не существует")
    # Возвращаем конкретного персонажа, к которому относиться конкретная сладость
    return CharacterDetail.model_validate(obj=sweet.character, from_attributes=True)


@router.get(
    path="/{sweet_id}/universe/",
    status_code=status.HTTP_200_OK,
    response_model=CharacterDetail,
    name="Получение вселенной конкретной сладости"
)
async def get_universe_of_sweet(sweet_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение вселенной конкретной сладости
    :param sweet_id:
    :param session:
    :return:
    """
    # Достаём конкретную сладость
    sweet = session.scalar(select(Sweet).filter_by(id=sweet_id))
    # Если сладость не найдена
    if sweet is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой сладости не существует")
    # Возвращаем конкретную вселенную, к которой относиться конкретная сладость
    return UniverseDetail.model_validate(obj=sweet.character.universe, from_attributes=True)


