from app.core.exceptions import ConflictError
from app.modules.role.contracts import AbstractRoleRepository
from app.modules.role.model import Role, RoleName


class RoleService:
    def __init__(self, role_repo: AbstractRoleRepository) -> None:
        self.role_repo = role_repo

    def create_role(self, role: Role) -> Role:
        if role.name not in RoleName:
            raise ConflictError(
                detail=f"Invalid role: {role.name}. Must be one of {list(RoleName)}",
            )

        self.role_repo.create(role)
        return role
