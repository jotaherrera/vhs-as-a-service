from datetime import UTC, datetime, timedelta

from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.modules.role.model import RoleName
from tests.fakes.factories.movie import MovieFactory
from tests.fakes.factories.rental import RentalFactory
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory


def test_list_rentals_requires_authentication(db_client: TestClient) -> None:
    response = db_client.get("/api/v1/rentals")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_staff_can_list_rentals(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    RentalFactory.create()
    RentalFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/rentals", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK


def test_customer_cannot_list_rentals(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/rentals", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_rental_requires_authentication(db_client: TestClient) -> None:
    response = db_client.get("/api/v1/rentals/123")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_rental_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get("/api/v1/rentals/999", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_can_get_any_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    rental = RentalFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/rentals/{rental.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK


def test_customer_can_get_own_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    rental = RentalFactory.create(customer=user)

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/rentals/{rental.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK


def test_customer_cannot_get_other_customer_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    rental = RentalFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.get(
        f"/api/v1/rentals/{rental.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_register_rental_requires_authentication(db_client: TestClient) -> None:
    response = db_client.post("/api/v1/rentals", json={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_register_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.post(
        "/api/v1/rentals",
        headers={"Authorization": f"Bearer {token}"},
        json={"customer_id": 1, "staff_id": 2, "movie_id": 3},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_staff_can_register_rental(db_client: TestClient) -> None:
    staff = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    customer = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    movie = MovieFactory.create(copies_available=1)

    token = create_access_token(data={"sub": str(staff.id)})

    response = db_client.post(
        "/api/v1/rentals",
        headers={"Authorization": f"Bearer {token}"},
        json={"customer_id": customer.id, "staff_id": staff.id, "movie_id": movie.id},
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_register_rental_customer_not_found(db_client: TestClient) -> None:
    staff = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    movie = MovieFactory.create(copies_available=1)

    token = create_access_token(data={"sub": str(staff.id)})

    response = db_client.post(
        "/api/v1/rentals",
        headers={"Authorization": f"Bearer {token}"},
        json={"customer_id": 999, "staff_id": staff.id, "movie_id": movie.id},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_register_rental_movie_not_found(db_client: TestClient) -> None:
    staff = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    customer = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))

    token = create_access_token(data={"sub": str(staff.id)})

    response = db_client.post(
        "/api/v1/rentals",
        headers={"Authorization": f"Bearer {token}"},
        json={"customer_id": customer.id, "staff_id": staff.id, "movie_id": 999},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_register_rental_movie_unavailable(db_client: TestClient) -> None:
    staff = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    customer = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    movie = MovieFactory.create(copies_available=0)

    token = create_access_token(data={"sub": str(staff.id)})

    response = db_client.post(
        "/api/v1/rentals",
        headers={"Authorization": f"Bearer {token}"},
        json={"customer_id": customer.id, "staff_id": staff.id, "movie_id": movie.id},
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_rental_requires_authentication(db_client: TestClient) -> None:
    response = db_client.patch("/api/v1/rentals/1", json={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_update_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    rental = RentalFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.patch(
        f"/api/v1/rentals/{rental.id}",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_rental_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.patch(
        "/api/v1/rentals/999",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_can_update_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    rental = RentalFactory.create()
    new_return_date = (datetime.now(UTC) + timedelta(days=14)).isoformat()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.patch(
        f"/api/v1/rentals/{rental.id}",
        json={"expected_return_at": new_return_date},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK


def test_delete_rental_requires_authentication(db_client: TestClient) -> None:
    response = db_client.delete("/api/v1/rentals/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_customer_cannot_delete_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    rental = RentalFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/rentals/{rental.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_rental_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.delete(
        "/api/v1/rentals/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_can_delete_rental(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    rental = RentalFactory.create()

    token = create_access_token(data={"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/rentals/{rental.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
