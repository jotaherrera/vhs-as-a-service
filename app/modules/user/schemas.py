from datetime import datetime
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, ConfigDict, EmailStr, computed_field

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
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    users: list[UserResponse]

    @computed_field
    @property
    def total(self) -> int:
        return len(self.users)


class UserQueryParams(BaseModel):
    role: RoleName | None = None


class UserFilters(UserQueryParams):
    is_active: bool | None = None


UserQueryDep = Annotated[UserQueryParams, Query()]
