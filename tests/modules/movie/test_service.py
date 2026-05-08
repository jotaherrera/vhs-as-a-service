import pytest

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.movie.model import MovieExternalId
from app.modules.movie.schemas import (
    ExternalId,
    MovieCreate,
    MovieResponsePrivate,
    MovieResponsePublic,
    MovieUpdate,
)
from app.modules.movie.service import MovieService
from app.modules.role.model import RoleName
from tests.fakes.factories.movie import MovieFactory
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory
from tests.fakes.repository import FakeMovieRepository


def test_list_movies_for_customer_returns_only_active() -> None:
    service = MovieService(
        movie_repo=FakeMovieRepository(
            movies=[
                MovieFactory.build(is_active=True),
                MovieFactory.build(is_active=False),
            ],
        ),
    )
    result = service.list_movies_for_customer()

    assert len(result) == 1


def test_list_movies_for_customer_returns_public_schema() -> None:
    movie = MovieFactory.build(is_active=True)
    service = MovieService(movie_repo=FakeMovieRepository(movies=[movie]))

    result = service.list_movies_for_customer()

    assert len(result) == 1
    item = result[0]
    assert isinstance(item, MovieResponsePublic)
    assert item.id == movie.id
    assert item.title == movie.title
    assert item.description == movie.description
    assert item.genre == movie.genre
    assert item.director == movie.director
    assert item.critic_rating == movie.critic_rating
    assert item.age_rating == movie.age_rating
    assert item.release_date == movie.release_date


def test_list_movies_for_customer_does_not_expose_private_fields() -> None:
    service = MovieService(
        movie_repo=FakeMovieRepository(
            movies=[MovieFactory.build(is_active=True)],
        ),
    )

    result = service.list_movies_for_customer()

    item = result[0]
    assert not hasattr(item, "rental_price")
    assert not hasattr(item, "copies_available")
    assert not hasattr(item, "is_active")
    assert not hasattr(item, "created_at")


def test_list_movies_for_customer_returns_empty_when_none_active() -> None:
    service = MovieService(
        movie_repo=FakeMovieRepository(
            movies=[MovieFactory.build(is_active=False)],
        ),
    )

    result = service.list_movies_for_customer()

    assert result == []


def test_list_movies_for_staff_returns_all_movies() -> None:
    service = MovieService(
        movie_repo=FakeMovieRepository(
            movies=[
                MovieFactory.build(is_active=True),
                MovieFactory.build(is_active=False),
            ],
        ),
    )

    result = service.list_movies_for_staff()

    assert len(result) == 2


def test_list_movies_for_staff_returns_private_schema() -> None:
    movie = MovieFactory.build(is_active=True)
    service = MovieService(movie_repo=FakeMovieRepository(movies=[movie]))

    result = service.list_movies_for_staff()

    assert len(result) == 1
    item = result[0]
    assert isinstance(item, MovieResponsePrivate)
    assert item.id == movie.id
    assert item.title == movie.title
    assert item.rental_price == movie.rental_price
    assert item.copies_available == movie.copies_available
    assert item.is_active == movie.is_active
    assert item.created_at == movie.created_at


def test_list_movies_routes_customer_to_public_listing() -> None:
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = MovieService(
        movie_repo=FakeMovieRepository(
            movies=[
                MovieFactory.build(is_active=True),
                MovieFactory.build(is_active=False),
            ],
        ),
    )

    result = service.list_movies(customer)

    assert len(result) == 1
    assert isinstance(result[0], MovieResponsePublic)


def test_list_movies_routes_staff_to_private_listing() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = MovieService(
        movie_repo=FakeMovieRepository(
            movies=[
                MovieFactory.build(is_active=True),
                MovieFactory.build(is_active=False),
            ],
        ),
    )

    result = service.list_movies(staff)

    assert len(result) == 2
    assert isinstance(result[0], MovieResponsePrivate)


def test_non_staff_cannot_add_movie() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = MovieService(movie_repo=FakeMovieRepository())
    request = MovieCreate(
        title="Inception",
        description="A thief steals corporate secrets through the use of dream-sharing technology.",
        genre="sci_fi",
        director="Christopher Nolan",
        critic_rating=8,
        age_rating="PG-13",
        release_date="2010-07-16",
        rental_price=3.99,
        copies_available=4,
        external_ids=[ExternalId(provider="imdb", external_id="tt1375666")],
    )

    with pytest.raises(ForbiddenError):
        service.register(user, request)


def test_create_movie_persists_correctly() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = MovieService(movie_repo=FakeMovieRepository())
    request = MovieCreate(
        title="The Matrix",
        description="A hacker discovers the truth about reality.",
        genre="sci_fi",
        director="The Wachowskis",
        critic_rating=9,
        age_rating="R",
        release_date="1999-03-31",
        rental_price=3.99,
        copies_available=5,
        external_ids=[ExternalId(provider="imdb", external_id="tt0133093")],
    )

    movie = service.register(user, request)

    assert isinstance(movie, MovieResponsePrivate)
    assert movie.is_active is True
    assert len(movie.external_ids) == 1
    assert movie.external_ids[0].provider == "imdb"
    assert movie.external_ids[0].external_id == "tt0133093"


def test_create_movie_raises_conflict_when_external_id_exists() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    existing = MovieFactory.build(
        external_ids=[MovieExternalId(provider="imdb", external_id="tt0133093")],
    )
    service = MovieService(movie_repo=FakeMovieRepository(movies=[existing]))
    request = MovieCreate(
        title="The Matrix Reloaded",
        description="The sequel.",
        genre="sci_fi",
        director="The Wachowskis",
        critic_rating=7,
        age_rating="R",
        release_date="2003-05-15",
        rental_price=3.99,
        copies_available=3,
        external_ids=[ExternalId(provider="imdb", external_id="tt0133093")],
    )

    with pytest.raises(ConflictError):
        service.register(user, request)


def test_create_movie_conflict_error_includes_provider_and_id() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    existing = MovieFactory.build(
        external_ids=[MovieExternalId(provider="imdb", external_id="tt0133093")],
    )
    service = MovieService(movie_repo=FakeMovieRepository(movies=[existing]))
    request = MovieCreate(
        title="The Matrix Reloaded",
        description="The sequel.",
        genre="sci_fi",
        director="The Wachowskis",
        critic_rating=7,
        age_rating="R",
        release_date="2003-05-15",
        rental_price=3.99,
        copies_available=3,
        external_ids=[ExternalId(provider="imdb", external_id="tt0133093")],
    )

    with pytest.raises(ConflictError) as exc_info:
        service.register(user, request)

    assert "imdb" in exc_info.value.detail.lower()
    assert "tt0133093" in exc_info.value.detail


def test_create_movie_raises_conflict_on_any_matching_external_id() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    existing = MovieFactory.build(
        external_ids=[MovieExternalId(provider="tmdb", external_id="438631")],
    )
    service = MovieService(movie_repo=FakeMovieRepository(movies=[existing]))
    request = MovieCreate(
        title="Dune",
        description="Epic sci-fi.",
        genre="sci_fi",
        director="Denis Villeneuve",
        critic_rating=8,
        age_rating="PG-13",
        release_date="2021-10-22",
        rental_price=4.99,
        copies_available=3,
        external_ids=[
            ExternalId(provider="imdb", external_id="tt1160419"),
            ExternalId(provider="tmdb", external_id="438631"),
        ],
    )

    with pytest.raises(ConflictError):
        service.register(user, request)


def test_non_staff_cannot_modify_movie() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = MovieService(movie_repo=FakeMovieRepository())
    request = MovieUpdate(description="This is a modification attempt by a non-staff user.")

    with pytest.raises(ForbiddenError):
        service.modify(user, movie_id=1, request=request)


def test_modify_movie_nonexistent_id() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = MovieService(movie_repo=FakeMovieRepository())
    request = MovieUpdate(description="Attempting to modify a non-existent movie.")

    with pytest.raises(NotFoundError):
        service.modify(user, movie_id=999, request=request)


def test_modify_movie_successful() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    existing = MovieFactory.build(title="Original Title", description="Original description.")
    service = MovieService(movie_repo=FakeMovieRepository(movies=[existing]))
    request = MovieUpdate(description="Modified description.")

    movie = service.modify(user, movie_id=existing.id, request=request)

    assert isinstance(movie, MovieResponsePrivate)
    assert movie.description == "Modified description."
    assert movie.title == "Original Title"


def test_non_staff_cannot_remove_movie() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = MovieService(movie_repo=FakeMovieRepository())

    with pytest.raises(ForbiddenError):
        service.remove(user, movie_id=1)


def test_remove_movie_nonexistent_id() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = MovieService(movie_repo=FakeMovieRepository())

    with pytest.raises(NotFoundError):
        service.remove(user, movie_id=999)


def test_remove_movie_successful() -> None:
    user = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    existing = MovieFactory.build()
    service = MovieService(movie_repo=FakeMovieRepository(movies=[existing]))

    service.remove(user, movie_id=existing.id)
