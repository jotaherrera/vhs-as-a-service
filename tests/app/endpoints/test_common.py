from fastapi import status
from fastapi.testclient import TestClient

from app.config import get_settings


def test_info(simple_client: TestClient) -> None:
    response = simple_client.get("/info")

    assert response.status_code is status.HTTP_200_OK
    assert response.json() == {
        "app_name": get_settings().app.name,
        "app_version": get_settings().app.version,
        "app_debug": get_settings().app.debug,
    }


def test_health(simple_client: TestClient) -> None:
    response = simple_client.get("/health")

    assert response.status_code is status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
