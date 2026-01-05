from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> UserResponse:
    hashed_password = hash_password(user.password)
    db_user = User(**user.model_dump(exclude={"password"}), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
