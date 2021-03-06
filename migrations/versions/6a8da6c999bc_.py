"""empty message

Revision ID: 6a8da6c999bc
Revises: 14e222fb2862
Create Date: 2020-10-15 19:57:00.904992

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6a8da6c999bc'
down_revision = '14e222fb2862'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seatsforshow', 'seatstatus')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seatsforshow', sa.Column('seatstatus', postgresql.ENUM('free', 'close', name='freeclose'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
