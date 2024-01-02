from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Device
from src.dependencies import get_db_session
from src.types import UniverseDetail, CharacterDetail
from src.types.device import DeviceDetail, DeviceAddFrom, DeviceUpdateForm

# Роутер девайсов
router = APIRouter(
    prefix="/devices",
    tags=["Девайсы персонажей и вселенных"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[DeviceDetail],
    name="Получение списка девайсов"
)
async def get_list_of_devices(session: Session = get_db_session):
    """
    Получение списка девайсов
    :param session:
    :return:
    """
    # Достаём все девайсы
    devices = session.scalars(select(Device).order_by(Device.id))
    # Возвращаем список всех девайсов
    return [DeviceDetail.model_validate(obj=device, from_attributes=True) for device in devices]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DeviceDetail,
    name="Добавление нового девайса"
)
async def add_new_device(form: DeviceAddFrom, session: Session = get_db_session):
    """
    Добавление нового девайса
    :param form:
    :param session:
    :return:
    """
    # Создаём новый девайс, валидировав через основную схему представления девайса
    form_device = DeviceDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    device = Device(**form_device.model_dump())
    # Добавляем новый девайс в БД
    session.add(device)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(device)
    # Возвращаем новый девайс в виде основной схемы представления девайса
    return DeviceDetail.model_validate(obj=device, from_attributes=True)


@router.get(
    path="/{device_id}/",
    status_code=status.HTTP_200_OK,
    response_model=DeviceDetail,
    name="Получение конкретного девайса"
)
async def get_device(device_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение конкретного девайса
    :param device_id:
    :param session:
    :return:
    """
    # Достаём кокнертный девайс по его ID
    device = session.scalar(select(Device).filter_by(id=device_id))
    # Если девайс не найден
    if device is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого девайса не существует")
    # В другом случае возвращаем валидированные данные
    return DeviceDetail.model_validate(obj=device, from_attributes=True)


@router.put(
    path="/{device_id}/",
    status_code=status.HTTP_200_OK,
    response_model=DeviceDetail,
    name="Обновление конкретного девайса"
)
async def update_device(form: DeviceUpdateForm, device_id: PositiveInt = Path(default=..., ge=1),
                        session: Session = get_db_session):
    """
    Обновление конкретного девайса
    :param form:
    :param device_id:
    :param session:
    :return:
    """
    # Достаём кокнертный девайс по его ID
    device = session.scalar(select(Device).filter_by(id=device_id))
    # Если девайс не найден
    if device is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого девайса не существует")
    # Валидируем полученные данные
    form_device = DeviceDetail(id=device_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_device:
        # Изменяем полученный по ID девайс
        setattr(device, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(device)
    # Возвращаем изменённый девайс в виде основной схемы представления девайса
    return DeviceDetail.model_validate(obj=device, from_attributes=True)


@router.delete(
    path="/{device_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретного девайса"
)
async def delete_device(device_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретного девайса
    :param device_id:
    :param session:
    :return:
    """
    # Достаём кокнертный девайс по его ID
    device = session.scalar(select(Device).filter_by(id=device_id))
    # Если девайс не найден
    if device is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого девайса не существует")
    # Удаляем выбранный девайс
    session.delete(device)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретного девайса
    return {"msg": "Done"}


@router.get(
    path="/{device_id}/universe/",
    status_code=status.HTTP_200_OK,
    response_model=UniverseDetail,
    name="Получение вселенной конкретного девайса"
)
async def get_universe_of_device(device_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение вселенной конкретного девайса
    :param device_id:
    :param session:
    :return:
    """
    # Достаём кокнертный девайс по его ID
    device = session.scalar(select(Device).filter_by(id=device_id))
    # Если девайс не найден
    if device is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого девайса не существует")
    # Возвращаем конкретную вселенную, к которой относиться конкретный девайс
    return UniverseDetail.model_validate(obj=device.unverse, from_attributes=True)


@router.get(
    path="/{device_id}/character/",
    status_code=status.HTTP_200_OK,
    response_model=CharacterDetail,
    name="Получение персонажа конкретного девайса"
)
async def get_character_of_device(device_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение персонажа конкретного девайса
    :param device_id:
    :param session:
    :return:
    """
    # Достаём кокнертный девайс по его ID
    device = session.scalar(select(Device).filter_by(id=device_id))
    # Если девайс не найден
    if device is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого девайса не существует")
    # Возвращаем конкретного персонажа, к которому относиться конкретный девайс
    return CharacterDetail.model_validate(obj=device.character, from_attributes=True)
