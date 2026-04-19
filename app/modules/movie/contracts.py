from abc import abstractmethod

from sqlalchemy import Sequence

from app.modules.movie.model import Movie
from app.modules.movie.schemas import ExternalId


class AbstractMovieRepository:
    @abstractmethod
    def get_all(self, *, is_active: bool | None = None) -> Sequence[Movie]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Movie | None: ...

    @abstractmethod
    def create(self, entity: Movie) -> Movie: ...

    @abstractmethod
    def update(self, entity: Movie) -> Movie: ...

    @abstractmethod
    def delete(self, entity: Movie) -> None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Sequence[Movie]: ...

    @abstractmethod
    def find_by_external_id(self, external_id: ExternalId) -> Movie | None: ...
