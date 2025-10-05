"""Fix admin enum value case

Revision ID: af2d723fcbe6
Revises: 74a75710a054
Create Date: 2025-10-04 22:59:13.789859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af2d723fcbe6'
down_revision: Union[str, Sequence[str], None] = '74a75710a054'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # First, add the correct ADMIN value
    op.execute("ALTER TYPE userrole ADD VALUE 'ADMIN'")
    
    # Note: We can't remove the lowercase 'admin' value directly
    # The lowercase 'admin' will remain but won't be used


def downgrade() -> None:
    """Downgrade schema."""
    # Note: PostgreSQL doesn't support removing enum values directly
    # This would require recreating the enum type and updating all references
    pass
