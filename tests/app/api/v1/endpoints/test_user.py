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
    user_response = UsersResponse.model_validate(response.json())

    returned_ids = {u.id for u in user_response.users}
    assert returned_ids == {admin_user.id, normal_user.id}


def test_list_users_normal_user(db_client: TestClient) -> None:
    user = UserFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not authorized to perform this action"


def test_create_user(db_client: TestClient) -> None:
    role = RoleFactory.create(name="user")

    request = UserCreateRequest(
        email="johndoe@mail.com",
        name="John",
        last_name="Doe",
        password="test-password",  # noqa: S106
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
    assert user.is_active
    assert user.role_id == role.id


def test_create_user_role_not_found(db_client: TestClient) -> None:
    request = UserCreateRequest(
        email="johndoe@mail.com",
        name="John",
        last_name="Doe",
        password="test-password",  # noqa: S106
        role="not-a-role",
    ).model_dump()
    response = db_client.post("/api/v1/users", json=request)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Role not found"


def test_get_own_user(db_client: TestClient) -> None:
    user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    user_response = UserResponse.model_validate(response.json())

    assert user_response.id == user.id
    assert user_response.email == user.email
    assert user_response.name == user.name
    assert user_response.last_name == user.last_name
    assert user_response.is_active == user.is_active
    assert user_response.role_id == user.role_id

    assert user_response.created_at is not None
    assert user_response.modified_at is not None
    assert user_response.modified_at is not None


def test_get_user_by_id_normal_user(db_client: TestClient) -> None:
    user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    user_response = UserResponse.model_validate(response.json())

    assert user_response.id == user.id
    assert user_response.email == user.email
    assert user_response.name == user.name
    assert user_response.last_name == user.last_name
    assert user_response.is_active == user.is_active
    assert user_response.role_id == user.role_id

    assert user_response.created_at is not None
    assert user_response.modified_at is not None
    assert user_response.modified_at is not None


def test_get_user_by_id_admin_user(db_client: TestClient) -> None:
    role = RoleFactory.create(name="admin")

    user_admin = UserFactory.create(role=role)
    user = UserFactory.create()

    token = create_access_token({"sub": str(user_admin.id)})

    response = db_client.get(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    user_response = UserResponse.model_validate(response.json())

    assert user_response.id == user.id
    assert user_response.email == user.email
    assert user_response.name == user.name
    assert user_response.last_name == user.last_name
    assert user_response.is_active == user.is_active
    assert user_response.role_id == user.role_id

    assert user_response.created_at is not None
    assert user_response.modified_at is not None
    assert user_response.modified_at is not None


def test_get_user_by_id_normal_user_not_self_id(db_client: TestClient) -> None:
    user = UserFactory.create()
    another_user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/users/{another_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Not authorized to perform this action"


def test_get_user_by_id_admin_user_not_found(db_client: TestClient) -> None:
    role = RoleFactory.create(name="admin")

    user_admin = UserFactory.create(role=role)

    token = create_access_token({"sub": str(user_admin.id)})

    response = db_client.get("/api/v1/users/123", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
