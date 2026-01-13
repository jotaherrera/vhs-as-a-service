from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.operations.user.schemas import UserBase, UserCreateBase


class UserResponse(UserBase):
    id: int
    created_at: datetime
    modified_at: datetime
    is_active: bool
    role_id: int

    class Config:
        from_attributes = True


class UserCreateRequest(UserCreateBase):
    role: str = "user"


class UsersResponse(BaseModel):
    users: list[UserResponse]
    total: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str
