from sqlalchemy.orm import Session

from app.modules.roles.model import Role


def get_by_id(db: Session, entity_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == entity_id).first()


def get_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()


def get_all(db: Session) -> list[Role]:
    return db.query(Role).all()


def create(db: Session, role: Role) -> Role:
    db.add(role)
    db.commit()
    db.refresh(role)
    return role
