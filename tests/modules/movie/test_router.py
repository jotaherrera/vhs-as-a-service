from fastapi import status
from fastapi.testclient import TestClient

from app.core.security import create_access_token
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
