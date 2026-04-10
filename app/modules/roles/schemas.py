from datetime import datetime

from pydantic import BaseModel

from app.modules.roles.model import Roles


class RoleCreate(BaseModel):
    name: Roles
    is_active: bool = True


class RoleResponse(BaseModel):
    id: int
    name: Roles
    created_at: datetime
    modified_at: datetime
    is_active: bool
