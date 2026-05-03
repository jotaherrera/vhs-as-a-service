from fastapi import APIRouter

from app.modules.auth.dependencies import CurrentUserDep
from app.modules.movie.schemas import MovieResponsePrivate, MovieResponsePublic
from app.modules.movie.service import MovieServiceDep

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/")
async def list_movies(
    service: MovieServiceDep,
    current_user: CurrentUserDep,
) -> list[MovieResponsePublic] | list[MovieResponsePrivate]:
    return service.list_movies(current_user)


@router.get("/{movie_id}")
async def get_movie(
    service: MovieServiceDep,
    current_user: CurrentUserDep,
    movie_id: int,
) -> MovieResponsePublic | MovieResponsePrivate:
    return service.get_by_id(current_user, movie_id)
