"""empty message

Revision ID: 90a934bf3f12
Revises: 069e57012f09
Create Date: 2020-10-11 21:49:49.379482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90a934bf3f12'
down_revision = '069e57012f09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('subgenres_parentid_fkey', 'subgenres', type_='foreignkey')
    op.drop_column('subgenres', 'parentid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subgenres', sa.Column('parentid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('subgenres_parentid_fkey', 'subgenres', 'genres', ['parentid'], ['genreid'])
    # ### end Alembic commands ###
