"""Update category_order column

Revision ID: cda5ddf932c6
Revises: 66eba8c58b46
Create Date: 2024-07-31 00:49:45.989190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cda5ddf932c6'
down_revision: Union[str, None] = '66eba8c58b46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('categories', 'category_order',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('categories', 'category_order',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
