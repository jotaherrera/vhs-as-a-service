from typing import Annotated

from fastapi import Depends

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.role.contracts import AbstractRoleRepository
from app.modules.role.model import Role, RoleName
from app.modules.role.schemas import RoleCreate, RoleList, RoleResponse
from app.modules.user.model import User


def get_role_service(role_repo: AbstractRoleRepository) -> "RoleService":
    return RoleService(role_repo=role_repo)


RoleServiceDep = Annotated["RoleService", Depends(get_role_service)]


class RoleService:
    def __init__(self, role_repo: AbstractRoleRepository) -> None:
        self.role_repo = role_repo

    def list_roles(self, current_user: User) -> RoleList:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        roles = [RoleResponse.model_validate(r) for r in self.role_repo.get_all()]
        return RoleList(roles=roles, total=len(roles))

    def get_by_id(self, current_user: User, role_id: int) -> RoleResponse:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        role = self.role_repo.find_by_id(role_id)
        if role is None:
            raise NotFoundError(detail="Role not found")

        return RoleResponse.model_validate(self.role_repo.find_by_id(role_id))

    def register(self, current_user: User, request: RoleCreate) -> RoleResponse:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        potential_role = self.role_repo.find_by_name(request.name)
        if potential_role is not None:
            raise ConflictError(detail=f"Role with name {request.name} already exists.")

        role = Role(name=request.name, is_active=request.is_active)

        return RoleResponse.model_validate(self.role_repo.create(role))

    def remove(self, current_user: User, role_id: int) -> None:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        role = self.role_repo.find_by_id(role_id)
        if role is None:
            raise NotFoundError(detail="Role not found")

        self.role_repo.delete(role)
