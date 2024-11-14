"""Add create_date column to channels

Revision ID: 919a83f08738
Revises: d68b72e9cd08
Create Date: 2024-11-14 11:54:29.237966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import datetime

# revision identifiers, used by Alembic.
revision: str = '919a83f08738'
down_revision: Union[str, None] = 'd68b72e9cd08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

channels_table = table('channels', column('create_date', sa.DateTime))

def upgrade() -> None:
    op.add_column('channels', sa.Column('create_date', sa.DateTime(), nullable=True))

    op.execute(
        channels_table.update().values(create_date=datetime.datetime.utcnow())
    )
    
    op.alter_column('channels', 'create_date', nullable=False)

def downgrade() -> None:
    op.drop_column('channels', 'create_date')
