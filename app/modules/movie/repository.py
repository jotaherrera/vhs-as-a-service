from typing import Annotated

from fastapi import Depends
from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session

from app.database.infrastructure.session import DbSession
from app.modules.movie.contracts import AbstractMovieRepository
from app.modules.movie.model import Movie, MovieExternalId
from app.modules.movie.schemas import ExternalId


def get_movie_repository(db: DbSession) -> AbstractMovieRepository:
    return MovieRepository(db)


MovieRepo = Annotated[AbstractMovieRepository, Depends(get_movie_repository)]


class MovieRepository(AbstractMovieRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, *, is_active: bool | None = None) -> Sequence[Movie]:
        stmt = select(Movie)

        if is_active is not None:
            stmt = stmt.where(Movie.is_active.is_(is_active))

        return self.db.scalars(stmt).all()

    def find_by_id(self, entity_id: int) -> Movie | None:
        stmt = select(Movie).where(Movie.id == entity_id)
        return self.db.scalar(stmt)

    def create(self, entity: Movie) -> Movie:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Movie) -> Movie:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: Movie) -> None:
        entity.is_active = False
        self.db.commit()

    def get_by_name(self, name: str) -> Sequence[Movie]:
        stmt = select(Movie).where(Movie.title.ilike(f"%{name}%"))
        return self.db.scalars(stmt).all()

    def find_by_external_id(self, external_id: ExternalId) -> Movie | None:
        stmt = (
            select(Movie)
            .join(Movie.external_ids)
            .where(
                MovieExternalId.provider == external_id.provider,
                MovieExternalId.external_id == external_id.external_id,
            )
        )
        return self.db.scalar(stmt)
