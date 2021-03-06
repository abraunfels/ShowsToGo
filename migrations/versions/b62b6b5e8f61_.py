"""empty message

Revision ID: b62b6b5e8f61
Revises: f8b55d89982f
Create Date: 2020-10-14 23:29:07.604665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b62b6b5e8f61'
down_revision = 'f8b55d89982f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('seatid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tickets', 'seats', ['seatid'], ['seatid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tickets', type_='foreignkey')
    op.drop_column('tickets', 'seatid')
    # ### end Alembic commands ###
