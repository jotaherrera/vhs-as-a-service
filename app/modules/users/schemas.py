from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.fields import PasswordStr
from app.modules.roles.model import Roles


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    last_name: str
    password: PasswordStr
    role: Roles


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
    last_name: str | None = None
    password: PasswordStr | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    last_name: str
    role_id: int
    is_active: bool
    created_at: datetime
    modified_at: datetime


class UserList(BaseModel):
    users: list[UserResponse]
    total: int
