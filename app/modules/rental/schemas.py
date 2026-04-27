from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.modules.movie.schemas import MovieResponsePublic
from app.modules.rental.model import RentalStatus
from app.modules.user.schemas import UserResponse


class RentalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: RentalStatus
    expected_return_at: datetime
    returned_at: datetime | None
    movie: MovieResponsePublic
    customer: UserResponse
    staff: UserResponse
    created_at: datetime
    modified_at: datetime


class RentalCreate(BaseModel):
    customer_id: int
    staff_id: int
    movie_id: int


class RentalList(BaseModel):
    rentals: list[RentalResponse]
    total: int
