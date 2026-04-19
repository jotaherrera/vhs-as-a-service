from datetime import UTC, datetime, timedelta

from factory import LazyFunction, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.modules.rental.model import Rental, RentalStatus
from tests.fakes.factories.movie import MovieFactory
from tests.fakes.factories.user import UserFactory


class RentalFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Rental
        sqlalchemy_session_persistence = "flush"

    customer = SubFactory(UserFactory)
    staff = SubFactory(UserFactory)
    movie = SubFactory(MovieFactory)
    status = RentalStatus.ACTIVE
    expected_return_at = LazyFunction(lambda: datetime.now(UTC) + timedelta(days=7))
    returned_at = None
