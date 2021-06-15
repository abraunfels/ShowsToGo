"""empty message

Revision ID: 069e57012f09
Revises: b40bea776b79
Create Date: 2020-10-11 21:46:20.278522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '069e57012f09'
down_revision = 'b40bea776b79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subgenres', sa.Column('parentid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'subgenres', 'genres', ['parentid'], ['genreid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subgenres', type_='foreignkey')
    op.drop_column('subgenres', 'parentid')
    # ### end Alembic commands ###
