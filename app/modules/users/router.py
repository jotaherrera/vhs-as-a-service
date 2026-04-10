from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends

from app.database.infrastructure.session import DbSession
from app.modules.auth.dependencies import get_current_active_user
from app.modules.users import repository as user_repo
from app.modules.users import service as user_service
from app.modules.users.model import User
from app.modules.users.schemas import UserCreate, UserList, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def list_users(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserList:
    users = user_service.list_users(db, current_user)
    users_response = [UserResponse.model_validate(user) for user in users]
    return UserList(users=users_response, total=len(users))


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: DbSession, user_request: UserCreate) -> UserResponse:
    user = user_service.create_user(db, user_request)
    return UserResponse.model_validate(user_repo.create(db, user))


@router.get("/me")
async def get_own_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserResponse:
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}")
async def get_user(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int,
) -> UserResponse:
    user = user_service.get_user(db, current_user, user_id)
    return UserResponse.model_validate(user)
