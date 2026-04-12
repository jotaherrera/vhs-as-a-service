from factory import Faker, LazyFunction, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.core.security import hash_password
from app.modules.user.model import User
from tests.factories.role import RoleFactory


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("email",)

    role = SubFactory(RoleFactory)
    email = Faker("email")
    password = LazyFunction(lambda: hash_password("testpassword123"))
    name = Faker("first_name")
    last_name = Faker("last_name")
    is_active = True

    @classmethod
    def _create(cls, model_class: type[User], *args: object, **kwargs: object) -> User:
        if "password" in kwargs and isinstance(kwargs["password"], str):
            kwargs["password"] = hash_password(kwargs["password"])
        return super()._create(model_class, *args, **kwargs)
