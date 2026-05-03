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
