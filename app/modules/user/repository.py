from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, Sequence
from sqlalchemy.orm import Session

from app.database.infrastructure.session import DbSession
from app.modules.role.model import Role
from app.modules.user.contracts import AbstractUserRepository
from app.modules.user.model import User
from app.modules.user.schemas import UserFilters


def get_user_repository(db: DbSession) -> AbstractUserRepository:
    return UserRepository(db)


UserRepo = Annotated[AbstractUserRepository, Depends(get_user_repository)]


class UserRepository(AbstractUserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, filters: UserFilters) -> Sequence[User]:
        stmt = Select(User)

        if filters.is_active is not None:
            stmt = stmt.where(User.is_active.is_(filters.is_active))
        if filters.role is not None:
            stmt = stmt.join(User.role).where(Role.name == filters.role)

        return self.db.scalars(stmt).all()

    def find_by_id(self, entity_id: int) -> User | None:
        stmt = Select(User).where(User.id == entity_id)
        return self.db.scalar(stmt)

    def create(self, entity: User) -> User:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: User) -> User:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: User) -> None:
        entity.is_active = False
        self.db.commit()

    def find_by_email(self, email: str) -> User | None:
        stmt = Select(User).where(User.email == email)
        return self.db.scalar(stmt)
