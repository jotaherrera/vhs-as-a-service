from typing import ClassVar

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from app.models import Base


class Role(Base):
    __tablename__ = "roles"
    __table_args__: ClassVar[dict[str, str]] = {"schema": "app"}

    id = Column(Integer, primary_key=True)

    name = Column(String(255), unique=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    modified_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    is_active = Column(Boolean, nullable=False)

    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return (
            f"Role(id={self.id}, name={self.name}, is_active={self.is_active})"
            f"created_at={self.created_at}, modified_at={self.modified_at}"
        )
