import pytest
from pydantic import SecretStr

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError
from app.modules.role.model import Role, RoleName
from app.modules.user.model import User
from app.modules.user.schemas import UserCreate, UserResponse
from app.modules.user.service import UserService
from tests.fakes.factories.role import RoleFactory
from tests.fakes.factories.user import UserFactory
from tests.fakes.repository import FakeRoleRepository, FakeUserRepository


def make_service(
    users: list[User] | None = None,
    roles: list[Role] | None = None,
) -> UserService:
    return UserService(
        user_repo=FakeUserRepository(users),
        role_repo=FakeRoleRepository(roles),
    )


def make_user_create(
    *,
    email: str = "new@example.com",
    role: RoleName = RoleName.CUSTOMER,
) -> UserCreate:
    return UserCreate(
        email=email,
        password=SecretStr("secret1234"),
        name="Jane",
        last_name="Doe",
        role=role,
    )


def test_list_all_users_returns_all_users_when_staff() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    other = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = make_service(users=[staff, other])

    result = service.list_all_users(current_user=staff)

    assert result.total == 2
    assert len(result.users) == 2


def test_list_all_users_raises_forbidden_when_customer() -> None:
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = make_service(users=[customer])

    with pytest.raises(ForbiddenError):
        service.list_all_users(current_user=customer)


def test_register_user_creates_user_successfully() -> None:
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    service = make_service(roles=[role])

    result = service.register_user(make_user_create())

    assert result.email == "new@example.com"
    assert result.name == "Jane"


def test_register_user_returns_user_response_schema() -> None:
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    service = make_service(roles=[role])

    result = service.register_user(make_user_create())

    assert isinstance(result, UserResponse)


def test_register_user_raises_conflict_when_email_already_exists() -> None:
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    existing = UserFactory.build(email="taken@example.com", role=role)
    service = make_service(users=[existing], roles=[role])

    with pytest.raises(ConflictError):
        service.register_user(make_user_create(email="taken@example.com"))


def test_register_user_raises_not_found_when_role_does_not_exist() -> None:
    service = make_service(roles=[])

    with pytest.raises(NotFoundError):
        service.register_user(make_user_create())


def test_register_user_hashes_password() -> None:
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    fake_repo = FakeUserRepository()
    service = UserService(user_repo=fake_repo, role_repo=FakeRoleRepository([role]))

    service.register_user(make_user_create())

    persisted = next(iter(fake_repo.entities.values()))
    assert persisted.password != "secret1234"  # noqa: S105


def test_register_user_persists_correct_role() -> None:
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    fake_repo = FakeUserRepository()
    service = UserService(user_repo=fake_repo, role_repo=FakeRoleRepository([role]))

    service.register_user(make_user_create())

    persisted = next(iter(fake_repo.entities.values()))
    assert persisted.role_id == role.id
    assert persisted.role == role


def test_get_user_profile_returns_own_profile() -> None:
    customer = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = make_service(users=[customer])

    result = service.get_user_profile(current_user=customer, user_id=customer.id)

    assert result.id == customer.id
    assert result.email == customer.email


def test_get_user_profile_staff_can_view_any_profile() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    target = UserFactory.build(role=RoleFactory.build(name=RoleName.CUSTOMER))
    service = make_service(users=[staff, target])

    result = service.get_user_profile(current_user=staff, user_id=target.id)

    assert result.id == target.id


def test_get_user_profile_raises_forbidden_when_customer_views_other() -> None:
    role = RoleFactory.build(name=RoleName.CUSTOMER)
    requester = UserFactory.build(role=role)
    other = UserFactory.build(role=role)
    service = make_service(users=[requester, other])

    with pytest.raises(ForbiddenError):
        service.get_user_profile(current_user=requester, user_id=other.id)


def test_get_user_profile_raises_not_found_when_user_does_not_exist() -> None:
    staff = UserFactory.build(role=RoleFactory.build(name=RoleName.STAFF))
    service = make_service(users=[staff])

    with pytest.raises(NotFoundError):
        service.get_user_profile(current_user=staff, user_id=999)
