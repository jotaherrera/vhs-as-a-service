from datetime import datetime

from pydantic import BaseModel

from app.modules.role.model import RoleName


class RoleCreate(BaseModel):
    name: RoleName
    is_active: bool = True


class RoleResponse(BaseModel):
    id: int
    name: RoleName
    created_at: datetime
    modified_at: datetime
    is_active: bool
