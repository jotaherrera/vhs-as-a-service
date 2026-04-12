from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from sqlalchemy import Boolean, DateTime, Enum, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.infrastructure.base import Base


class RoleName(StrEnum):
    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"


class Role(Base):
    __tablename__ = "roles"
    __table_args__: ClassVar[dict[str, str]] = {"schema": "app"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        Enum(RoleName, name="role_name", schema="app"),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return (
            f"<Role(id={self.id}, "
            f"name={str(self.name)!r}, "
            f"is_active={self.is_active}, "
            f"created_at={self.created_at}, "
            f"modified_at={self.modified_at})>"
        )
