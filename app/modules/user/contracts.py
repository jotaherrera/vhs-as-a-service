from abc import ABC, abstractmethod

from sqlalchemy import Sequence

from app.modules.user.model import User
from app.modules.user.schemas import UserFilters


class AbstractUserRepository(ABC):
    @abstractmethod
    def get_all(self, filters: UserFilters) -> Sequence[User]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> User | None: ...

    @abstractmethod
    def create(self, entity: User) -> User: ...

    @abstractmethod
    def update(self, entity: User) -> User: ...

    @abstractmethod
    def delete(self, entity: User) -> None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> User | None: ...
