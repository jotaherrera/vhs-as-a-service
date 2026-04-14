from datetime import UTC, datetime
from typing import Protocol


class Persistable(Protocol):
    id: int | None
    created_at: datetime | None
    is_active: bool


class BaseFakeRepository[T: Persistable]:
    def __init__(self, entities: list[T] | None = None) -> None:
        self._entities: dict[int, T] = {}
        self._next_id = 1

        for entity in entities or []:
            self._persist(entity)

    def _persist(self, entity: T) -> None:
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1

        if entity.created_at is None:
            entity.created_at = datetime.now(UTC)

        self._entities[entity.id] = entity

    def get_all(self, *, is_active: bool | None = None) -> list[T]:
        entities = list(self._entities.values())

        if is_active is not None:
            entities = [i for i in entities if i.is_active == is_active]

        return entities

    def find_by_id(self, entity_id: int) -> T | None:
        return self._entities.get(entity_id)

    def create(self, entity: T) -> T:
        self._persist(entity)
        return entity
