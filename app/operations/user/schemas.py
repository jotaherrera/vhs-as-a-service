from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str
    last_name: str


class UserCreateBase(UserBase):
    password: str


class UserCreate(UserCreateBase):
    role_id: int
    is_active: bool = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    is_active: bool | None = None
