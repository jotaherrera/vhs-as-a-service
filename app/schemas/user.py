from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserCreateInternal(UserCreate):
    role_id: int
    is_active: bool = True


class UserCreatePublic(UserCreate):
    role: str = "user"


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
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

    class Config:
        from_attributes = True


class UsersResponse(BaseModel):
    users: list[UserResponse]
    total: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str
