from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.models import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100))
    last_name = Column(String(100))

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now,
        nullable=False,
    )

    role = relationship("Role", back_populates="users")

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, email={self.email}, name={self.name}, "
            f"last_name={self.last_name}, role={self.role.name}), "
        )
