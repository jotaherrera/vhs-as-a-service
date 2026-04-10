from sqlalchemy.orm import Session

from app.modules.roles.model import Role
from app.modules.roles.schemas import RoleCreate


def get_all_roles(db: Session) -> list[Role]:
    return db.query(Role).all()


def get_role_by_name(db: Session, name: str) -> Role | None:
    return db.query(Role).filter(Role.name == name).first()


def get_role_by_id(db: Session, role_id: int) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()


def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(**role.model_dump())

    db.add(db_role)
    db.commit()
    db.refresh(db_role)

    return db_role
