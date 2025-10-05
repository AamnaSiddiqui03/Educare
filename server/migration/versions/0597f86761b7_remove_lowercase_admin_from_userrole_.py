"""Remove lowercase admin from userrole enum

Revision ID: 0597f86761b7
Revises: af2d723fcbe6
Create Date: 2025-10-04 23:05:18.858978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0597f86761b7'
down_revision: Union[str, Sequence[str], None] = 'af2d723fcbe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Since PostgreSQL doesn't support removing enum values directly,
    # we need to recreate the enum type with only the correct values
    
    # First, create a new enum type with only the correct values
    op.execute("CREATE TYPE userrole_new AS ENUM ('STUDENT', 'DONOR', 'MENTOR', 'ADMIN')")
    
    # Update the column to use the new enum type
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole_new USING role::text::userrole_new")
    
    # Drop the old enum type
    op.execute("DROP TYPE userrole")
    
    # Rename the new enum type to the original name
    op.execute("ALTER TYPE userrole_new RENAME TO userrole")


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the original enum with lowercase admin
    op.execute("CREATE TYPE userrole_new AS ENUM ('STUDENT', 'DONOR', 'MENTOR', 'admin')")
    
    # Update the column to use the new enum type
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole_new USING role::text::userrole_new")
    
    # Drop the current enum type
    op.execute("DROP TYPE userrole")
    
    # Rename the new enum type to the original name
    op.execute("ALTER TYPE userrole_new RENAME TO userrole")
