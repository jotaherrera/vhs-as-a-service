from fastapi import APIRouter, status

from app.modules.auth.dependencies import CurrentActiveUserDep
from app.modules.user.schemas import UserCreate, UserList, UserResponse
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
