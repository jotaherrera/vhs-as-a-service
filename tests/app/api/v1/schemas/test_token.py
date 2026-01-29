import pytest
from pydantic import ValidationError

from app.api.v1.schemas.token import TokenRequest


def test_token_request_invalid_email() -> None:
    with pytest.raises(ValidationError) as ex:
        TokenRequest(email="not-a-valid-email.com", password="test-password")  # noqa: S106

    errors = ex.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("email",)
    assert errors[0]["type"] == "value_error"
