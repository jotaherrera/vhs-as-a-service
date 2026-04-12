from app.core.exceptions import ConflictError
from app.modules.movies.contracts import AbstractMovieRepository
from app.modules.movies.model import Movie, MovieExternalId
from app.modules.movies.schemas import (
    MovieCreate,
    MovieResponsePrivate,
    MovieResponsePublic,
)
from app.modules.roles.model import Roles
from app.modules.users.model import User


class MovieService:
    def __init__(self, movie_repo: AbstractMovieRepository) -> None:
        self.movie_repo = movie_repo

    def list_movies_for_customer(self) -> list[MovieResponsePublic]:
        movies = self.movie_repo.get_all(is_active=True)
        return [MovieResponsePublic.model_validate(m) for m in movies]

    def list_movies_for_staff(self) -> list[MovieResponsePrivate]:
        movies = self.movie_repo.get_all()
        return [MovieResponsePrivate.model_validate(m) for m in movies]

    def list_movies(
        self,
        current_user: User,
    ) -> list[MovieResponsePublic] | list[MovieResponsePrivate]:
        if current_user.role.name != Roles.STAFF:
            return self.list_movies_for_customer()

        return self.list_movies_for_staff()

    def create_movie(self, request: MovieCreate) -> Movie:
        for ext in request.external_ids:
            existing = self.movie_repo.find_by_external_id(ext)
            if existing:
                raise ConflictError(
                    detail=f"Movie already exists with {ext.provider} ID {ext.external_id}",
                )

        movie = Movie(
            title=request.title,
            description=request.description,
            genre=request.genre,
            director=request.director,
            critic_rating=request.critic_rating,
            age_rating=request.age_rating,
            release_date=request.release_date,
            rental_price=request.rental_price,
            copies_available=request.copies_available,
            is_active=True,
            external_ids=[
                MovieExternalId(
                    provider=ext.provider,
                    external_id=ext.external_id,
                )
                for ext in request.external_ids
            ],
        )

        return self.movie_repo.create(movie)
