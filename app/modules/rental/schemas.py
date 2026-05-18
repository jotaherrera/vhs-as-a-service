from datetime import datetime

from pydantic import BaseModel, ConfigDict, computed_field

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


class RentalUpdate(BaseModel):
    status: RentalStatus | None = None
    expected_return_at: datetime | None = None
    returned_at: datetime | None = None


class RentalList(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    rentals: list[RentalResponse]

    @computed_field
    @property
    def total(self) -> int:
        return len(self.rentals)
