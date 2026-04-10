from typing import Literal

from pydantic import BaseModel, EmailStr

from app.core.fields import PasswordStr


class TokenCreate(BaseModel):
    email: EmailStr
    password: PasswordStr


class TokenResponse(BaseModel):
    token: str
    type: Literal["Bearer"]
