from factory.alchemy import SQLAlchemyModelFactory

from app.modules.roles.model import Role, Roles


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = Roles.CUSTOMER
    is_active = True
