from factory.alchemy import SQLAlchemyModelFactory

from app.models import Role


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = "user"
    is_active = True
