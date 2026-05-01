from app.core.exceptions import ConflictError
from app.modules.role.contracts import AbstractRoleRepository
from app.modules.role.model import Role


class RoleService:
    def __init__(self, role_repo: AbstractRoleRepository) -> None:
        self.role_repo = role_repo

    def create_role(self, role: Role) -> Role:
        potential_role = self.role_repo.find_by_name(role.name)
        if potential_role is not None:
            raise ConflictError(detail=f"Role with name {role.name} already exists.")

        self.role_repo.create(role)
        return role
