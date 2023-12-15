from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn = "postgresql://admin1:qwerty@0.0.0.0:5432/geek_shop"