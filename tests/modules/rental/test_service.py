from datetime import UTC, datetime, timedelta

import pytest

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.movie.model import Movie
from app.modules.rental.model import Rental, RentalStatus
from app.modules.rental.schemas import RentalCreate, RentalResponse, RentalUpdate
from app.modules.rental.service import RentalService
from app.modules.role.model import RoleName
from app.modules.user.model import User
from tests.fakes.factories.movie import MovieFactory
from tests.fakes.factories.rental import RentalFactory
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory
from tests.fakes.repository import FakeMovieRepository, FakeRentalRepository, FakeUserRepository


def make_service(
    rentals: list[Rental] | None = None,
    users: list[User] | None = None,
    movies: list[Movie] | None = None,
) -> RentalService:
    return RentalService(
        rental_repo=FakeRentalRepository(rentals),
        user_repo=FakeUserRepository(users),
        movie_repo=FakeMovieRepository(movies),
    )


def test_list_all_rentals_when_staff() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie_1 = MovieFactory.build()
    movie_2 = MovieFactory.build()
    rental_1 = RentalFactory.build(customer=customer, staff=staff, movie=movie_1)
    rental_2 = RentalFactory.build(customer=customer, staff=staff, movie=movie_2)
    service = make_service(
        users=[staff, customer],
        movies=[movie_1, movie_2],
        rentals=[rental_1, rental_2],
    )

    result = service.list_all_rentals(staff)

    assert result.total == 2
    assert len(result.rentals) == 2


def test_list_all_rentals_raises_forbidden_when_not_staff() -> None:
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = make_service(users=[customer])

    with pytest.raises(ForbiddenError):
        service.list_all_rentals(customer)


def test_register_rental_success() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=1)
    service = make_service(users=[staff, customer], movies=[movie])

    rental_request = RentalCreate(
        customer_id=customer.id,
        staff_id=staff.id,
        movie_id=movie.id,
    )

    result = service.register(rental_request)

    assert result.movie.id == movie.id
    assert result.status == RentalStatus.ACTIVE


def test_register_rental_decrements_copies_available() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=2)
    service = make_service(users=[staff, customer], movies=[movie])

    service.register(
        RentalCreate(customer_id=customer.id, staff_id=staff.id, movie_id=movie.id),
    )

    assert movie.copies_available == 1


def test_register_rental_raises_not_found_when_customer_missing() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    movie = MovieFactory.build(copies_available=1)
    service = make_service(users=[staff], movies=[movie])

    with pytest.raises(NotFoundError):
        service.register(
            RentalCreate(customer_id=9999, staff_id=staff.id, movie_id=movie.id),
        )


def test_register_rental_raises_not_found_when_staff_missing() -> None:
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=1)
    service = make_service(users=[customer], movies=[movie])

    with pytest.raises(NotFoundError):
        service.register(
            RentalCreate(customer_id=customer.id, staff_id=9999, movie_id=movie.id),
        )


def test_register_rental_raises_not_found_when_movie_not_found() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = make_service(users=[staff, customer], movies=[])

    with pytest.raises(NotFoundError):
        service.register(
            RentalCreate(customer_id=customer.id, staff_id=staff.id, movie_id=9999),
        )


def test_register_rental_raises_not_found_when_movie_has_no_copies() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=0)
    service = make_service(users=[staff, customer], movies=[movie])

    with pytest.raises(NotFoundError):
        service.register(
            RentalCreate(customer_id=customer.id, staff_id=staff.id, movie_id=movie.id),
        )


def test_return_rental_on_time_sets_completed() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=0)
    rental = RentalFactory.build(
        customer=customer,
        staff=staff,
        movie=movie,
        status=RentalStatus.ACTIVE,
        expected_return_at=datetime.now(UTC) + timedelta(days=3),
    )
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])

    result = service.return_rental(rental.id)

    assert result.status == RentalStatus.COMPLETED
    assert result.returned_at is not None


def test_return_rental_late_sets_late_status() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=0)
    rental = RentalFactory.build(
        customer=customer,
        staff=staff,
        movie=movie,
        status=RentalStatus.ACTIVE,
        expected_return_at=datetime.now(UTC) - timedelta(days=1),
    )
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])

    result = service.return_rental(rental.id)

    assert result.status == RentalStatus.LATE


def test_return_rental_increments_copies_available() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=0)
    rental = RentalFactory.build(
        customer=customer,
        staff=staff,
        movie=movie,
        status=RentalStatus.ACTIVE,
        expected_return_at=datetime.now(UTC) + timedelta(days=3),
    )
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])

    service.return_rental(rental.id)

    assert movie.copies_available == 1


def test_return_rental_raises_not_found_when_rental_missing() -> None:
    service = make_service()

    with pytest.raises(NotFoundError):
        service.return_rental(9999)


def test_return_rental_raises_conflict_when_already_returned() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build(copies_available=1)
    rental = RentalFactory.build(
        customer=customer,
        staff=staff,
        movie=movie,
        status=RentalStatus.COMPLETED,
    )
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])

    with pytest.raises(ConflictError):
        service.return_rental(rental.id)


def test_return_rental_raises_not_found_when_movie_not_found() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    rental = RentalFactory.build(customer=customer, staff=staff)
    service = make_service(users=[staff, customer], movies=[], rentals=[rental])

    with pytest.raises(NotFoundError):
        service.return_rental(rental.id)


def test_get_by_id_returns_rental() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build()
    rental = RentalFactory.build(customer=customer, staff=staff, movie=movie)
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])

    result = service.get_by_id(rental.id)

    assert isinstance(result, RentalResponse)
    assert result.id == rental.id


def test_get_by_id_raises_not_found_when_missing() -> None:
    service = make_service()

    with pytest.raises(NotFoundError):
        service.get_by_id(9999)


def test_modify_raises_not_found_when_missing() -> None:
    service = make_service()

    with pytest.raises(NotFoundError):
        service.modify(9999, RentalUpdate(expected_return_at=datetime.now(UTC) + timedelta(days=1)))


def test_modify_updates_expected_return_at() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build()
    rental = RentalFactory.build(
        customer=customer,
        staff=staff,
        movie=movie,
        status=RentalStatus.ACTIVE,
    )
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])
    new_date = datetime.now(UTC) + timedelta(days=14)

    result = service.modify(rental.id, RentalUpdate(expected_return_at=new_date))

    assert isinstance(result, RentalResponse)
    assert result.expected_return_at == new_date


def test_remove_raises_not_found_when_missing() -> None:
    service = make_service()

    with pytest.raises(NotFoundError):
        service.remove(9999)


def test_removes_rental_successfully() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    movie = MovieFactory.build()
    rental = RentalFactory.build(customer=customer, staff=staff, movie=movie)
    service = make_service(users=[staff, customer], movies=[movie], rentals=[rental])

    service.remove(rental.id)
