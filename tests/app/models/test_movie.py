from tests.factories.movie import MovieFactory


def test_movie_string_repr() -> None:
    movie = MovieFactory.build()

    expected = (
        f"Movie(id={movie.id}, title={movie.title!r}, genre={movie.genre!r}, "
        f"director={movie.director!r}, critic_rating={movie.critic_rating}, "
        f"age_rating={movie.age_rating!r}, release_date={movie.release_date}, "
        f"copies_available={movie.copies_available})"
    )

    assert repr(movie) == expected
