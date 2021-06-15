"""empty message

Revision ID: a8ad8ef2b336
Revises: e6918464a3b8
Create Date: 2020-10-15 20:40:09.284039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8ad8ef2b336'
down_revision = 'e6918464a3b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seatsforshow', sa.Column('close', sa.Boolean(), nullable=True))
    op.drop_column('seatsforshow', 'seatstatus')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seatsforshow', sa.Column('seatstatus', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('seatsforshow', 'close')
    # ### end Alembic commands ###
