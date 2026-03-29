from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.database.seeders.bootstrap import ADMIN_USER, SEED_ROLES, seed_admin, seed_roles
from app.models import Role, User
from tests.factories.role import RoleFactory


def test_seed_roles(db_session: Session) -> None:
    seed_roles(db_session)

    names = {r.name for r in db_session.query(Role).all()}

    assert names == set(SEED_ROLES)


def test_seed_roles_is_idempotent(db_session: Session) -> None:
    RoleFactory.create(name="user")

    seed_roles(db_session)

    count = db_session.query(Role).count()
    assert count == len(SEED_ROLES)


def test_seed_admin(db_session: Session) -> None:
    RoleFactory.create(name="admin")

    seed_admin(db_session)

    user = db_session.query(User).filter(User.email == ADMIN_USER["email"]).one()

    assert user.name == ADMIN_USER["name"]
    assert user.is_active is True
    assert verify_password(ADMIN_USER["password"], user.password)


def test_seed_admin_is_idempotent(db_session: Session) -> None:
    RoleFactory.create(name="admin")

    seed_admin(db_session)
    seed_admin(db_session)

    count = db_session.query(User).filter(User.email == ADMIN_USER["email"]).count()
    assert count == 1
