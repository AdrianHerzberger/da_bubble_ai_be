"""Create channels model and channeluserassociation model 

Revision ID: 28de27cf4fc6
Revises: 057f5982fd35
Create Date: 2024-09-26 14:14:11.700333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28de27cf4fc6'
down_revision: Union[str, None] = '057f5982fd35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('channel_name', sa.String(length=50), nullable=False),
    sa.Column('channel_description', sa.String(length=100), nullable=False),
    sa.Column('channel_color', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('channel_user_association',
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('channel_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('channel_user_association')
    op.drop_table('channels')
    # ### end Alembic commands ###