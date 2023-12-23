from typing import List

from pydantic import PositiveInt
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.database.models import Universe
from src.dependencies import get_db_session
from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse

from src.types import CharacterDetail, DeviceDetail, ToyDetail
from src.types.universe import UniverseDetail, UniverseAddForm, UniverseUpdateForm

# Роутер вселенной
router = APIRouter(
    prefix="/universes",
    tags=["Вселенная комиксов и их персонажей"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[UniverseDetail],
    name="Получение списка всех вселенных"
)
async def get_list_universes(session: Session = get_db_session):
    """
    Получение списка всех вселенных комиксов и их персонажей
    :param session:
    :return:
    """
    # Достаём все вселенные
    universes = session.scalars(select(Universe).order_by(Universe.id))
    # Возвращаем их, провалидировав через схемки
    return [UniverseDetail.model_validate(obj=universe, from_attributes=True) for universe in universes]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=UniverseDetail,
    name="Добавление новой вселеннной"
)
async def add_new_universe(form: UniverseAddForm, session: Session = get_db_session):
    """
    Добавление новой вселенной
    :param session:
    :param form:
    :return:
    """
    # Создаём новую вселенную, валидировав через основную схему представления вселенной
    form_universe = UniverseDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    universe = Universe(**form_universe.model_dump())
    # Добавляем новую вселеную в БД
    session.add(universe)
    # Сохраняем изменения
    session.commit()
    # Дописываем id, если это не обходимо
    session.refresh(universe)
    # Возвращаем новую вселенную в виде основной схемы представления вселенной
    return UniverseDetail.model_validate(obj=universe, from_attributes=True)


@router.get(
    path="/{universe_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UniverseDetail,
    name="Получение конкретной вселенной"
)
async def get_universe(universe_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение конкретной вселенной
    :param universe_id:
    :param session:
    :return:
    """
    # Получение конкретной вселенной по её ID
    universe = session.scalar(select(Universe).filter_by(id=universe_id))
    # Если вселенной не существует
    if universe is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой вселенной не существует")
    # В другом случае возвращаем валидированные данные
    return UniverseDetail.model_validate(obj=universe, from_attributes=True)


@router.put(
    path="/{universe_id}/",
    response_model=UniverseDetail,
    status_code=status.HTTP_200_OK,
    name="Обновление конкретной вселенной"
)
async def update_universe(form: UniverseUpdateForm, universe_id: PositiveInt = Path(default=..., ge=1),
                          session: Session = get_db_session):
    """
    Изменение конкретной вселенной
    :param form:
    :param universe_id:
    :param session:
    :return:
    """
    # Достаём вселенную по её ID
    universe = session.scalar(select(Universe).filter_by(id=universe_id))
    # Если вселенная не найдена
    if universe is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой вселенной не существует")
    # Валидируем полученные данные
    form_universe = UniverseDetail(**form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_universe:
        # Изменяем полученую по ID вселенную
        setattr(universe, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(universe)
    # Возвращаем изменённую вселенную в виде основной схемы представления вселенной
    return UniverseDetail.model_validate(obj=universe, from_attributes=True)


@router.delete(
    path="/{universe_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретной категории"
)
async def delete_universe(universe_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретной вселенной
    :param universe_id:
    :param session:
    :return:
    """
    # Достаём вселенную по ID
    universe = session.scalar(select(Universe).filter_by(id=universe_id))
    # Если вселенная не найдена
    if universe is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой вселенной не существует")
    # Удаляем выбранную вселенную
    session.delete(universe)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретной вселенной
    return {"msg": "Done"}


@router.get(
    path="/{universe_id}/characters/",
    status_code=status.HTTP_200_OK,
    response_model=List[CharacterDetail],
    name="Получение всех персонажей конкретной вселенной"
)
async def get_list_character_of_universe(universe_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение списка персонажей конкретной вселенной
    :param universe_id:
    :param session:
    :return:
    """
    # Получение конкретной вселенной по её ID
    universe = session.scalar(select(Universe).filter_by(id=universe_id))
    # Если вселенная не найдена
    if universe is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой вселенной не существует")
    # Возвращаем список персонажей конкретной вселенной
    return [CharacterDetail.model_validate(character, from_attributes=True) for character in universe.characters]


@router.get(
    path="/{universe_id}/devices/",
    status_code=status.HTTP_200_OK,
    response_model=List[DeviceDetail],
    name="Получение всех девайсов конкретной вселенной"
)
async def get_list_devices_of_universe(universe_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение всех девайсов конкретной вселенной
    :param universe_id:
    :param session:
    :return:
    """
    # Получение конкретной вселенной по её ID
    universe = session.scalar(select(Universe).filter_by(id=universe_id))
    # Если вселенная не найдена
    if universe is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой вселенной не существует")
    # Возвращаем список девайсов конкретной вселенной
    return [DeviceDetail.model_validate(device, from_attributes=True) for device in universe.devices]


@router.get(
    path="/{universe_id}/toys/",
    status_code=status.HTTP_200_OK,
    response_model=List[ToyDetail],
    name="Получение всех игрушек конкретной вселенной"
)
async def get_list_toys_of_universe(universe_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение списка игрущек конкретной вселенной
    :param universe_id:
    :param session:
    :return:
    """
    # Получение конкретной вселенной по её ID
    universe = session.scalar(select(Universe).filter_by(id=universe_id))
    # Если вселенная не найдена
    if universe is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой вселенной не существует")
    # Возвращаем список игрушек конкретной категории
    return [ToyDetail.model_validate(toy, from_attributes=True) for toy in universe.toys]
