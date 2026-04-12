import pytest

from app.core.config import Settings


def test_settings_loads_app_env_vars() -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("APP__DEBUG", "true")
        mp.setenv("APP__JWT_SECRET", "test_secret")

        settings = Settings()  # ty:ignore[missing-argument]

    assert settings.app.name == "vhsaas"
    assert settings.app.version == "0.1.0"
    assert settings.app.debug is True
    assert settings.app.jwt_secret.get_secret_value() == "test_secret"


def test_settings_loads_db_env_vars() -> None:
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("DATABASE__USER", "test_user")
        mp.setenv("DATABASE__PASSWORD", "test_password")
        mp.setenv("DATABASE__HOST", "test_host")
        mp.setenv("DATABASE__PORT", "123")

        settings = Settings()  # ty:ignore[missing-argument]

    assert settings.database.name == "vhsaas"
    assert settings.database.user == "test_user"
    assert settings.database.password.get_secret_value() == "test_password"
    assert settings.database.host == "test_host"
    assert settings.database.port == 123
