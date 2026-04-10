from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.core.security import hash_password
from app.database.infrastructure.session import DbSession
from app.modules.roles import repository as role_repo
from app.modules.roles.model import Roles
from app.modules.users import repository as user_repo
from app.modules.users.model import User
from app.modules.users.schemas import UserCreate


def list_users(db: DbSession, current_user: User) -> list[User]:
    if current_user.role.name != Roles.STAFF:
        raise ForbiddenError(detail="Not authorized to perform this action")

    return user_repo.get_all(db)


def create_user(db: DbSession, user_request: UserCreate) -> User:
    potential_user = user_repo.get_by_email(db, user_request.email)
    if potential_user is not None:
        raise ConflictError(detail="A user with this email already exists")

    db_role = role_repo.get_by_name(db, user_request.role)
    if db_role is None:
        raise NotFoundError(detail="Role not found")

    return User(
        email=user_request.email,
        password=hash_password(user_request.password.get_secret_value()),
        name=user_request.name,
        last_name=user_request.last_name,
        is_active=True,
        role_id=db_role.id,
    )


def get_user(db: DbSession, current_user: User, user_id: int) -> User:
    if current_user.id != user_id and current_user.role.name != Roles.STAFF:
        raise ForbiddenError(detail="Not authorized to perform this action")

    user = user_repo.get_by_id(db, int(user_id))
    if not user:
        raise NotFoundError(detail="User not found")

    return user
