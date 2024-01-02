from typing import List

from fastapi import APIRouter, status, Path, HTTPException
from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.responses import ORJSONResponse

from src.database.models import Comics, Author, ComicsAuthors
from src.dependencies import get_db_session
from src.types.comics_author import ComicsAuthorsDetail, ComicsAuthorsAddForm, ComicsAuthorsUpdateForm

router = APIRouter(
    prefix="/comics_authors",
    tags=["Связь Комиксов и Авторов"],
    default_response_class=ORJSONResponse
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=List[ComicsAuthorsDetail],
    name="Получение списка связей между комиксами и авторами"
)
async def get_comics_authors(session: Session = get_db_session):
    """
    Получение списка связей между комиксами и авторами
    :param session:
    :return:
    """
    # Получение списка всех связей между комиксами и авторами
    comics_authors = session.scalars(select(ComicsAuthors).order_by(ComicsAuthors.id))
    # Возвращаем список всех связей между комиксами и авторами
    return [ComicsAuthorsDetail.model_validate(obj=comic_author, from_attributes=True) for comic_author in
            comics_authors]


@router.post(
    path="/",
    response_model=ComicsAuthorsDetail,
    status_code=status.HTTP_200_OK,
    name="Добавление связи между комиксами и авторами"
)
async def add_new_comics_authors(form: ComicsAuthorsAddForm, session: Session = get_db_session):
    """
    Добавление связи между комиксами и авторами
    :param form:
    :param session:
    :return:
    """
    # Создаём новую связь, валидировав через основную схему представления связи между комиксами и авторами
    form_comics_author = ComicsAuthorsDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    comics_author = ComicsAuthors(**form_comics_author.model_dump())
    # Добавляем новую вселеную в БД
    session.add(comics_author)
    # Сохраняем изменения
    session.commit()
    # Возвращаем новую связь в виде основной схемы представления связи между кимксами и авторами
    return ComicsAuthorsDetail.model_validate(obj=comics_author, from_attributes=True)


@router.get(
    path="/{comics_authors_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ComicsAuthorsDetail,
    name="Получение конкретной связи между комиксами и авторами"
)
async def get_comics_author(comics_authors_id: PositiveInt = Path(default=..., ge=1),
                            session: Session = get_db_session):
    """
    Получение конкретной связи между комиксами и авторами
    :param comics_authors_id:
    :param session:
    :return:
    """
    # Достаём конкретную связь между комиксами и авторами по её ID
    comics_authors = session.scalar(select(ComicsAuthors).filter_by(id=comics_authors_id))
    # Если связь не найден
    if comics_authors is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи не существует")
    # В другом случае возвращаем валидированные данные
    return ComicsAuthorsDetail.model_validate(obj=comics_authors, from_attributes=True)


@router.put(
    path="/{comics_authors_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ComicsAuthorsDetail,
    name="Обновление конкретной связи между комиксами и авторами"
)
async def update_comics_author(form: ComicsAuthorsUpdateForm, comics_authors_id: PositiveInt = Path(default=..., ge=1),
                               session: Session = get_db_session):
    """
    Обновление конкретной связи между комиксами и авторами
    :param form:
    :param comics_authors_id:
    :param session:
    :return:
    """
    # Достаём конкретную связь между комиксами и авторами по её ID
    comics_authors = session.scalar(select(ComicsAuthors).filter_by(id=comics_authors_id))
    # Если связь не найден
    if comics_authors is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи не существует")
    # Валидируем полученные данные
    form_comics_authors = ComicsAuthorsDetail(id=comics_authors_id, **form.model_dump())
    # Достаём ключи и их значения в провалидированных данных
    for name, value in form_comics_authors:
        # Изменяем полученого по ID автора
        setattr(comics_authors, name, value)
    # Сохраняем изменения в БД
    session.commit()
    # Дописываем ID, если это необходимо
    session.refresh(comics_authors)
    # Возвращаем изменённую связь в виде основной схемы представления связи между комиксоми и автороми
    return ComicsAuthorsDetail.model_validate(obj=comics_authors, from_attributes=True)


@router.delete(
    path="/{comics_authors_id}/",
    status_code=status.HTTP_200_OK,
    name="Удаление конкретной связи между комиксами и авторами"
)
async def delete_comics_authors(comics_authors_id: PositiveInt = Path(default=..., ge=1),
                                session: Session = get_db_session):
    """
    Удаление конкретной связи между комиксами и авторами
    :param comics_authors_id:
    :param session:
    :return:
    """
    # Достаём конкретную связь между комиксами и авторами по её ID
    comics_authors = session.scalar(select(ComicsAuthors).filter_by(id=comics_authors_id))
    # Если связь не найден
    if comics_authors is None:
        # Выдаём ошибку
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи не существует")
    # Удаляем выбранную связь между комиксами и авторами
    session.delete(comics_authors)
    # Сохраняем изменения в БД
    session.commit()
    # Возвращаем сообщение об успешном удалении конкретной связи сежду комиксами и авторами
    return {"msg": "Done"}