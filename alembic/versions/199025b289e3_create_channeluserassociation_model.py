"""Create ChannelUserAssociation model

Revision ID: 199025b289e3
Revises: 923f65666f60
Create Date: 2024-09-23 15:15:04.858636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '199025b289e3'
down_revision: Union[str, None] = '923f65666f60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel_user_association',
    sa.Column('channel_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('channel_id', 'user_id')
    )
    op.drop_table('channel_user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('channel_user',
    sa.Column('channel_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['channel_id'], ['channels.id'], name='channel_user_channel_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='channel_user_user_id_fkey'),
    sa.PrimaryKeyConstraint('channel_id', 'user_id', name='channel_user_pkey')
    )
    op.drop_table('channel_user_association')
    # ### end Alembic commands ###
