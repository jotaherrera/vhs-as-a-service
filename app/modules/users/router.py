from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends

from app.modules.auth.dependencies import get_current_active_user
from app.modules.users.model import User
from app.modules.users.schemas import UserCreate, UserList, UserResponse
from app.modules.users.service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users(
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserList:
    return service.list_all_users(current_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    service: Annotated[UserService, Depends(get_user_service)],
    user_request: UserCreate,
) -> UserResponse:
    return service.register_user(user_request)


@router.get("/me")
async def get_own_user(
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    return service.get_user_profile(current_user, current_user.id)  # ???


@router.get("/{user_id}")
async def get_user(
    service: Annotated[UserService, Depends(get_user_service)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int,
) -> UserResponse:
    return service.get_user_profile(current_user, user_id)
