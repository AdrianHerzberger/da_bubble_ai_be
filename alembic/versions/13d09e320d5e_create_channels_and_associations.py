"""create channels and associations

Revision ID: 13d09e320d5e
Revises: 28de27cf4fc6
Create Date: 2024-09-26 14:49:20.971643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13d09e320d5e'
down_revision: Union[str, None] = '28de27cf4fc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'channels',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('channel_name', sa.String(length=50), nullable=False),
        sa.Column('channel_description', sa.String(length=100), nullable=False),
        sa.Column('channel_color', sa.String(length=50), nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )
    
    op.create_table(
        'channel_user_association',
        sa.Column('channel_id', sa.Integer, sa.ForeignKey('channels.id'), primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), primary_key=True),
    )

def downgrade():
    op.drop_table('channel_user_association')
    op.drop_table('channels')
