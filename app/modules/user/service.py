from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.core.security import hash_password
from app.modules.role.contracts import AbstractRoleRepository
from app.modules.role.model import RoleName
from app.modules.role.repository import RoleRepo
from app.modules.user.contracts import AbstractUserRepository
from app.modules.user.model import User
from app.modules.user.repository import UserRepo
from app.modules.user.schemas import UserCreate, UserList, UserResponse


def get_user_service(user_repo: UserRepo, role_repo: RoleRepo) -> "UserService":
    return UserService(user_repo=user_repo, role_repo=role_repo)


class UserService:
    def __init__(
        self,
        user_repo: AbstractUserRepository,
        role_repo: AbstractRoleRepository,
    ) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo

    def list_all_users(self, current_user: User) -> UserList:
        if current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        users = self.user_repo.get_all()
        return UserList(
            users=[UserResponse.model_validate(user) for user in users],
            total=len(users),
        )

    def register_user(self, user_request: UserCreate) -> UserResponse:
        potential_user = self.user_repo.get_by_email(user_request.email)
        if potential_user is not None:
            raise ConflictError(detail="A user with this email already exists")

        db_role = self.role_repo.get_by_name(user_request.role)
        if db_role is None:
            raise NotFoundError(detail="Role not found")

        user = User(
            email=user_request.email,
            password=hash_password(user_request.password.get_secret_value()),
            name=user_request.name,
            last_name=user_request.last_name,
            is_active=True,
            role_id=db_role.id,
            role=db_role,
        )

        return UserResponse.model_validate(self.user_repo.create(user))

    def get_user_profile(self, current_user: User, user_id: int) -> UserResponse:
        if current_user.id != user_id and current_user.role.name != RoleName.STAFF:
            raise ForbiddenError(detail="Not authorized to perform this action")

        user = self.user_repo.find_by_id(int(user_id))
        if not user:
            raise NotFoundError(detail="User not found")

        return UserResponse.model_validate(user)
