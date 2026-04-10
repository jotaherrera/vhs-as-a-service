from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.fields import PasswordStr
from app.models.role import Roles


class UserBase(BaseModel):
    email: EmailStr
    name: str
    last_name: str


class UserCreateBase(UserBase):
    password: PasswordStr


class UserCreate(UserCreateBase):
    role_id: int
    is_active: bool = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: PasswordStr | None = None
    name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    modified_at: datetime
    is_active: bool
    role_id: int

    model_config = ConfigDict(from_attributes=True)


class UserCreateRequest(UserCreateBase):
    role: str = Roles.CUSTOMER


class UsersResponse(BaseModel):
    users: list[UserResponse]
    total: int


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr
