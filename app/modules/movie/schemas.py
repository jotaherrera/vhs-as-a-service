from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ExternalId(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    provider: str
    external_id: str


class MovieResponsePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    title: str
    description: str
    genre: str
    director: str
    critic_rating: int
    age_rating: str
    release_date: date


class MovieResponsePrivate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    title: str
    description: str
    genre: str
    director: str
    critic_rating: int
    age_rating: str
    release_date: date
    rental_price: float
    copies_available: int
    created_at: datetime
    is_active: bool
    external_ids: list[ExternalId]


class MovieList(BaseModel):
    model_config = ConfigDict(extra="forbid")

    movies: list[MovieResponsePublic | MovieResponsePrivate]
    total: int


class MovieCreate(BaseModel):
    title: str
    description: str
    genre: str
    director: str
    critic_rating: int
    age_rating: str
    release_date: str
    rental_price: float
    copies_available: int
    external_ids: list[ExternalId] = Field(min_length=1)
