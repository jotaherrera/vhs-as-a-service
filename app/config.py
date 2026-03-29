import logging
from functools import lru_cache

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL

LOGGER = logging.getLogger(__name__)


class AppSettings(BaseModel):
    name: str = "vhsaas"
    debug: bool = False
    version: str = "0.1.0"
    jwt_secret: SecretStr


class DatabaseSettings(BaseModel):
    name: str = "vhsaas"
    user: str
    password: SecretStr
    host: str = "localhost"
    port: int = 5432
    migration_user: str | None = None
    migration_password: SecretStr | None = None

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

    @property
    def migration_url(self) -> URL:
        if self.migration_user is not None and self.migration_password is not None:
            return URL.create(
                drivername="postgresql",
                username=self.migration_user,
                password=self.migration_password.get_secret_value(),
                host=self.host,
                port=self.port,
                database=self.name,
            )
        LOGGER.debug("Migration credentials not set; using runtime URL")
        return self.url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=(".env", ".env.test"),
        extra="ignore",
    )

    app: AppSettings
    database: DatabaseSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()  # ty:ignore[missing-argument]
