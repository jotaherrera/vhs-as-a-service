from fastapi import status
from fastapi.testclient import TestClient

from app.api.v1.schemas.token import TokenRequest, TokenResponse
from tests.factories.user import UserFactory


def test_get_access_token(db_client: TestClient) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory.create(password=password)

    login_request = TokenRequest(
        email=user.email,
        password=password,
    ).model_dump()
    response = db_client.post("/api/v1/token", json=login_request)

    assert response.status_code == status.HTTP_200_OK

    token = TokenResponse.model_validate(response.json())

    assert token.token
    assert token.type == "Bearer"


def test_get_token_unauthorized(db_client: TestClient) -> None:
    login_request = TokenRequest(
        email="johndoe@mail.com",
        password="test-password",  # noqa: S106
    ).model_dump()
    response = db_client.post("/api/v1/token", json=login_request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"
