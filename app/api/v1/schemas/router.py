from typing import Literal

from pydantic import BaseModel


class TokenRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    token: str
    type: Literal["Bearer"]
