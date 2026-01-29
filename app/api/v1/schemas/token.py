from typing import Literal

from pydantic import BaseModel, EmailStr


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    token: str
    type: Literal["Bearer"]
