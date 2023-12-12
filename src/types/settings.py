from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_STR: SecretStr