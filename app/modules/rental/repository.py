from datetime import UTC, datetime

from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session

from app.modules.rental.contracts import AbstractRentalRepository
from app.modules.rental.model import Rental, RentalStatus


class RentalRepository(AbstractRentalRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, *, status: RentalStatus | None = None) -> Sequence[Rental]:
        stmt = select(Rental)
        if status is not None:
            stmt = stmt.where(Rental.status == status)
        return self.db.scalars(stmt).all()

    def find_by_id(self, entity_id: int) -> Rental | None:
        return self.db.get(Rental, entity_id)

    def find_by_customer(
        self,
        customer_id: int,
        *,
        status: RentalStatus | None = None,
    ) -> Sequence[Rental]:
        stmt = select(Rental).where(Rental.customer_id == customer_id)
        if status is not None:
            stmt = stmt.where(Rental.status == status)
        return self.db.scalars(stmt).all()

    def find_by_movie(
        self,
        movie_id: int,
        *,
        status: RentalStatus | None = None,
    ) -> Sequence[Rental]:
        stmt = select(Rental).where(Rental.movie_id == movie_id)
        if status is not None:
            stmt = stmt.where(Rental.status == status)
        return self.db.scalars(stmt).all()

    def find_by_staff(self, staff_id: int) -> Sequence[Rental]:
        stmt = select(Rental).where(Rental.staff_id == staff_id)
        return self.db.scalars(stmt).all()

    def find_overdue(self) -> Sequence[Rental]:
        now = datetime.now(tz=UTC)
        stmt = select(Rental).where(Rental.expected_return_at < now)
        return self.db.scalars(stmt).all()

    def create(self, entity: Rental) -> Rental:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Rental) -> Rental:
        self.db.commit()
        self.db.refresh(entity)
        return entity
