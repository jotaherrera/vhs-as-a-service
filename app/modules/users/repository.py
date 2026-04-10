from sqlalchemy.orm import Session

from app.modules.users.model import User


def get_by_id(db: Session, entity_id: int) -> User | None:
    return db.query(User).filter(User.id == entity_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_all(db: Session) -> list[User]:
    return db.query(User).all()


def create(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
