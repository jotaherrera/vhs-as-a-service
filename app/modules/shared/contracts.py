from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


class AbstractRepository[T](ABC):
    @abstractmethod
    def get_all(self, *, is_active: bool | None = None) -> Sequence[T]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None: ...

    @abstractmethod
    def create(self, entity: T) -> T: ...
