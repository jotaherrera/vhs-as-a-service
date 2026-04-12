import pytest
from sqlalchemy.orm import Session

from app.modules.movie.model import Movie, MovieExternalId
from app.modules.movie.repository import MovieRepository
from app.modules.movie.schemas import ExternalId
from tests.factories.movie import MovieFactory


@pytest.fixture
def movie_repo(db_session: Session) -> MovieRepository:
    return MovieRepository(db_session)


def test_find_by_id_returns_movie_when_exists(movie_repo: MovieRepository) -> None:
    movie = MovieFactory.create()

    result = movie_repo.find_by_id(movie.id)

    assert result is not None
    assert result.id == movie.id
    assert result.title == movie.title


def test_find_by_id_returns_none_when_not_found(movie_repo: MovieRepository) -> None:
    result = movie_repo.find_by_id(999_999)

    assert result is None


def test_get_all_returns_all_movies_without_filter(movie_repo: MovieRepository) -> None:
    MovieFactory.create(is_active=True)
    MovieFactory.create(is_active=False)

    result = movie_repo.get_all()

    assert len(result) == 2


def test_get_all_with_is_active_true_returns_only_active(movie_repo: MovieRepository) -> None:
    active = MovieFactory.create(is_active=True)
    MovieFactory.create(is_active=False)

    result = movie_repo.get_all(is_active=True)

    assert len(result) == 1
    assert result[0].id == active.id
    assert result[0].is_active is True


def test_get_all_with_is_active_false_returns_only_inactive(
    movie_repo: MovieRepository,
) -> None:
    MovieFactory.create(is_active=True)
    inactive = MovieFactory.create(is_active=False)

    result = movie_repo.get_all(is_active=False)

    assert len(result) == 1
    assert result[0].id == inactive.id
    assert result[0].is_active is False


def test_create_persists_movie_and_returns_it(
    movie_repo: MovieRepository,
    db_session: Session,
) -> None:
    movie = MovieFactory.build()

    result = movie_repo.create(movie)

    assert result.id is not None
    assert db_session.get(Movie, result.id) is not None


def test_get_by_name_returns_partial_matches(movie_repo: MovieRepository) -> None:
    MovieFactory.create(title="The Matrix Reloaded")
    MovieFactory.create(title="The Matrix Revolutions")
    MovieFactory.create(title="Inception")

    result = movie_repo.get_by_name("matrix")

    assert len(result) == 2
    assert all("matrix" in m.title.lower() for m in result)


def test_get_by_name_is_case_insensitive(movie_repo: MovieRepository) -> None:
    MovieFactory.create(title="Blade Runner 2049")

    result = movie_repo.get_by_name("BLADE")

    assert len(result) == 1
    assert result[0].title == "Blade Runner 2049"


def test_get_by_name_returns_empty_list_when_no_match(movie_repo: MovieRepository) -> None:
    MovieFactory.create(title="Inception")

    result = movie_repo.get_by_name("matrix")

    assert result == []


def test_find_by_external_id_returns_movie_when_match(
    movie_repo: MovieRepository,
    db_session: Session,
) -> None:
    movie = MovieFactory.create()
    ext = MovieExternalId(movie_id=movie.id, provider="tmdb", external_id="tt1234567")
    db_session.add(ext)
    db_session.flush()

    query = ExternalId(provider="tmdb", external_id="tt1234567")

    result = movie_repo.find_by_external_id(query)

    assert result is not None
    assert result.id == movie.id


def test_find_by_external_id_returns_none_when_no_match(movie_repo: MovieRepository) -> None:
    query = ExternalId(provider="tmdb", external_id="does-not-exist")

    result = movie_repo.find_by_external_id(query)

    assert result is None


def test_find_by_external_id_does_not_match_different_provider(
    movie_repo: MovieRepository,
    db_session: Session,
) -> None:
    movie = MovieFactory.create()
    ext = MovieExternalId(movie_id=movie.id, provider="imdb", external_id="tt9999999")
    db_session.add(ext)
    db_session.flush()

    query = ExternalId(provider="tmdb", external_id="tt9999999")

    result = movie_repo.find_by_external_id(query)

    assert result is None
