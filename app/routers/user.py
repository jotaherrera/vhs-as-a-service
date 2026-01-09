from fastapi import APIRouter
from pydantic import BaseModel

from app.database.session import DbSession
from app.operations import user as crud_user
from app.schemas.user import UserResponse

router = APIRouter()


class AllUsersResponse(BaseModel):
    users: list[UserResponse]
    total: int


@router.get("/users")
async def get_all_users(db: DbSession) -> AllUsersResponse:
    users = crud_user.get_all_users(db)
    return AllUsersResponse(
        users=users,
        total=len(users),
    )
