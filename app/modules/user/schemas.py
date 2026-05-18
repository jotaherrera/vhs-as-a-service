from datetime import datetime
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, ConfigDict, EmailStr

from app.core.fields import PasswordStr
from app.modules.role.model import RoleName
from app.modules.role.schemas import RoleResponse


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    last_name: str
    password: PasswordStr
    role: RoleName


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
    role: RoleResponse
    is_active: bool
    created_at: datetime
    modified_at: datetime


class UserList(BaseModel):
    users: list[UserResponse]
    total: int


class UserFilters(BaseModel):
    is_active: bool | None = None
    role: RoleName | None = None


UserFiltersQuery = Annotated[UserFilters, Query()]
