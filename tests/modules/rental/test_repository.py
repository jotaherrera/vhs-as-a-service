from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from app.modules.rental.model import Rental, RentalStatus
from app.modules.rental.repository import RentalRepository
from app.modules.role.model import RoleName
from tests.fakes.factories.movie import MovieFactory
from tests.fakes.factories.rental import RentalFactory
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory


@pytest.fixture
def rental_repo(db_session: Session) -> RentalRepository:
    return RentalRepository(db_session)


def test_find_by_id_returns_rental_when_exists(rental_repo: RentalRepository) -> None:
    rental = RentalFactory.create()

    result = rental_repo.find_by_id(rental.id)

    assert result is not None
    assert result.id == rental.id


def test_find_by_id_returns_none_when_not_found(rental_repo: RentalRepository) -> None:
    result = rental_repo.find_by_id(999_999)

    assert result is None


def test_get_all_returns_all_rentals_without_filter(rental_repo: RentalRepository) -> None:
    RentalFactory.create(status=RentalStatus.ACTIVE)
    RentalFactory.create(status=RentalStatus.COMPLETED)

    result = rental_repo.get_all()

    assert len(result) == 2


def test_get_all_with_status_returns_only_matching(rental_repo: RentalRepository) -> None:
    active = RentalFactory.create(status=RentalStatus.ACTIVE)
    RentalFactory.create(status=RentalStatus.COMPLETED)

    result = rental_repo.get_all(status=RentalStatus.ACTIVE)

    assert len(result) == 1
    assert result[0].id == active.id
    assert result[0].status == RentalStatus.ACTIVE


def test_create_persists_rental_and_returns_it(
    rental_repo: RentalRepository,
    db_session: Session,
) -> None:
    customer = UserFactory.create()
    staff = UserFactory.create()
    movie = MovieFactory.create()

    rental = RentalFactory.build(
        customer=customer,
        staff=staff,
        movie=movie,
    )

    result = rental_repo.create(rental)

    assert result.id is not None
    assert db_session.get(Rental, result.id) is not None


def test_update_persists_changes(rental_repo: RentalRepository, db_session: Session) -> None:
    customer = UserFactory.create()
    staff = UserFactory.create()
    movie = MovieFactory.create()

    rental = rental_repo.create(
        RentalFactory.build(
            customer=customer,
            staff=staff,
            movie=movie,
            status=RentalStatus.ACTIVE,
        ),
    )

    rental.status = RentalStatus.COMPLETED
    rental_repo.update(rental)

    db_rental = db_session.get(Rental, rental.id)
    assert db_rental is not None
    assert db_rental.status == RentalStatus.COMPLETED


def test_find_by_customer_returns_all_rentals_for_customer(
    rental_repo: RentalRepository,
) -> None:
    rental = RentalFactory.create()
    RentalFactory.create()

    result = rental_repo.find_by_customer(rental.customer_id)

    assert len(result) == 1
    assert result[0].id == rental.id


def test_find_by_customer_with_status_returns_only_matching(
    rental_repo: RentalRepository,
) -> None:
    active = RentalFactory.create(status=RentalStatus.ACTIVE)
    RentalFactory.create(
        customer_id=active.customer_id,
        status=RentalStatus.COMPLETED,
    )

    result = rental_repo.find_by_customer(active.customer_id, status=RentalStatus.ACTIVE)

    assert len(result) == 1
    assert result[0].id == active.id


def test_find_by_customer_returns_empty_when_no_match(
    rental_repo: RentalRepository,
) -> None:
    result = rental_repo.find_by_customer(999_999)

    assert result == []


def test_find_by_movie_returns_all_rentals_for_movie(
    rental_repo: RentalRepository,
) -> None:
    rental = RentalFactory.create()
    RentalFactory.create()

    result = rental_repo.find_by_movie(rental.movie_id)

    assert len(result) == 1
    assert result[0].id == rental.id


def test_find_by_movie_with_status_returns_only_matching(
    rental_repo: RentalRepository,
) -> None:
    active = RentalFactory.create(status=RentalStatus.ACTIVE)
    RentalFactory.create(
        movie_id=active.movie_id,
        status=RentalStatus.COMPLETED,
    )

    result = rental_repo.find_by_movie(active.movie_id, status=RentalStatus.ACTIVE)

    assert len(result) == 1
    assert result[0].id == active.id


def test_find_by_movie_returns_empty_when_no_match(rental_repo: RentalRepository) -> None:
    result = rental_repo.find_by_movie(999_999)

    assert result == []


def test_find_by_staff_returns_rentals_processed_by_staff(
    rental_repo: RentalRepository,
    db_session: Session,  # noqa: ARG001
) -> None:
    staff = UserFactory.create()
    RentalFactory.create(staff=staff)
    RentalFactory.create(staff=staff)
    RentalFactory.create()

    result = rental_repo.find_by_staff(staff.id)

    assert len(result) == 2
    assert all(r.staff_id == staff.id for r in result)


def test_find_by_staff_returns_empty_when_no_match(rental_repo: RentalRepository) -> None:
    result = rental_repo.find_by_staff(999_999)

    assert result == []


def test_find_overdue_returns_all_overdue(
    rental_repo: RentalRepository,
    db_session: Session,  # noqa: ARG001
) -> None:
    RentalFactory.create(
        status=RentalStatus.ACTIVE,
        expected_return_at=datetime.now(tz=UTC) - timedelta(days=1),
    )
    RentalFactory.create(
        status=RentalStatus.COMPLETED,
        expected_return_at=datetime.now(tz=UTC) - timedelta(days=1),
    )
    RentalFactory.create(
        status=RentalStatus.ACTIVE,
        expected_return_at=datetime.now(tz=UTC) + timedelta(days=1),
    )

    result = rental_repo.find_overdue()

    assert len(result) == 2


def test_find_overdue_returns_empty_when_none_overdue(
    rental_repo: RentalRepository,
    db_session: Session,  # noqa: ARG001
) -> None:
    RentalFactory.create(
        status=RentalStatus.ACTIVE,
        expected_return_at=datetime.now(tz=UTC) + timedelta(days=1),
    )

    result = rental_repo.find_overdue()

    assert result == []


def test_delete_soft_deletes_rental(rental_repo: RentalRepository, db_session: Session) -> None:
    staff_role = RoleFactory(name=RoleName.STAFF)
    customer_role = RoleFactory(name=RoleName.CUSTOMER)
    staff = UserFactory(role=staff_role)
    customer = UserFactory(role=customer_role)
    movie = MovieFactory()
    rental = rental_repo.create(
        RentalFactory.build(
            customer=customer,
            staff=staff,
            movie=movie,
            status=RentalStatus.ACTIVE,
        ),
    )

    rental_repo.delete(rental)

    db_rental = db_session.get(Rental, rental.id)
    assert db_rental is not None
    assert db_rental.status == RentalStatus.REMOVED
