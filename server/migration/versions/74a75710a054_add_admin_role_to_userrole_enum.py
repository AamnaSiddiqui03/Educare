"""Add admin role to UserRole enum

Revision ID: 74a75710a054
Revises: 48406ecc149a
Create Date: 2025-10-04 22:53:46.989269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74a75710a054'
down_revision: Union[str, Sequence[str], None] = '48406ecc149a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add 'admin' value to the existing UserRole enum
    op.execute("ALTER TYPE userrole ADD VALUE 'admin'")


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type and updating all references
    # For now, we'll leave the admin value in place
    pass
