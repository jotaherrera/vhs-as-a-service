from fastapi import status
from fastapi.testclient import TestClient

from tests.factories.user import UserFactory


def test_get_access_token(db_client: TestClient) -> None:
    password = "test-password"  # noqa: S105
    user = UserFactory(password=password)

    login_request = {
        "email": user.email,
        "password": password,
    }
    response = db_client.post("/api/v1/token", json=login_request)

    assert response.status_code is status.HTTP_200_OK

    response_json = response.json()
    assert response_json

    assert response_json["token"]
    assert response_json["type"] == "Bearer"
