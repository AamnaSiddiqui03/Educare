"""Update ParentLiveStatus enum values to both/one/none

Revision ID: bd2ed1c35a25
Revises: 0597f86761b7
Create Date: 2025-10-04 23:26:22.174277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd2ed1c35a25'
down_revision: Union[str, Sequence[str], None] = '0597f86761b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # First, add a temporary text column
    op.add_column('students', sa.Column('parent_live_status_temp', sa.String()))
    
    # Copy and transform the data
    op.execute("""
        UPDATE students 
        SET parent_live_status_temp = CASE 
            WHEN parent_live_status::text = 'alive' THEN 'both'
            WHEN parent_live_status::text = 'deceased' THEN 'none'
            WHEN parent_live_status::text = 'unknown' THEN 'none'
            ELSE parent_live_status::text
        END
        WHERE parent_live_status IS NOT NULL
    """)
    
    # Drop the old column
    op.drop_column('students', 'parent_live_status')
    
    # Create new enum type with updated values
    op.execute("CREATE TYPE parentlivestatus_new AS ENUM ('both', 'one', 'none')")
    
    # Add the column back with the new enum type
    op.add_column('students', sa.Column('parent_live_status', sa.Enum('both', 'one', 'none', name='parentlivestatus_new')))
    
    # Copy data from temp column
    op.execute("UPDATE students SET parent_live_status = parent_live_status_temp::parentlivestatus_new WHERE parent_live_status_temp IS NOT NULL")
    
    # Drop the temp column
    op.drop_column('students', 'parent_live_status_temp')
    
    # Drop the old enum type
    op.execute("DROP TYPE parentlivestatus")
    
    # Rename the new enum type to the original name
    op.execute("ALTER TYPE parentlivestatus_new RENAME TO parentlivestatus")


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate the original enum type
    op.execute("CREATE TYPE parentlivestatus_new AS ENUM ('alive', 'deceased', 'unknown')")
    
    # Update any existing data to map new values back to old values
    op.execute("""
        UPDATE students 
        SET parent_live_status = CASE 
            WHEN parent_live_status = 'both' THEN 'alive'
            WHEN parent_live_status = 'one' THEN 'deceased'
            WHEN parent_live_status = 'none' THEN 'unknown'
            ELSE parent_live_status
        END::text::parentlivestatus_new
        WHERE parent_live_status IS NOT NULL
    """)
    
    # Update the column type
    op.execute("ALTER TABLE students ALTER COLUMN parent_live_status TYPE parentlivestatus_new USING parent_live_status::text::parentlivestatus_new")
    
    # Drop the current enum type
    op.execute("DROP TYPE parentlivestatus")
    
    # Rename the new enum type to the original name
    op.execute("ALTER TYPE parentlivestatus_new RENAME TO parentlivestatus")
