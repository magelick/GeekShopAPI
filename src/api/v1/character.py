from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from fastapi.responses import ORJSONResponse
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Character
from src.dependencies import get_db_session
from src.types.character import CharacterAddForm, CharacterDetail, CharacterUpdateForm
from src.types.universe import UniverseDetail
from src.types.аuthor import AuthorDetail
from src.types.device import DeviceDetail
from src.types.sweet import SweetDetail
from src.types.toy import ToyDetail

# Роутер персонажей комиксов и вселенных
router = APIRouter(
    prefix="/characters",
    tags=["Персонажи комиксов и вселенных"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[CharacterDetail],
    name="Получение списка всех персонажей"
)
async def get_list_characters(session: Session = get_db_session):
    """
    Получение списка всех персонажей
    :param session:
    :return:
    """
    # Достаём всех персонажей
    characters = session.scalars(select(Character).order_by(Character.id))
    # Возвращаем список всех персонажей
    return [CharacterDetail.model_validate(obj=character, from_attributes=True) for character in characters]


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=CharacterDetail,
    name="Добавление нового персонажа"
)
async def add_new_character(form: CharacterAddForm, session: Session = get_db_session):
    """
    Добавление нового персонажа
    :param form:
    :param session:
    :return:
    """
    # Создаём нового персонажа, валидировав через основную схему представления персонажа
    form_character = CharacterDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    character = Character(**form_character.model_dump())
    # Добавляем нового персонажа в БД
    session.add(character)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это не обходимо
    session.refresh(character)
    # Возвращаем нового персонажа в виде основной схемы представления персонажа
    return CharacterDetail.model_validate(obj=character, from_attributes=True)


@router.get(
    path="/{character_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CharacterDetail,
    name="Получение конкретного персонажа"
)
async def get_character(character_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Получение конкретного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # В другом случае возвращаем валидированные данные
    return CharacterDetail.model_validate(obj=character, from_attributes=True)


@router.put(
    path="/{character_id}/",
    status_code=status.HTTP_200_OK,
    response_model=CharacterDetail,
    name="Обновление конкретного персонажа"
)
async def update_character(form: CharacterUpdateForm, character_id: PositiveInt = Path(default=..., ge=1),
                           session: Session = get_db_session):
    """
    Обновление конкретного персонажа
    :param form:
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Валидируем полученные данные
    form_character = CharacterDetail(id=character_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_character:
        # Изменяем полученного по ID персонажа
        setattr(character, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(character)
    # Возвращаем изменённого персонажа в виде основной схемы представления персонажа
    return CharacterDetail.model_validate(obj=character, from_attributes=True)


@router.delete(
    path="/{character_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретного персонажа"
)
async def delete_character(character_id: PositiveInt = Path(default=..., ge=1), session: Session = get_db_session):
    """
    Удаление конкретного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Удаляем выбранного персонажа
    session.delete(character)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретного персонажа
    return {"msg": "Done"}


@router.get(
    path="/{character_id}/universe/",
    status_code=status.HTTP_200_OK,
    response_model=UniverseDetail,
    name="Получение вселенной конкретного персонажа"
)
async def get_universe_of_character(character_id: PositiveInt = Path(default=..., ge=1),
                                    session: Session = get_db_session):
    """
    Получение вселенной конкретного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Возвращаем конкретную вселенную конкретного персонажа
    return UniverseDetail.model_validate(obj=character.universe, from_attributes=True)


@router.get(
    path="/{character_id}/author/",
    status_code=status.HTTP_200_OK,
    response_model=AuthorDetail,
    name="Получение автора конкретного персонажа"
)
async def get_author_of_character(character_id: PositiveInt = Path(default=..., ge=1),
                                  session: Session = get_db_session):
    """
    Получение автора конкретного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Возвращаем конкретного автора конкретного персонажа
    return AuthorDetail.model_validate(obj=character.author, from_attributes=True)


@router.get(
    path="/{character_id}/devices/",
    status_code=status.HTTP_200_OK,
    response_model=List[DeviceDetail],
    name="Получение списка девайсов кокнертного персонажа"
)
async def get_list_devices_of_character(character_id: PositiveInt = Path(default=..., ge=1),
                                        session: Session = get_db_session):
    """
    Получение списка девайсов кокнертного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Возвращаем список девайсов, к которому относится конкретный персонаж
    return [DeviceDetail.model_validate(obj=device, from_attributes=True) for device in character.devices]


@router.get(
    path="/{character_id}/sweets/",
    status_code=status.HTTP_200_OK,
    response_model=List[SweetDetail],
    name="Получение списка сладостей конкретного персонажа"
)
async def get_list_sweets_of_character(character_id: PositiveInt = Path(default=..., ge=1),
                                       session: Session = get_db_session):
    """
    Получение списка сладостей конкретного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Возвращаем список сладостей, к которому относится конкретный персонаж
    return [SweetDetail.model_validate(obj=sweet, from_attributes=True) for sweet in character.sweets]


@router.get(
    path="/{character_id}/toys/",
    status_code=status.HTTP_200_OK,
    response_model=List[ToyDetail],
    name="Получение списка игрушек конркетного персонажа"
)
async def get_list_toys_of_character(character_id: PositiveInt = Path(default=..., ge=1),
                                     session: Session = get_db_session):
    """
    Получение списка игрушек конркетного персонажа
    :param character_id:
    :param session:
    :return:
    """
    # Достаём конкретного персонажа по его ID
    character = session.scalar(select(Character).filter_by(id=character_id))
    # Если персонаж не найден
    if character is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого персонажа не существует")
    # Возвращаем список игрушек, к которому относится конкретный персонаж
    return [ToyDetail.model_validate(obj=toy, from_attributes=True) for toy in character.toys]

