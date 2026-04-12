from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import Sequence

T = TypeVar("T")


class AbstractRepository[T](ABC):
    @abstractmethod
    def get_all(self, *, is_active: bool | None = None) -> Sequence[T]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None: ...

    @abstractmethod
    def create(self, entity: T) -> T: ...
