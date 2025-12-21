"""update constraint names.

Revision ID: eab06c628d12
Revises: 043051aed244
Create Date: 2025-12-14 11:01:09.247770

"""

from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = "eab06c628d12"
down_revision: str | Sequence[str] | None = "043051aed244"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    pk_result = conn.execute(
        text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_schema = 'app'
            AND table_name = 'users'
            AND constraint_type = 'PRIMARY KEY'
        """),
    )
    pk_row = pk_result.fetchone()
    if pk_row and pk_row[0] != "pk_users":
        pk_name = pk_row[0]
        op.execute(f'ALTER TABLE users RENAME CONSTRAINT "{pk_name}" TO pk_users')

    uq_result = conn.execute(
        text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_schema = 'app'
            AND table_name = 'users'
            AND constraint_type = 'UNIQUE'
            AND constraint_name LIKE '%email%'
        """),
    )
    uq_row = uq_result.fetchone()
    if uq_row and uq_row[0] != "uq_users_email":
        uq_name = uq_row[0]
        op.execute(f'ALTER TABLE users RENAME CONSTRAINT "{uq_name}" TO uq_users_email')


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()

    pk_result = conn.execute(
        text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_schema = 'app'
            AND table_name = 'users'
            AND constraint_type = 'PRIMARY KEY'
            AND constraint_name = 'pk_users'
        """),
    )
    if pk_result.fetchone():
        op.execute("ALTER TABLE users RENAME CONSTRAINT pk_users TO users_pkey")

    uq_result = conn.execute(
        text("""
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE table_schema = 'app'
            AND table_name = 'users'
            AND constraint_type = 'UNIQUE'
            AND constraint_name = 'uq_users_email'
        """),
    )
    if uq_result.fetchone():
        op.execute("ALTER TABLE users RENAME CONSTRAINT uq_users_email TO users_email_key")
