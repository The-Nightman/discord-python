"""add server invites

Revision ID: bb732f5c5a60
Revises: dc1259e0e7eb
Create Date: 2024-11-19 21:49:22.655232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bb732f5c5a60'
down_revision: Union[str, None] = 'dc1259e0e7eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('serverinvite',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('server_id', sa.Uuid(), nullable=False),
    sa.Column('invite_code', sqlmodel.sql.sqltypes.AutoString(length=8), nullable=False),
    sa.Column('expires_at', sa.Integer(), nullable=False),
    sa.Column('uses', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['server_id'], ['server.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('serverinvite')
    # ### end Alembic commands ###
