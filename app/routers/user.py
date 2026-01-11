from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

from app.database.session import DbSession
from app.dependencies.auth import get_current_active_user
from app.exceptions import ForbidenError
from app.models.user import User
from app.operations import user as crud_user
from app.schemas.user import UserResponse

router = APIRouter()


class AllUsersResponse(BaseModel):
    users: list[UserResponse]
    total: int


@router.get("/users")
async def get_all_users(
    db: DbSession,
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> AllUsersResponse:
    if current_user.role.name != "admin":
        raise ForbidenError(detail="Not authorized to perform this action")

    users = crud_user.get_all_users(db)
    users_response = [UserResponse.model_validate(user) for user in users]

    return AllUsersResponse(users=users_response, total=len(users))
