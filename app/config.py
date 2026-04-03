from functools import lru_cache

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class AppSettings(BaseModel):
    name: str
    debug: bool
    version: str
    jwt_secret: SecretStr


class DatabaseSettings(BaseModel):
    name: str
    user: str
    password: SecretStr
    host: str
    port: int

    @property
    def url(self) -> URL:
        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=(".env.test", ".env"),
        extra="ignore",
    )

    app: AppSettings
    database: DatabaseSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]
