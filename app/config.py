from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL


class AppSettings(BaseModel):
    name: str = "pluto"
    debug: bool = False
    version: str = "0.1.0"


class DatabaseSettings(BaseModel):
    name: str
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432
    container_name: str

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
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    app: AppSettings
    database: DatabaseSettings


settings = Settings()
