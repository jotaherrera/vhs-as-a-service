from fastapi import APIRouter, status

from app.modules.auth.dependencies import CurrentActiveUserDep
from app.modules.role.schemas import RoleCreate, RoleFiltersQuery, RoleList, RoleResponse
from app.modules.role.service import RoleServiceDep

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/")
async def list_roles(
    service: RoleServiceDep,
    current_user: CurrentActiveUserDep,
    filters: RoleFiltersQuery,
) -> RoleList:
    return service.list_roles(current_user, filters)


@router.get("/{role_id}")
async def get_role(
    service: RoleServiceDep,
    current_user: CurrentActiveUserDep,
    role_id: int,
) -> RoleResponse:
    return service.get_by_id(current_user, role_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_role(
    service: RoleServiceDep,
    current_user: CurrentActiveUserDep,
    request: RoleCreate,
) -> RoleResponse:
    return service.register(current_user, request)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    service: RoleServiceDep,
    current_user: CurrentActiveUserDep,
    role_id: int,
) -> None:
    service.remove(current_user, role_id)
