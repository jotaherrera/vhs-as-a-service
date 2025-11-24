from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env")

    name: str
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432

    @property
    def connection_url(self) -> URL:
        return URL.create(
            drivername="postgresql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")

    app_name: str = "pluto"
    debug: bool = False

    database: DatabaseSettings = Field(default_factory=DatabaseSettings)

SETTINGS = Settings()
