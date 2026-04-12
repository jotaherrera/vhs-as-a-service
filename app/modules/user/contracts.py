from app.modules.shared.contracts import AbstractRepository
from app.modules.user.model import User


class AbstractUserRepository(AbstractRepository[User]):
    def get_by_email(self, email: str) -> User | None: ...
