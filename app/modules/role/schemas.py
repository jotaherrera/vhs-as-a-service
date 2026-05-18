from datetime import datetime
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, ConfigDict, computed_field

from app.modules.role.model import RoleName


class RoleCreate(BaseModel):
    name: RoleName
    is_active: bool = True


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: RoleName
    created_at: datetime
    modified_at: datetime
    is_active: bool


class RoleList(BaseModel):
    ConfigDict(extra="forbid", from_attributes=True)

    roles: list[RoleResponse]

    @computed_field
    @property
    def total(self) -> int:
        return len(self.roles)


class RoleFilters(BaseModel):
    is_active: bool | None = None


RoleFiltersQuery = Annotated[RoleFilters, Query()]
