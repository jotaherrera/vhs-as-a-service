from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.modules.movie.model import MovieExternalId
from app.modules.movie.schemas import MovieResponsePrivate, MovieResponsePublic
from app.modules.role.model import RoleName
from tests.fakes.factories.movie import MovieFactory
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory


def test_list_movies_requires_authentication(db_client: TestClient) -> None:
    response = db_client.get("/api/v1/movies")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_staff_can_list_movies(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    MovieFactory.create()
    MovieFactory.create()

    token = create_access_token(data={"sub": str(user.id)})
    response = db_client.get("/api/v1/movies", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    movies = [MovieResponsePrivate.model_validate(item) for item in response.json()]
    assert len(movies) == 2


def test_customer_can_list_movies(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))

    MovieFactory.create()
    MovieFactory.create()

    token = create_access_token(data={"sub": str(user.id)})
    response = db_client.get("/api/v1/movies", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_200_OK
    movies = [MovieResponsePublic.model_validate(item) for item in response.json()]
    assert len(movies) == 2


def test_get_movie_requires_authentication(db_client: TestClient) -> None:
    response = db_client.get("/api/v1/movies/123")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_movie_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})
    response = db_client.get("/api/v1/movies/456", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_staff_can_get_movie(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})
    movie = MovieFactory.create()

    response = db_client.get(
        f"/api/v1/movies/{movie.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    movie = MovieResponsePrivate.model_validate(response.json())
    assert movie.id == movie.id


def test_customer_can_get_movie(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    token = create_access_token(data={"sub": str(user.id)})
    movie = MovieFactory.create()

    response = db_client.get(
        f"/api/v1/movies/{movie.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    movie = MovieResponsePublic.model_validate(response.json())
    assert movie.id == movie.id


def test_add_movie_requires_authentication(db_client: TestClient) -> None:
    response = db_client.post("/api/v1/movies", json={})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_non_staff_cannot_add_movie(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    token = create_access_token(data={"sub": str(user.id)})

    request = {
        "title": "Test Movie",
        "description": "Test",
        "genre": "Action",
        "director": "Test Director",
        "critic_rating": 7,
        "age_rating": "PG",
        "release_date": "2024-01-01",
        "rental_price": 3.99,
        "copies_available": 5,
        "external_ids": [{"provider": "imdb", "external_id": "tt1234567"}],
    }

    response = db_client.post(
        "/api/v1/movies",
        headers={"Authorization": f"Bearer {token}"},
        json=request,
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_staff_can_add_movie(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})

    request = {
        "title": "Test Movie",
        "description": "Test",
        "genre": "Action",
        "director": "Test Director",
        "critic_rating": 7,
        "age_rating": "PG",
        "release_date": "2024-01-01",
        "rental_price": 3.99,
        "copies_available": 5,
        "external_ids": [{"provider": "imdb", "external_id": "tt1234567"}],
    }

    response = db_client.post(
        "/api/v1/movies",
        headers={"Authorization": f"Bearer {token}"},
        json=request,
    )

    assert response.status_code == status.HTTP_201_CREATED
    movie = MovieResponsePrivate.model_validate(response.json())
    assert movie.id is not None


def test_add_movie_returns_conflict_on_duplicate_external_id(db_client: TestClient) -> None:
    MovieFactory.create(external_ids=[MovieExternalId(provider="imdb", external_id="tt1234567")])
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    token = create_access_token(data={"sub": str(user.id)})

    request = {
        "title": "Another Movie",
        "description": "Test",
        "genre": "Action",
        "director": "Test Director",
        "critic_rating": 7,
        "age_rating": "PG",
        "release_date": "2024-01-01",
        "rental_price": 3.99,
        "copies_available": 5,
        "external_ids": [{"provider": "imdb", "external_id": "tt1234567"}],
    }

    response = db_client.post(
        "/api/v1/movies",
        headers={"Authorization": f"Bearer {token}"},
        json=request,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_movie_unauthenticated(db_client: TestClient) -> None:
    response = db_client.patch("/api/v1/movies/1", json={})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_movie_customer_forbidden(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    movie = MovieFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.patch(
        f"/api/v1/movies/{movie.id}",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_movie_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token({"sub": str(user.id)})

    response = db_client.patch(
        "/api/v1/movies/999",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_movie_staff_success(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    movie = MovieFactory.create(title="Original Title")

    token = create_access_token({"sub": str(user.id)})

    response = db_client.patch(
        f"/api/v1/movies/{movie.id}",
        json={"description": "New description."},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    movie_response = MovieResponsePrivate.model_validate(response.json())
    assert movie_response.description == "New description."
    assert movie_response.title == "Original Title"


def test_delete_movie_unauthenticated(db_client: TestClient) -> None:
    response = db_client.delete("/api/v1/movies/1")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_movie_customer_forbidden(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.CUSTOMER))
    movie = MovieFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/movies/{movie.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_movie_not_found(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))

    token = create_access_token({"sub": str(user.id)})

    response = db_client.delete(
        "/api/v1/movies/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_movie_staff_success(db_client: TestClient) -> None:
    user = UserFactory.create(role=RoleFactory.create(name=RoleName.STAFF))
    movie = MovieFactory.create()

    token = create_access_token({"sub": str(user.id)})

    response = db_client.delete(
        f"/api/v1/movies/{movie.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
