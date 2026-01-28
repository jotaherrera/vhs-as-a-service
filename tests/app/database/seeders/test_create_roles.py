from sqlalchemy.orm import Session

from app.database.seeders.create_roles import create_roles
from app.models import Role


def test_create_roles(db_session: Session) -> None:
    create_roles(db_session)

    all_roles = db_session.query(Role).all()

    returned_names = {r.name for r in all_roles}

    assert returned_names == {"admin", "user"}
