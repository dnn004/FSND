"""empty message

Revision ID: bc91c29cd09f
Revises: b09a0b8fe250
Create Date: 2020-06-23 01:35:40.938643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc91c29cd09f'
down_revision = 'b09a0b8fe250'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###