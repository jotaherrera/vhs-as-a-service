from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.modules.role.model import RoleName
from app.modules.user.schemas import UserList, UserResponse
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory


def test_list_users_staff(db_client: TestClient) -> None:
    staff_user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    customer_user = UserFactory.create()

    token = create_access_token(data={"sub": str(staff_user.id)})

    response = db_client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    user_response = UserList.model_validate(response.json())

    returned_ids = {u.id for u in user_response.users}
    assert returned_ids == {staff_user.id, customer_user.id}


def test_list_users_customer(db_client: TestClient) -> None:
    user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.get("/api/v1/users", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user(db_client: TestClient) -> None:
    role = RoleFactory.create(name=RoleName.CUSTOMER)

    request = {
        "email": "johndoe@mail.com",
        "name": "John",
        "last_name": "Doe",
        "password": "test-password",
        "role": role.name,
    }
    response = db_client.post("/api/v1/users", json=request)

    assert response.status_code == status.HTTP_201_CREATED
    user = UserResponse.model_validate(response.json())
    assert user.id is not None


def test_create_user_email_already_exists(db_client: TestClient) -> None:
    role = RoleFactory.create(name=RoleName.CUSTOMER)
    user = UserFactory.create(email="johndoe@mail.com")

    request = {
        "email": user.email,
        "name": user.name,
        "last_name": user.last_name,
        "password": "test-password",
        "role": role.name,
    }
    response = db_client.post("/api/v1/users", json=request)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_user_role_not_found(db_client: TestClient) -> None:
    request = {
        "email": "johndoe@mail.com",
        "name": "John",
        "last_name": "Doe",
        "password": "test-password",
        "role": "not-a-role",
    }
    response = db_client.post("/api/v1/users", json=request)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_own_user(db_client: TestClient) -> None:
    user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    user_response = UserResponse.model_validate(response.json())
    assert user_response.id == user.id


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


def test_get_user_by_id_admin_user(db_client: TestClient) -> None:
    role = RoleFactory.create(name=RoleName.STAFF)
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


def test_get_user_by_id_normal_user_not_self_id(db_client: TestClient) -> None:
    user = UserFactory.create()
    another_user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/users/{another_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_by_id_admin_user_not_found(db_client: TestClient) -> None:
    role = RoleFactory.create(name=RoleName.STAFF)
    user_admin = UserFactory.create(role=role)

    token = create_access_token({"sub": str(user_admin.id)})

    response = db_client.get("/api/v1/users/123", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_requires_authentication(db_client: TestClient) -> None:
    response = db_client.patch("/api/v1/users/1", json={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user_customer_cannot_update_other(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    another_user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.patch(
        f"/api/v1/users/{another_user.id}",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_user_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token({"sub": str(user.id)})

    response = db_client.patch(
        "/api/v1/users/999",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_customer_can_update_own_profile(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))

    token = create_access_token({"sub": str(user.id)})

    response = db_client.patch(
        f"/api/v1/users/{user.id}",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    user_response = UserResponse.model_validate(response.json())
    assert user_response.id == user.id
    assert user_response.name == "New Name"


def test_update_user_staff_can_update_any_user(db_client: TestClient) -> None:
    staff = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    user = UserFactory.create()

    token = create_access_token({"sub": str(staff.id)})

    response = db_client.patch(
        f"/api/v1/users/{user.id}",
        json={"name": "New Name"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    user_response = UserResponse.model_validate(response.json())
    assert user_response.id == user.id
    assert user_response.name == "New Name"


def test_delete_user_requires_authentication(db_client: TestClient) -> None:
    response = db_client.delete("/api/v1/users/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_user_customer_forbidden(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    another_user = UserFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/users/{another_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_user_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token({"sub": str(user.id)})

    response = db_client.delete(
        "/api/v1/users/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_staff_success(db_client: TestClient) -> None:
    staff = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    user = UserFactory.create()

    token = create_access_token({"sub": str(staff.id)})

    response = db_client.delete(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
