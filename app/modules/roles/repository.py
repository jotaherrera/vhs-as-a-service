from sqlalchemy import Select, Sequence
from sqlalchemy.orm import Session

from app.modules.roles.contracts import AbstractRoleRepository
from app.modules.roles.model import Role


class RoleRepository(AbstractRoleRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, *, is_active: bool | None = None) -> Sequence[Role]:
        stmt = Select(Role)

        if is_active is not None:
            stmt = stmt.where(Role.is_active.is_(is_active))

        return self.db.scalars(stmt).all()

    def find_by_id(self, entity_id: int) -> Role | None:
        stmt = Select(Role).where(Role.id == entity_id)
        return self.db.scalar(stmt)

    def create(self, entity: Role) -> Role:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_name(self, name: str) -> Role | None:
        stmt = Select(Role).where(Role.name == name)
        return self.db.scalar(stmt)
