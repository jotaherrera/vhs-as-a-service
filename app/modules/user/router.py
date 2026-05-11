from fastapi import APIRouter, status

from app.modules.auth.dependencies import CurrentActiveUserDep
from app.modules.user.schemas import UserCreate, UserList, UserResponse, UserUpdate
from app.modules.user.service import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users(service: UserServiceDep, current_user: CurrentActiveUserDep) -> UserList:
    return service.list_all_users(current_user)


@router.get("/me")
async def get_own_user(current_user: CurrentActiveUserDep) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}")
async def get_user(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    user_id: int,
) -> UserResponse:
    return service.get_user_profile(current_user, user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(service: UserServiceDep, request: UserCreate) -> UserResponse:
    return service.register_user(request)


@router.patch("/{user_id}")
async def update_user(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    user_id: int,
    request: UserUpdate,
) -> UserResponse:
    return service.modify(current_user, user_id, request)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    service: UserServiceDep,
    current_user: CurrentActiveUserDep,
    user_id: int,
) -> None:
    return service.remove(current_user, user_id)
