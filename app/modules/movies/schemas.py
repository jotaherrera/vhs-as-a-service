from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MovieResponsePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    genre: str
    director: str
    critic_rating: int
    age_rating: str
    release_date: date


class MovieResponsePrivate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class MovieList(BaseModel):
    movies: list[MovieResponsePublic | MovieResponsePrivate]
    total: int


class ExternalId(BaseModel):
    provider: str
    external_id: str


class MovieCreate(BaseModel):
    title: str
    description: str
    genre: str
    director: str
    critic_rating: str
    age_rating: str
    release_date: str
    rental_price: float
    copies_available: int
    external_ids: list[ExternalId] = Field(min_length=1)
