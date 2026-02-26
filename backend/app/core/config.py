from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'coins-platform'
    environment: str = 'dev'
    debug: bool = False
    api_prefix: str = '/api/v1'

    database_url: str = Field(default='postgresql+asyncpg://postgres:postgres@db:5432/coins')

    jwt_secret_key: str = 'change_me'
    jwt_algorithm: str = 'HS256'
    access_token_minutes: int = 30
    refresh_token_days: int = 14

    cors_origins: str = 'http://localhost:3000,http://localhost:5173'


@lru_cache
def get_settings() -> Settings:
    return Settings()
