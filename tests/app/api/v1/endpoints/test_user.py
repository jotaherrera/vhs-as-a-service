from fastapi import status
from fastapi.testclient import TestClient

from app.api.v1.schemas.user import UserCreateRequest, UserResponse, UsersResponse
from app.core.security import create_access_token
from tests.factories.role import RoleFactory
from tests.factories.user import UserFactory


def test_list_users_admin(db_client: TestClient) -> None:
    role = RoleFactory.create(name="admin")
    admin_user = UserFactory.create(role=role)
    normal_user = UserFactory.create()

    token = create_access_token(data={"sub": str(admin_user.id)})

    response = db_client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    parsed = UsersResponse(**response.json())

    returned_ids = {u.id for u in parsed.users}
    assert returned_ids == {admin_user.id, normal_user.id}


def test_list_users(db_client: TestClient) -> None:
    normal_user = UserFactory.create()

    token = create_access_token(data={"sub": str(normal_user.id)})

    response = db_client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user(db_client: TestClient) -> None:
    role = RoleFactory.create(name="user")
    password = "test-password"  # noqa: S105

    request = UserCreateRequest(
        email="jhondoe@mail.com",
        name="Jhon",
        last_name="Doe",
        password=password,
        role=role.name,
    ).model_dump()

    response = db_client.post("/api/v1/users", json=request)

    assert response.status_code == status.HTTP_201_CREATED

    user = UserResponse.model_validate(response.json())

    assert user.email == request["email"]
    assert user.name == request["name"]
    assert user.last_name == request["last_name"]

    assert user.id is not None
    assert user.created_at is not None
    assert user.modified_at is not None
    assert user.is_active is True
    assert user.role_id == role.id
