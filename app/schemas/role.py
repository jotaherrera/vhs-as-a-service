from datetime import datetime

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    is_active: bool = True


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    modified_at: datetime
    is_active: bool
