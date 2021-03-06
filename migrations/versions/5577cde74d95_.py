"""empty message

Revision ID: 5577cde74d95
Revises: 13ba9775797d
Create Date: 2020-10-09 21:08:57.305637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5577cde74d95'
down_revision = '13ba9775797d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('shows_hallid_fkey', 'shows', type_='foreignkey')
    op.drop_column('shows', 'hallid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('hallid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('shows_hallid_fkey', 'shows', 'halls', ['hallid'], ['hallid'])
    # ### end Alembic commands ###
