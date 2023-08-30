from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int
    DB_URL: str
    SECRET_KEY: str
    REFRESH_SECRET: str
    ACCESS_TOKEN_EXPIRY_MINUTES: int
    REFRESH_TOKEN_EXPIRY_DAYS: int
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
