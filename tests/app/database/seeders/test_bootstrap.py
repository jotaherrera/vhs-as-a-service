from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.database.seeders.bootstrap import STAFF_USER, seed_roles, seed_staff
from app.models import Role, User
from app.models.role import Roles
from tests.factories.role import RoleFactory


def test_seed_roles(db_session: Session) -> None:
    seed_roles(db_session)

    names = {r.name for r in db_session.query(Role).all()}

    assert names == set(Roles)


def test_seed_roles_is_idempotent(db_session: Session) -> None:
    RoleFactory.create(name=Roles.CUSTOMER)

    seed_roles(db_session)

    count = db_session.query(Role).count()
    assert count == len(Roles)


def test_seed_staff(db_session: Session) -> None:
    RoleFactory.create(name=Roles.STAFF)

    seed_staff(db_session)

    user = db_session.query(User).filter(User.email == STAFF_USER["email"]).one()

    assert user.name == STAFF_USER["name"]
    assert user.is_active is True
    assert verify_password(STAFF_USER["password"], user.password)


def test_seed_staff_is_idempotent(db_session: Session) -> None:
    RoleFactory.create(name=Roles.STAFF)

    seed_staff(db_session)
    seed_staff(db_session)

    count = db_session.query(User).filter(User.email == STAFF_USER["email"]).count()
    assert count == 1
