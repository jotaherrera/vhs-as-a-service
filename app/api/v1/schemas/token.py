from typing import Literal

from pydantic import BaseModel, EmailStr

from app.fields import PasswordStr


class TokenRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class TokenResponse(BaseModel):
    token: str
    type: Literal["Bearer"]
