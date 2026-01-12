from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends

from app.database.session import DbSession
from app.dependencies.auth import get_current_active_user
from app.exceptions import ForbidenError, NotFoundError
from app.models.user import User
from app.operations import role as crud_role
from app.operations import user as crud_user
from app.schemas.user import UserCreateInternal, UserCreatePublic, UserResponse, UsersResponse

router = APIRouter()


@router.get("/users")
async def list_users(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UsersResponse:
    if current_user.role.name != "admin":
        raise ForbidenError(detail="Not authorized to perform this action")

    users = crud_user.get_all_users(db)
    users_response = [UserResponse.model_validate(user) for user in users]

    return UsersResponse(users=users_response, total=len(users))


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(db: DbSession, user_request: UserCreatePublic) -> UserResponse:
    db_role = crud_role.get_role_by_name(db, user_request.role)
    if db_role is None:
        raise NotFoundError(detail="Role not found")

    user = UserCreateInternal(**user_request.model_dump(exclude={"role"}), role_id=db_role.id)

    return UserResponse.model_validate(crud_user.create_user(db, user))
