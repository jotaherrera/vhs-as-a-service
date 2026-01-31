import pytest
from pydantic import SecretStr, ValidationError

from app.operations.user.schemas import UserCreateBase, UserUpdate


def test_user_create_base_password_printing() -> None:
    password = "test-password"  # noqa: S105
    user_create = UserCreateBase(
        email="johndoe@mail.com",
        name="John",
        last_name="Doe",
        password=SecretStr(password),
    )

    assert user_create.password != password
    assert user_create.password.get_secret_value() == password


def test_user_create_base_password_min_length() -> None:
    short_password = "1234567"  # noqa: S105
    with pytest.raises(ValidationError) as exc:
        UserCreateBase(
            email="johndoe@mail.com",
            name="John",
            last_name="Doe",
            password=SecretStr(short_password),
        )

    errors = exc.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("password",)
    assert errors[0]["type"] == "too_short"


def test_user_create_base_password_max_length() -> None:
    long_password = "12345678901234567890123456789012345678901234567890123456789012345"  # noqa: S105
    with pytest.raises(ValidationError) as exc:
        UserCreateBase(
            email="johndoe@mail.com",
            name="John",
            last_name="Doe",
            password=SecretStr(long_password),
        )

    errors = exc.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("password",)
    assert errors[0]["type"] == "too_long"


def test_user_update_invalid_email() -> None:
    with pytest.raises(ValidationError) as ex:
        UserUpdate(email="not-a-valid-mail.com", password=SecretStr("test-password"))

    errors = ex.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("email",)
    assert errors[0]["type"] == "value_error"
