from datetime import datetime

from pydantic import BaseModel, ConfigDict

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
    model_config = ConfigDict(extra="forbid")

    roles: list[RoleResponse]
    total: int
