from typing import Annotated

from fastapi import Depends

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.auth.dependencies import CurrentActiveUserDep
from app.modules.movie.contracts import AbstractMovieRepository
from app.modules.movie.model import Movie, MovieExternalId
from app.modules.movie.repository import MovieRepo
from app.modules.movie.schemas import (
    MovieCreate,
    MovieList,
    MovieResponsePrivate,
    MovieResponsePublic,
    MovieUpdate,
)
from app.modules.role.model import RoleName
from app.modules.user.model import User


def get_movie_service(movie_repo: MovieRepo) -> "MovieService":
    return MovieService(movie_repo=movie_repo)


MovieServiceDep = Annotated["MovieService", Depends(get_movie_service)]


class MovieService:
    def __init__(self, movie_repo: AbstractMovieRepository) -> None:
        self.movie_repo = movie_repo

    def list_movies_for_customer(self) -> list[MovieResponsePublic]:
        movies = self.movie_repo.get_all(is_active=True)
        return [MovieResponsePublic.model_validate(m) for m in movies]

    def list_movies_for_staff(self) -> list[MovieResponsePrivate]:
        movies = self.movie_repo.get_all()
        return [MovieResponsePrivate.model_validate(m) for m in movies]

    def list_movies(self, current_user: User) -> MovieList:
        if current_user.role.name != RoleName.STAFF:
            movies = self.list_movies_for_customer()
            return MovieList(movies=movies, total=len(movies))

        movies = self.list_movies_for_staff()
        return MovieList(movies=movies, total=len(movies))

    def get_by_id(
        self,
        current_user: CurrentActiveUserDep,
        movie_id: int,
    ) -> MovieResponsePublic | MovieResponsePrivate:
        movie = self.movie_repo.find_by_id(movie_id)
        if movie is None:
            raise NotFoundError(detail="Movie not found")

        if current_user.role.name != RoleName.STAFF:
            return MovieResponsePublic.model_validate(movie)
        return MovieResponsePrivate.model_validate(movie)

    def register(self, current_user: User, request: MovieCreate) -> MovieResponsePrivate:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

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

        return MovieResponsePrivate.model_validate(self.movie_repo.create(movie))

    def modify(
        self,
        current_user: User,
        movie_id: int,
        request: MovieUpdate,
    ) -> MovieResponsePrivate:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        movie = self.movie_repo.find_by_id(movie_id)
        if movie is None:
            raise NotFoundError(detail="Movie not found")

        for field, value in request.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        return MovieResponsePrivate.model_validate(self.movie_repo.update(movie))

    def remove(self, current_user: User, movie_id: int) -> None:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        movie = self.movie_repo.find_by_id(movie_id)
        if movie is None:
            raise NotFoundError(detail="Movie not found")

        self.movie_repo.delete(movie)
