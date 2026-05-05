from fastapi import APIRouter, status

from app.modules.auth.dependencies import CurrentActiveUserDep
from app.modules.movie.schemas import (
    MovieCreate,
    MovieResponsePrivate,
    MovieResponsePublic,
)
from app.modules.movie.service import MovieServiceDep

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/")
async def list_movies(
    service: MovieServiceDep,
    current_user: CurrentActiveUserDep,
) -> list[MovieResponsePublic] | list[MovieResponsePrivate]:
    return service.list_movies(current_user)


@router.get("/{movie_id}")
async def get_movie(
    service: MovieServiceDep,
    current_user: CurrentActiveUserDep,
    movie_id: int,
) -> MovieResponsePublic | MovieResponsePrivate:
    return service.get_by_id(current_user, movie_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_movie(
    service: MovieServiceDep,
    current_user: CurrentActiveUserDep,
    request: MovieCreate,
) -> MovieResponsePrivate:
    return service.register(current_user, request)
