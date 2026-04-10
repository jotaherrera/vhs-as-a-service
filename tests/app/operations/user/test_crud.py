from pydantic import SecretStr
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.modules.roles.model import Roles
from app.modules.users import repository as user_repo
from app.modules.users.schemas import UserCreate
from tests.factories.role import RoleFactory
from tests.factories.user import UserFactory


def test_get_all_users(db_session: Session) -> None:
    user_1 = UserFactory.create()
    user_2 = UserFactory.create()

    all_users = user_repo.get_all_users(db_session)

    returned_ids = {u.id for u in all_users}

    assert returned_ids == {user_1.id, user_2.id}


def test_get_user_by_id(db_session: Session) -> None:
    user = UserFactory.create()
    user_db = user_repo.get_user_by_id(db_session, user.id)

    assert user_db is not None
    assert user_db.id == user.id
    assert user_db.email == user.email


def test_get_user_by_email(db_session: Session) -> None:
    user = UserFactory.create()
    user_db = user_repo.get_user_by_email(db_session, user.email)

    assert user_db is not None
    assert user_db.id == user.id
    assert user_db.email == user.email


def test_create_user(db_session: Session) -> None:
    role = RoleFactory.create(name=Roles.CUSTOMER)
    user_create = UserCreate(
        email="johndoe@mail.com",
        name="John",
        last_name="Doe",
        password=SecretStr("tests-password"),
        role_id=role.id,
    )

    created_user = user_repo.create_user(db_session, user_create)

    assert created_user.email == user_create.email

    assert created_user.name == user_create.name
    assert created_user.last_name == user_create.last_name
    assert created_user.role_id == role.id

    assert created_user.password != user_create.password
    assert verify_password("tests-password", created_user.password)
