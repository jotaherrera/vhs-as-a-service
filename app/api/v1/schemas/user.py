from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.fields import PasswordStr
from app.operations.user.schemas import UserBase, UserCreateBase


class UserResponse(UserBase):
    id: int
    created_at: datetime
    modified_at: datetime
    is_active: bool
    role_id: int

    model_config = ConfigDict(from_attributes=True)


class UserCreateRequest(UserCreateBase):
    role: str = "user"


class UsersResponse(BaseModel):
    users: list[UserResponse]
    total: int


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr
