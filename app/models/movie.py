from datetime import date, datetime
from typing import ClassVar

from sqlalchemy import Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class Movie(Base):
    __tablename__ = "movies"
    __table_args__: ClassVar[dict[str, str]] = {"schema": "app"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    director: Mapped[str] = mapped_column(String(255), nullable=False)
    critic_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    age_rating: Mapped[str] = mapped_column(String(10), nullable=False)
    release_date: Mapped[date] = mapped_column(Date, nullable=False)

    copies_available: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Movie(id={self.id}, title={self.title!r}, genre={self.genre!r}, "
            f"director={self.director!r}, critic_rating={self.critic_rating}, "
            f"age_rating={self.age_rating!r}, release_date={self.release_date}, "
            f"copies_available={self.copies_available})"
        )
