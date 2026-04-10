from fastapi import status
from fastapi.testclient import TestClient

from app.modules.auth.schemas import TokenResponse
from tests.factories.user import UserFactory


def test_get_access_token(db_client: TestClient) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory.create(password=password)

    login_request = {
        "email": user.email,
        "password": password,
    }
    response = db_client.post("/api/v1/token", json=login_request)

    assert response.status_code == status.HTTP_200_OK

    token = TokenResponse.model_validate(response.json())

    assert token.token
    assert token.type == "Bearer"


def test_get_token_unauthorized(db_client: TestClient) -> None:
    login_request = {
        "email": "johndoe@mail.com",
        "password": "test-password",
    }
    response = db_client.post("/api/v1/token", json=login_request)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"
