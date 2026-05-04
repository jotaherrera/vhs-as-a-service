from abc import ABC, abstractmethod

from sqlalchemy import Sequence

from app.modules.role.model import Role, RoleName


class AbstractRoleRepository(ABC):
    @abstractmethod
    def get_all(self, *, is_active: bool | None = None) -> Sequence[Role]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Role | None: ...

    @abstractmethod
    def create(self, entity: Role) -> Role: ...

    @abstractmethod
    def update(self, entity: Role) -> Role: ...

    @abstractmethod
    def delete(self, entity: Role) -> None: ...

    @abstractmethod
    def find_by_name(self, name: RoleName) -> Role | None: ...
