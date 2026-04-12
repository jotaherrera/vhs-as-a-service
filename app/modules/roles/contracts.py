from app.modules.roles.model import Role
from app.modules.shared.contracts import AbstractRepository


class AbstractRoleRepository(AbstractRepository[Role]):
    def get_by_name(self, name: str) -> Role | None: ...
