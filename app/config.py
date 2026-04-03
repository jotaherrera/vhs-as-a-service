from functools import lru_cache

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class AppSettings(BaseModel):
    name: str = Field(default="vhsaas", init=False)
    debug: bool
    version: str = Field(default="0.1.0", init=False)
    jwt_secret: SecretStr


class DatabaseSettings(BaseModel):
    name: str = Field(default="vhsaas", init=False)
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
