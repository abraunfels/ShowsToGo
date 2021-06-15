"""empty message

Revision ID: 9bb4f7270d39
Revises: 0ab89880b372
Create Date: 2020-10-09 23:19:39.807202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb4f7270d39'
down_revision = '0ab89880b372'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seats', sa.Column('ticketid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'seats', 'tickets', ['ticketid'], ['ticketid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'seats', type_='foreignkey')
    op.drop_column('seats', 'ticketid')
    # ### end Alembic commands ###
