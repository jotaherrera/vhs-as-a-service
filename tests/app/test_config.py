import pytest

from app.config import Settings


def test_settings_loads_app_env_vars() -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("APP__NAME", "test_app")
        mp.setenv("APP__DEBUG", "true")
        mp.setenv("APP__VERSION", "1.0.0")

        settings = Settings()  # ty:ignore[missing-argument]

    assert settings.app.name == "test_app"
    assert settings.app.debug
    assert settings.app.version == "1.0.0"


def test_settings_loads_db_env_vars() -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("DATABASE__NAME", "test_db")
        mp.setenv("DATABASE__USER", "test_user")
        mp.setenv("DATABASE__PASSWORD", "test_password")
        mp.setenv("DATABASE__HOST", "test_host")
        mp.setenv("DATABASE__PORT", "123")

        settings = Settings()  # ty:ignore[missing-argument]

    assert settings.database.name == "test_db"
    assert settings.database.user == "test_user"
    assert settings.database.password.get_secret_value() == "test_password"
    assert settings.database.host == "test_host"
    assert settings.database.port == 123  # noqa: PLR2004


def test_database_migration_url_uses_migration_credentials_when_set() -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("APP__JWT_SECRET", "secret")
        mp.setenv("DATABASE__USER", "app_user")
        mp.setenv("DATABASE__PASSWORD", "user_pass")
        mp.setenv("DATABASE__MIGRATION_USER", "app_owner")
        mp.setenv("DATABASE__MIGRATION_PASSWORD", "owner_pass")

        settings = Settings()  # ty:ignore[missing-argument]

    assert settings.database.url.username == "app_user"
    assert settings.database.migration_url.username == "app_owner"
    assert settings.database.migration_url.password == "owner_pass"  # noqa: S105


def test_database_migration_url_falls_back_to_runtime_when_migration_unset() -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("APP__JWT_SECRET", "secret")
        mp.setenv("DATABASE__USER", "app_user")
        mp.setenv("DATABASE__PASSWORD", "user_pass")

        settings = Settings()  # ty:ignore[missing-argument]

    assert settings.database.migration_url.username == "app_user"
    assert settings.database.migration_url == settings.database.url
