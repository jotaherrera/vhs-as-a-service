from abc import abstractmethod

from sqlalchemy import Sequence

from app.modules.user.model import User


class AbstractUserRepository:
    @abstractmethod
    def get_all(self, *, is_active: bool | None = None) -> Sequence[User]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> User | None: ...

    @abstractmethod
    def create(self, entity: User) -> User: ...

    @abstractmethod
    def update(self, entity: User) -> User: ...

    @abstractmethod
    def delete(self, entity: User) -> None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...
