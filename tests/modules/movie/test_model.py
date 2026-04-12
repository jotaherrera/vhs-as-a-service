from tests.factories.movie import MovieFactory


def test_movie_string_repr() -> None:
    movie = MovieFactory.build()

    expected = (
        f"<Movie(id={movie.id}, "
        f"title={movie.title!r}, "
        f"genre={movie.genre!r}, "
        f"director={movie.director!r}, "
        f"critic_rating={movie.critic_rating}, "
        f"age_rating={movie.age_rating!r}, "
        f"release_date={movie.release_date}, "
        f"copies_available={movie.copies_available}), "
        f"rental_price={movie.rental_price}, "
        f"is_active={movie.is_active}>"
    )

    assert repr(movie) == expected
