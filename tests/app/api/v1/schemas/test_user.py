import pytest
from pydantic import SecretStr, ValidationError

from app.modules.users.schemas import UserLogin


def test_user_login_invalid_email() -> None:
    with pytest.raises(ValidationError) as ex:
        UserLogin(email="not-a-valid-email.com", password=SecretStr("test-password"))

    errors = ex.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("email",)
    assert errors[0]["type"] == "value_error"
