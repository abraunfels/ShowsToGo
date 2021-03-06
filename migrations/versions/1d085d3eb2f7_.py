"""empty message

Revision ID: 1d085d3eb2f7
Revises: dca8b674d3f9
Create Date: 2020-10-14 10:42:27.043583

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1d085d3eb2f7'
down_revision = 'dca8b674d3f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('datetimecreated', sa.DateTime(), nullable=False))
    op.drop_column('comments', 'dreated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('dreated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('comments', 'datetimecreated')
    # ### end Alembic commands ###
