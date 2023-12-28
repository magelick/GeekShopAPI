from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Comics, Author, ComicsAuthors
from src.dependencies import get_db_session
from src.types.comics_author import ComicsAuthorDetail, ComicsAuthorAddForm

router = APIRouter(
    prefix="/comics_author",
    tags=["Связь Комиксов и Авторов"]
)


@router.post(
    path="/",
    response_model=ComicsAuthorDetail,
    status_code=status.HTTP_200_OK,
    name="Добавление комиксов к авторам и наоборот"
)
async def add_new_comics_authors(form: ComicsAuthorAddForm, session: Session = get_db_session):
    """
    Добавление комиксов к авторам и наоборот
    :param form:
    :param session:
    :return:
    """
    # Создаём новую вселенную, валидировав через основную схему представления вселенной
    form_comics_author = ComicsAuthorDetail(**form.model_dump())
    # Затем создаём новый экземпляр модели на основе провалидированых данных
    comics_author = ComicsAuthors(**form_comics_author.model_dump())
    # Добавляем новую вселеную в БД
    session.add(comics_author)
    # Сохраняем изменения
    session.commit()
    # Возвращаем новую вселенную в виде основной схемы представления вселенной
    return ComicsAuthorDetail.model_validate(obj=comics_author, from_attributes=True)


