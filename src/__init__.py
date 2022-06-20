from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    MYSQL_DB_URL: str
    CHROME_DRIVER_PATH: str
    CHROME_BINARY_PATH: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str


@lru_cache()
def get_settings():
    return Settings()
