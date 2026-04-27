from datetime import UTC, datetime, timedelta

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.movie.contracts import AbstractMovieRepository
from app.modules.movie.repository import MovieRepository
from app.modules.rental.contracts import AbstractRentalRepository
from app.modules.rental.model import Rental, RentalStatus
from app.modules.rental.repository import RentalRepository
from app.modules.rental.schemas import RentalCreate, RentalList, RentalResponse
from app.modules.role.model import RoleName
from app.modules.user.contracts import AbstractUserRepository
from app.modules.user.model import User
from app.modules.user.repository import UserRepository


def get_rental_service(
    rental_repo: RentalRepository,
    user_repo: UserRepository,
    movie_repo: MovieRepository,
) -> "RentalService":
    return RentalService(rental_repo=rental_repo, user_repo=user_repo, movie_repo=movie_repo)


class RentalService:
    def __init__(
        self,
        rental_repo: AbstractRentalRepository,
        user_repo: AbstractUserRepository,
        movie_repo: AbstractMovieRepository,
    ) -> None:
        self.rental_repo = rental_repo
        self.user_repo = user_repo
        self.movie_repo = movie_repo

    def list_all_rentals(self, current_user: User) -> RentalList:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        rentals = self.rental_repo.get_all()
        return RentalList(
            rentals=[RentalResponse.model_validate(rental) for rental in rentals],
            total=len(rentals),
        )

    def register_rental(self, rental_request: RentalCreate) -> RentalResponse:
        customer = self.user_repo.find_by_id(rental_request.customer_id)
        if customer is None:
            raise NotFoundError(detail="Customer not found.")

        staff = self.user_repo.find_by_id(rental_request.staff_id)
        if staff is None:
            raise NotFoundError(detail="Staff not found.")

        movie = self.movie_repo.find_by_id(rental_request.movie_id)
        if movie is None or movie.copies_available <= 0:
            raise NotFoundError(detail="Movie not available.")

        movie.copies_available -= 1
        self.movie_repo.update(movie)

        rental = Rental(
            customer=customer,
            staff=staff,
            movie=movie,
            expected_return_at=datetime.now(UTC) + timedelta(days=7),
            status=RentalStatus.ACTIVE,
        )

        return RentalResponse.model_validate(self.rental_repo.create(rental))

    def return_rental(self, rental_id: int) -> RentalResponse:
        return_time = datetime.now(UTC)

        rental = self.rental_repo.find_by_id(rental_id)
        if rental is None:
            raise NotFoundError(detail="Rental not found.")

        if rental.status == RentalStatus.COMPLETED:
            raise ConflictError(detail="Rental already returned.")

        movie = self.movie_repo.find_by_id(rental.movie_id)
        if movie is None:
            raise NotFoundError(detail="Movie not found.")

        rental.status = (
            RentalStatus.LATE if return_time > rental.expected_return_at else RentalStatus.COMPLETED
        )
        rental.returned_at = return_time

        movie.copies_available += 1
        self.movie_repo.update(movie)

        return RentalResponse.model_validate(self.rental_repo.update(rental))
