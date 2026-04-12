from abc import abstractmethod

from sqlalchemy import Sequence

from app.modules.movies.model import Movie
from app.modules.movies.schemas import ExternalId
from app.modules.shared.contracts import AbstractRepository


class AbstractMovieRepository(AbstractRepository):
    @abstractmethod
    def get_by_name(self, name: str) -> Sequence[Movie]: ...

    @abstractmethod
    def find_by_external_id(self, external_id: ExternalId) -> Movie | None: ...
