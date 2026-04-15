from datetime import date, datetime
from typing import ClassVar

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Float

from app.database.infrastructure.base import Base
from app.modules.rental.model import Rental


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
    rental_price: Mapped[float] = mapped_column(Float, nullable=False)
    copies_available: Mapped[int] = mapped_column(Integer, nullable=False)

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

    rentals: Mapped[list[Rental]] = relationship("Rental", back_populates="movie")
    external_ids: Mapped[list["MovieExternalId"]] = relationship(
        "MovieExternalId",
        back_populates="movie",
    )

    def __repr__(self) -> str:
        return (
            f"<Movie(id={self.id}, "
            f"title={self.title!r}, "
            f"genre={self.genre!r}, "
            f"director={self.director!r}, "
            f"critic_rating={self.critic_rating}, "
            f"age_rating={self.age_rating!r}, "
            f"release_date={self.release_date}, "
            f"copies_available={self.copies_available}), "
            f"rental_price={self.rental_price}, "
            f"is_active={self.is_active}>"
        )


class MovieExternalId(Base):
    __tablename__ = "movie_external_ids"
    __table_args__: ClassVar[tuple] = (
        UniqueConstraint("provider", "external_id", name="uq_movie_external_id_per_provider"),
        {"schema": "app"},
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("app.movies.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    external_id: Mapped[str] = mapped_column(String(100), nullable=False)

    movie: Mapped[Movie] = relationship("Movie", back_populates="external_ids")

    def __repr__(self) -> str:
        return (
            f"<MovieExternalId(id={self.id!r}, "
            f"movie_id={self.movie_id!r}, "
            f"provider={self.provider!r}, "
            f"external_id={self.external_id!r})>"
        )
