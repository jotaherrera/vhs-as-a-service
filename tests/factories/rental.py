from datetime import UTC, datetime, timedelta

from factory import LazyFunction, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.modules.rentals.model import Rental, RentalStatus
from tests.factories.movie import MovieFactory
from tests.factories.user import UserFactory


class RentalFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Rental
        sqlalchemy_session_persistence = "flush"

    status = RentalStatus.ACTIVE
    expected_return_at = LazyFunction(
        lambda: datetime.now(tz=UTC) + timedelta(days=7),
    )
    returned_at = None

    movie = SubFactory(MovieFactory)
    customer = SubFactory(UserFactory)
    staff = SubFactory(UserFactory)
