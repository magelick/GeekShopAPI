from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.dependencies import get_db_session
from src.types.toy import ToyDetail, ToyAddForm, ToyUpdateForm
from src.types import UniverseDetail, CharacterDetail
from src.database.models import Toy

# Роутер игрушек
router = APIRouter(
    prefix="/toys",
    tags=["Игрушки персонажей и вселенных"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ToyDetail],
    name="Получение списка игрушек"
)
async def get_list_of_toys(session: Session = get_db_session):
    """
    Получение списка игрушек
    :param session:
    :return:
    """
    # Достаём все игрушки
    toys = session.scalars(select(Toy).order_by(Toy.id))
    # Возвращаем список всех игрушек
    return [ToyDetail.model_validate(obj=toy, from_attributes=True) for toy in toys]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ToyDetail,
    name="Добавление новой игрушки"
)
async def add_new_toy(form: ToyAddForm, session: Session = get_db_session):
    """
    Добавление новой игрушки
    :param form:
    :param session:
    :return:
    """
    # Создаём новую игрушку, валидировав через основную схему представления игрушки
    form_toy = ToyDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    toy = Toy(**form_toy.model_dump())
    # Добавляем новый девайс в БД
    session.add(toy)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем id, если это не обходимо
    session.refresh(toy)
    # Возвращаем новую игрушку в виде основной схемы представления игрушки
    return ToyDetail.model_validate(obj=toy, from_attributes=True)


@router.get(
    path="/{toy_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ToyDetail,
    name="Получение конкретной игрушки"
)
async def get_toy(toy_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение конкретной игрушки
    :param toy_id:
    :param session:
    :return:
    """
    # Достаём конкретную игрушку
    toy = session.scalar(select(Toy).filter_by(id=toy_id))
    # Если игрушка не найдена
    if toy is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой игрушки не сущетсвует")
    # В другом случае возвращаем валидированные данные
    return ToyDetail.model_validate(obj=toy, from_attributes=True)


@router.put(
    path="/{toy_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ToyDetail,
    name="Обновление конкретной игрушки"
)
async def update_toy(form: ToyUpdateForm, toy_id: PositiveInt = Path(default=..., ge=1),
                     session: Session = get_db_session):
    """
    Обновление конкретной игрушки
    :param form:
    :param toy_id:
    :param session:
    :return:
    """
    # Достаём конкретную игрушку
    toy = session.scalar(select(Toy).filter_by(id=toy_id))
    # Если игрушка не найдена
    if toy is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой игрушки не сущетсвует")
    # Валидируем полученные данные
    form_toy = ToyDetail(id=toy_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_toy:
        # Изменяем полученную по ID игрушку
        setattr(toy, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(toy)
    # Возвращаем изменённую игрушку в виде основной схемы представления игрушки
    return ToyDetail.model_validate(obj=toy, from_attributes=True)


@router.delete(
    path="/{toy_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретной игрушки"
)
async def delete_toy(toy_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретной игрушки
    :param toy_id:
    :param session:
    :return:
    """
    # Достаём конкретную игрушку
    toy = session.scalar(select(Toy).filter_by(id=toy_id))
    # Если игрушка не найдена
    if toy is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой игрушки не сущетсвует")
    # Удаляем выбранную игрушку
    session.delete(toy)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретной игрушку
    return {"msg": "Done"}


@router.get(
    path="/{toy_id}/universe/",
    status_code=status.HTTP_200_OK,
    response_model=UniverseDetail,
    name="Получение вселенной игрушки"
)
async def get_universe_of_toy(toy_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение вселенной игрушки
    :param toy_id:
    :param session:
    :return:
    """
    # Достаём конкретную игрушку
    toy = session.scalar(select(Toy).filter_by(id=toy_id))
    # Если игрушка не найдена
    if toy is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой игрушки не сущетсвует")
    # Возвращаем конкретную вселенную, к которой относиться конкретная игрушка
    return UniverseDetail.model_validate(obj=toy.universe, from_attributes=True)


@router.get(
    path="/{toy_id}/character/",
    status_code=status.HTTP_200_OK,
    response_model=CharacterDetail,
    name="Получение персонажа игрушки"
)
async def get_character_of_toy(toy_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение персонажа игрушки
    :param toy_id:
    :param session:
    :return:
    """
    # Достаём конкретную игрушку
    toy = session.scalar(select(Toy).filter_by(id=toy_id))
    # Если игрушка не найдена
    if toy is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой игрушки не сущетсвует")
    # Возвращаем конкретного персонажа, к которому относиться конкретный девайс
    return UniverseDetail.model_validate(obj=toy.character, from_attributes=True)