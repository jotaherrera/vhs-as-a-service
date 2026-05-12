from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.modules.role.model import RoleName
from app.modules.role.schemas import RoleResponse
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory


def test_list_roles_requires_authentication(db_client: TestClient) -> None:
    response = db_client.get("/api/v1/roles")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_list_roles(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/roles", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_staff_can_list_roles(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    RoleFactory.create(name=RoleName.CUSTOMER)
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/roles", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK


def test_get_role_requires_authentication(db_client: TestClient) -> None:
    response = db_client.get("/api/v1/roles/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_get_role(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/roles/1", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_role_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/roles/999", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_can_get_role(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    role = RoleFactory.create(name=RoleName.CUSTOMER)
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/roles/{role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    result = RoleResponse.model_validate(response.json())
    assert result.id == role.id
    assert result.name == role.name


def test_add_role_requires_authentication(db_client: TestClient) -> None:
    response = db_client.post("/api/v1/roles", json={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_add_role(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.post(
        "/api/v1/roles",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "STAFF", "is_active": True},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_staff_can_add_role(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.post(
        "/api/v1/roles",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "CUSTOMER", "is_active": True},
    )

    assert response.status_code == status.HTTP_201_CREATED
    result = RoleResponse.model_validate(response.json())
    assert result.id is not None


def test_add_role_returns_conflict_on_duplicate_name(db_client: TestClient) -> None:
    RoleFactory.create(name=RoleName.CUSTOMER)
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.post(
        "/api/v1/roles",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "CUSTOMER", "is_active": True},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_role_requires_authentication(db_client: TestClient) -> None:
    response = db_client.delete("/api/v1/roles/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_delete_role(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    role = RoleFactory.create(name=RoleName.STAFF)
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/roles/{role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_role_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.delete(
        "/api/v1/roles/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_can_delete_role(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    role = RoleFactory.create(name=RoleName.CUSTOMER)
    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/roles/{role.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
