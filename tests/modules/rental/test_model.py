import pytest

from tests.fakes.factories.rental import RentalFactory


def test_rental_string_repr() -> None:
    rental = RentalFactory.build()

    expected = (
        f"Rental(id={rental.id!r}, status={rental.status!r}, "
        f"movie_id={rental.movie_id!r}, customer_id={rental.customer_id!r}, "
        f"staff_id={rental.staff_id!r}, expected_return_at={rental.expected_return_at!r}, "
        f"returned_at={rental.returned_at!r})"
    )

    assert repr(rental) == expected


def test_create_rental_with_invalid_status() -> None:
    with pytest.raises(ValueError, match="Invalid status:"):
        RentalFactory.build(status="INVALID")
