from typing import Annotated

from pydantic import Field, SecretStr

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 64

PasswordStr = Annotated[
    SecretStr,
    Field(min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_LENGTH),
]
