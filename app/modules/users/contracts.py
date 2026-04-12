from app.modules.shared.contracts import AbstractRepository
from app.modules.users.model import User


class AbstractUserRepository(AbstractRepository[User]):
    def get_by_email(self, email: str) -> User | None: ...
