"""empty message

Revision ID: e3dd16bf75c2
Revises: 0b2263c87f52
Create Date: 2020-10-14 23:57:16.687275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3dd16bf75c2'
down_revision = '0b2263c87f52'
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