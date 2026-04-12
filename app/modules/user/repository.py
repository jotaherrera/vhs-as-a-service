from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, Sequence
from sqlalchemy.orm import Session

from app.database.infrastructure.session import DbSession
from app.modules.user.contracts import AbstractUserRepository
from app.modules.user.model import User


class UserRepository(AbstractUserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, *, is_active: bool | None = None) -> Sequence[User]:
        stmt = Select(User)

        if is_active is not None:
            stmt = stmt.where(User.is_active.is_(is_active))

        return self.db.scalars(stmt).all()

    def find_by_id(self, entity_id: int) -> User | None:
        stmt = Select(User).where(User.id == entity_id)
        return self.db.scalar(stmt)

    def create(self, entity: User) -> User:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_email(self, email: str) -> User | None:
        stmt = Select(User).where(User.email == email)
        return self.db.scalar(stmt)


def get_user_repository(db: DbSession) -> AbstractUserRepository:
    return UserRepository(db)


UserRepo = Annotated[AbstractUserRepository, Depends(get_user_repository)]
