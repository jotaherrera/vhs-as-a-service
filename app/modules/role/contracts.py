from abc import abstractmethod

from sqlalchemy import Sequence

from app.modules.role.model import Role, RoleName


class AbstractRoleRepository:
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
    def get_by_name(self, name: RoleName) -> Role | None: ...
