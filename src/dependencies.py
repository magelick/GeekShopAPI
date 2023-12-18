from sqlalchemy.orm import Session
from fastapi import Depends
from src.database.models import Base


def _get_db_session() -> Session:
    """
    Зависимость получения сессии
    :return:
    """
    # Открываем сессию
    with Base.session() as session:
        # Возращаем ёе при обращении к ней с помощью генератора для запоминания конечного состояния записанных данных в БД
        yield session


# Создаём зависимость
get_db_session = Depends(_get_db_session)
