"""update constraint names.

Revision ID: eab06c628d12
Revises: 043051aed244
Create Date: 2025-12-14 11:01:09.247770

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eab06c628d12"
down_revision: str | Sequence[str] | None = "043051aed244"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TABLE users RENAME CONSTRAINT users_pkey TO pk_users")

    op.execute("ALTER TABLE users RENAME CONSTRAINT users_email_key TO uq_users_email")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE users RENAME CONSTRAINT pk_users TO users_pkey")
    op.execute("ALTER TABLE users RENAME CONSTRAINT uq_users_email TO users_email_key")
