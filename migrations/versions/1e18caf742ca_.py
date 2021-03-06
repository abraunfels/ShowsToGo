"""empty message

Revision ID: 1e18caf742ca
Revises: e3dd16bf75c2
Create Date: 2020-10-14 23:57:41.488693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e18caf742ca'
down_revision = 'e3dd16bf75c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seats', sa.Column('seatstatus', sa.Enum('free', 'close', name='seatstatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seats', 'seatstatus')
    # ### end Alembic commands ###
