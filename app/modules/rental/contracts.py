from abc import ABC, abstractmethod

from sqlalchemy import Sequence

from app.modules.rental.model import Rental, RentalStatus


class AbstractRentalRepository(ABC):
    @abstractmethod
    def get_all(self, *, status: RentalStatus | None = None) -> Sequence[Rental]: ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Rental | None: ...

    @abstractmethod
    def find_by_customer(
        self,
        customer_id: int,
        *,
        status: RentalStatus | None = None,
    ) -> Sequence[Rental]: ...

    @abstractmethod
    def find_by_movie(
        self,
        movie_id: int,
        *,
        status: RentalStatus | None = None,
    ) -> Sequence[Rental]: ...

    @abstractmethod
    def find_by_staff(self, staff_id: int) -> Sequence[Rental]: ...

    @abstractmethod
    def find_overdue(self) -> Sequence[Rental]: ...

    @abstractmethod
    def create(self, entity: Rental) -> Rental: ...

    @abstractmethod
    def update(self, entity: Rental) -> Rental: ...

    @abstractmethod
    def delete(self, entity: Rental) -> None: ...
