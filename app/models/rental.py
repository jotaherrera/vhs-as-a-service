from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String

from app.models import Base


class RentalStatus(StrEnum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    LATE = "LATE"
    DAMAGED = "DAMAGED"


class Rental(Base):
    __tablename__ = "rentals"
    __table_args__: ClassVar[dict[str, str]] = {"schema": "app"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    expected_return_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

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

    customer = relationship(
        "User",
        foreign_keys="[Rental.customer_id]",
        back_populates="customer_rentals",
    )
    staff = relationship(
        "User",
        foreign_keys="[Rental.staff_id]",
        back_populates="staff_rentals",
    )
    movie = relationship("Movie", back_populates="rentals")

    @validates("status")
    def validate_status(self, _key: str, value: str) -> str:
        if value not in RentalStatus:
            msg = f"Invalid status: {value}. Must be one of {list(RentalStatus)}"
            raise ValueError(msg)
        return value

    def __repr__(self) -> str:
        return (
            f"Rental(id={self.id!r}, status={self.status!r}, "
            f"movie_id={self.movie_id!r}, customer_id={self.customer_id!r}, "
            f"staff_id={self.staff_id!r}, expected_return_at={self.expected_return_at!r}, "
            f"returned_at={self.returned_at!r})"
        )
