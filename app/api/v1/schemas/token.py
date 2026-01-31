from typing import Literal

from pydantic import BaseModel, EmailStr, SecretStr

from app.fields import PasswordStr


class TokenRequest(BaseModel):
    email: EmailStr
    password: PasswordStr


class TokenResponse(BaseModel):
    token: SecretStr
    type: Literal["Bearer"]
