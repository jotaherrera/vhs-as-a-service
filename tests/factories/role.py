from factory.alchemy import SQLAlchemyModelFactory

from app.models import Role
from app.models.role import Roles


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = Roles.CUSTOMER
    is_active = True
