from .base import Base
from sqlalchemy import Column, CHAR, VARCHAR, CheckConstraint, SMALLINT, ForeignKey, INT, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ulid import new


class User(Base):
    """
    Модель пользователя в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(name) >= 4'),
    )

    id = Column(CHAR(26), primary_key=True, default=lambda: new().str, )
    name = Column(VARCHAR(length=64), nullable=False)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(VARCHAR(length=128), nullable=False)

    def __repr__(self):
        return f"{self.name}"


class Universe(Base):
    """
    Модель вселенной в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(title) >= 4'),
        CheckConstraint('char_length(slug) >= 4'),
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    title = Column(VARCHAR(length=64), nullable=False, unique=True)
    date_created = Column(DATETIME, nullable=False, unique=True)
    characters = relationship(argument="Character", back_populates="universe")
    devices = relationship(argument="Device", back_populates="universe")
    toys = relationship(argument="Toy", back_populates="universe")

    def __repr__(self):
        return f"{self.title}"


class Author(Base):
    """
    Модель автора в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(slug) >= 4'),
        CheckConstraint('char_length(name) >= 4'),
        CheckConstraint('char_length(surname) >= 4'),
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    name = Column(VARCHAR(length=64), nullable=False, unique=True)
    surname = Column(VARCHAR(length=64), nullable=False, unique=True)
    birthday = Column(DATETIME, nullable=False)
    characters = relationship(argument="Character", back_populates="author")
    comics = relationship("Comics", secondary="ComicsAuthors", back_populates="authors")

    def __repr__(self):
        return f"{self.name}"


class Character(Base):
    """
    Модель персонажа в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(name) >= 2'),
        CheckConstraint('char_length(role) >= 4'),
        CheckConstraint('char_length(power) >= 4'),
        CheckConstraint('char_length(slug) >= 4')
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    name = Column(VARCHAR(length=64), nullable=False)
    date_created = Column(DATETIME, nullable=False)
    role = Column(VARCHAR(length=64), nullable=False)
    power = Column(VARCHAR(length=128), nullable=False)
    universe_id = Column(SMALLINT, ForeignKey(column="universe.id", ondelete="CASCADE"), nullable=False, index=True),
    universe = relationship(argument="Universe", back_populates="characters")
    author_id = Column(SMALLINT, ForeignKey('author.id', ondelete="CASCADE"), nullable=False, index=True)
    author = relationship(argument="Author", back_populates="characters")
    devices = relationship(argument="Device", back_populates="character")
    sweets = relationship(argument="Sweet", back_populates="character")
    toys = relationship(argument="Toy", back_populates="universe")
    comics = relationship(argument="Comics", secondary="ComicsCharacters", back_populates="characters")

    def __repr__(self):
        return f"{self.name}"


class Comics(Base):
    """
    Модель комикса в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(title) >= 4'),
        CheckConstraint('char_length(country) >= 4'),
        CheckConstraint('char_length(slug) >= 4')
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    title = Column(VARCHAR(length=128), nullable=False, unique=True)
    volume = Column(INT, nullable=False)
    date_created = Column(DATETIME, nullable=False)
    price = Column(DECIMAL, nullable=False)
    country = Column(VARCHAR(length=64), nullable=False)
    authors = relationship("Author", secondary="ComicsAuthors", back_populates="comics")
    characters = relationship(argument="Character", secondary="ComicsCharacters", back_populates="comics")

    def __repr__(self):
        return f"{self.title}"


class Device(Base):
    """
    Модель девайса в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(slug) >= 4'),
        CheckConstraint('char_length(title) >= 4'),
        CheckConstraint('char_length(type_of_device) >= 4'),
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    title = Column(VARCHAR(length=128), nullable=False, unique=True)
    type_of_device = Column(VARCHAR(length=64), nullable=False)
    price = Column(DECIMAL, nullable=False)
    universe_id = Column(SMALLINT, ForeignKey(column="universe.id", ondelete="CASCADE"), nullable=False, index=True),
    universe = relationship(argument="Universe", back_populates="devices")
    character_id = Column(SMALLINT, ForeignKey(column="character.id", ondelete="CASCADE"), nullable=False, index=True),
    character = relationship(argument="Character", back_populates="devices")

    def __repr__(self):
        return f"{self.title}"


class Sweet(Base):
    """
    Модель сладости в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(slug) >= 4'),
        CheckConstraint('char_length(title) >= 4')
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    title = Column(VARCHAR(length=128), nullable=False, unique=True)
    price = Column(DECIMAL, nullable=False)
    weight = Column(INT, nullable=False)
    character_id = Column(SMALLINT, ForeignKey(column="character.id", ondelete="CASCADE"), nullable=False, index=True),
    character = relationship(argument="Character", back_populates="sweets")

    def __repr__(self):
        return f"{self.title}"


class Toy(Base):
    """
    Модель игрушки в БД
    """
    __table_args__ = (
        CheckConstraint('char_length(slug) >= 4'),
        CheckConstraint('char_length(title) >= 4'),
        CheckConstraint('char_length(type_of_toy) >= 4')
    )

    id = Column(SMALLINT, primary_key=True)
    slug = Column(VARCHAR(length=128), nullable=False, unique=True)
    title = Column(VARCHAR(length=128), nullable=False, unique=True)
    age = Column(INT, nullable=False)
    type_of_toy = Column(VARCHAR(length=64), nullable=False)
    price = Column(DECIMAL, nullable=False)
    universe_id = Column(SMALLINT, ForeignKey(column="universe.id", ondelete="CASCADE"), nullable=False, index=True),
    universe = relationship(argument="Universe", back_populates="toys")
    character_id = Column(SMALLINT, ForeignKey(column="character.id", ondelete="CASCADE"), nullable=False, index=True),
    character = relationship(argument="Character", back_populates="toys")


class ComicsAuthors(Base):
    """
    Промежуточная таблица между моделями комикса и автора
    """
    comics_id = Column(SMALLINT, ForeignKey("comics.id", ondelete="NO ACTION"), primary_key=True, nullable=False,
                       index=True)
    author_id = Column(SMALLINT, ForeignKey("author.id", ondelete="NO ACTION"), primary_key=True, nullable=False,
                       index=True)


class ComicsCharacters(Base):
    """
    Промежуточная таблица между моделями комикса и персонажа
    """
    comics_id = Column(SMALLINT, ForeignKey("comics.id", ondelete="NO ACTION"), primary_key=True, nullable=False,
                       index=True)
    character_id = Column(SMALLINT, ForeignKey("character.id"), onupdate="NO ACTION", primary_key=True, nullable=False,
                          index=True)
