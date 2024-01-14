"""add desc col items table

Revision ID: 0491fbc60b24
Revises: f6205e91048d
Create Date: 2024-01-15 01:11:12.007637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0491fbc60b24'
down_revision: Union[str, None] = 'f6205e91048d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('desc', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'desc')
    # ### end Alembic commands ###
