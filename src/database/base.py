from sqlalchemy import Column, INT, create_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker
from src.settings import SETTINGS


class Base(DeclarativeBase):
    """
    Базовая модель для всех других моделей БД
    """
    # ID таблицы
    id = Column(INT, primary_key=True)

    engine = create_engine(url=SETTINGS.DATABASE_URL.unicode_string())
    session = sessionmaker(bind=engine)

    @declared_attr
    def __tablename__(cls) -> str:
        return ''.join(f'_{i.lower()}' if i.isupper() else i for i in cls.__name__).strip('_')
