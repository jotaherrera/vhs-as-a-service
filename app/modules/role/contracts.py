from app.modules.role.model import Role, RoleName
from app.modules.shared.contracts import AbstractRepository


class AbstractRoleRepository(AbstractRepository[Role]):
    def get_by_name(self, name: RoleName) -> Role | None: ...
