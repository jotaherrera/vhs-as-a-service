from factory.alchemy import SQLAlchemyModelFactory

from app.modules.role.model import Role, RoleName


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = RoleName.CUSTOMER
    is_active = True
