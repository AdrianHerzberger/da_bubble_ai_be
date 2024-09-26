"""Drop channel_user_association and channels tables

Revision ID: 057f5982fd35
Revises: 199025b289e3
Create Date: 2024-09-26 13:37:53.652584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '057f5982fd35'
down_revision: Union[str, None] = '199025b289e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the channel_user_association table
    op.drop_table('channel_user_association')

    # Drop the channels table
    op.drop_table('channels')


def downgrade() -> None:
    # Recreate the channels table
    op.create_table('channels',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('channel_name', sa.String(length=50), nullable=False),
        sa.Column('channel_description', sa.String(length=100), nullable=False),
        sa.Column('channel_color', sa.String(length=50), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Recreate the channel_user_association table
    op.create_table('channel_user_association',
        sa.Column('channel_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('channel_id', 'user_id')
    )
