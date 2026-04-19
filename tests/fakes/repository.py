from datetime import UTC, datetime
from typing import Protocol

from sqlalchemy import Sequence

from app.modules.movie.contracts import AbstractMovieRepository
from app.modules.movie.model import Movie
from app.modules.movie.schemas import ExternalId
from app.modules.rental.contracts import AbstractRentalRepository
from app.modules.rental.model import Rental, RentalStatus
from app.modules.role.contracts import AbstractRoleRepository
from app.modules.role.model import Role, RoleName
from app.modules.user.contracts import AbstractUserRepository
from app.modules.user.model import User


class Persistable(Protocol):
    id: int | None
    created_at: datetime | None
    modified_at: datetime | None


class BaseFakeRepository[T: Persistable]:
    def __init__(self, entities: list[T] | None = None) -> None:
        self.entities: dict[int, T] = {}
        self._next_id = 1
        for entity in entities or []:
            self._persist(entity)

    def _touch(self, entity: Persistable) -> None:
        now = datetime.now(UTC)
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        if entity.created_at is None:
            entity.created_at = now
        entity.modified_at = now

    def _persist(self, entity: T) -> None:
        self._touch(entity)
        self.entities[entity.id] = entity

    def find_by_id(self, entity_id: int) -> T | None:
        return self.entities.get(entity_id)

    def create(self, entity: T) -> T:
        self._persist(entity)
        return entity

    def update(self, entity: T) -> T:
        self._touch(entity)
        self.entities[entity.id] = entity
        return entity


class FakeUserRepository(BaseFakeRepository[User], AbstractUserRepository):
    def __init__(self, users: list[User] | None = None) -> None:
        super().__init__(entities=users)

    def _persist(self, entity: User) -> None:
        self._touch(entity.role)
        super()._persist(entity)

    def update(self, entity: User) -> User:
        self._touch(entity.role)
        self._touch(entity)
        self.entities[entity.id] = entity
        return entity

    def get_all(self, *, is_active: bool | None = None) -> list[User]:
        entities = list(self.entities.values())
        if is_active is not None:
            entities = [u for u in entities if u.is_active == is_active]
        return entities

    def delete(self, entity: User) -> None:
        entity.is_active = False

    def get_by_email(self, email: str) -> User | None:
        return next((u for u in self.entities.values() if u.email == email), None)


class FakeRoleRepository(BaseFakeRepository[Role], AbstractRoleRepository):
    def __init__(self, roles: list[Role] | None = None) -> None:
        super().__init__(entities=roles)

    def get_all(self, *, is_active: bool | None = None) -> list[Role]:
        entities = list(self.entities.values())
        if is_active is not None:
            entities = [r for r in entities if r.is_active == is_active]
        return entities

    def delete(self, entity: Role) -> None:
        entity.is_active = False

    def get_by_name(self, name: RoleName) -> Role | None:
        return next((r for r in self.entities.values() if r.name == name), None)


class FakeMovieRepository(BaseFakeRepository[Movie], AbstractMovieRepository):
    def __init__(self, movies: list[Movie] | None = None) -> None:
        super().__init__(entities=movies)

    def get_all(self, *, is_active: bool | None = None) -> list[Movie]:
        entities = list(self.entities.values())
        if is_active is not None:
            entities = [m for m in entities if m.is_active == is_active]
        return entities

    def delete(self, entity: Movie) -> None:
        entity.is_active = False

    def get_by_name(self, name: str) -> list[Movie]:
        return [m for m in self.entities.values() if name.lower() in m.title.lower()]

    def find_by_external_id(self, external_id: ExternalId) -> Movie | None:
        for movie in self.entities.values():
            for ext in movie.external_ids:
                if (
                    ext.provider == external_id.provider
                    and ext.external_id == external_id.external_id
                ):
                    return movie
        return None


class FakeRentalRepository(BaseFakeRepository[Rental], AbstractRentalRepository):
    def __init__(self, rentals: list[Rental] | None = None) -> None:
        super().__init__(entities=rentals)

    def get_all(self, *, status: RentalStatus | None = None) -> Sequence[Rental]:
        entities = list(self.entities.values())
        if status is not None:
            entities = [r for r in entities if r.status == status]
        return entities

    def find_by_customer(
        self,
        customer_id: int,
        *,
        status: RentalStatus | None = None,
    ) -> Sequence[Rental]:
        entities = [r for r in self.entities.values() if r.customer_id == customer_id]
        if status is not None:
            entities = [r for r in entities if r.status == status]
        return entities

    def find_by_movie(
        self,
        movie_id: int,
        *,
        status: RentalStatus | None = None,
    ) -> Sequence[Rental]:
        entities = [r for r in self.entities.values() if r.movie_id == movie_id]
        if status is not None:
            entities = [r for r in entities if r.status == status]
        return entities

    def find_by_staff(self, staff_id: int) -> Sequence[Rental]:
        return [r for r in self.entities.values() if r.staff_id == staff_id]

    def find_overdue(self) -> Sequence[Rental]:
        now = datetime.now(UTC)
        return [r for r in self.entities.values() if r.expected_return_at < now]
