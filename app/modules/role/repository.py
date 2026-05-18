from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, Sequence
from sqlalchemy.orm import Session

from app.database.infrastructure.session import DbSession
from app.modules.role.contracts import AbstractRoleRepository
from app.modules.role.model import Role, RoleName
from app.modules.role.schemas import RoleFilters


def get_role_repository(db: DbSession) -> AbstractRoleRepository:
    return RoleRepository(db)


RoleRepo = Annotated[AbstractRoleRepository, Depends(get_role_repository)]


class RoleRepository(AbstractRoleRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, filters: RoleFilters) -> Sequence[Role]:
        stmt = Select(Role)

        if filters.is_active is not None:
            stmt = stmt.where(Role.is_active.is_(filters.is_active))

        return self.db.scalars(stmt).all()

    def find_by_id(self, entity_id: int) -> Role | None:
        stmt = Select(Role).where(Role.id == entity_id)
        return self.db.scalar(stmt)

    def create(self, entity: Role) -> Role:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: Role) -> Role:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: Role) -> None:
        entity.is_active = False
        self.db.commit()

    def find_by_name(self, name: RoleName) -> Role | None:
        stmt = Select(Role).where(Role.name == name)
        return self.db.scalar(stmt)
