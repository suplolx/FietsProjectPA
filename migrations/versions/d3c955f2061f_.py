"""empty message

Revision ID: d3c955f2061f
Revises: 01a4427599da
Create Date: 2017-11-07 08:57:41.337352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3c955f2061f'
down_revision = '01a4427599da'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fiets', sa.Column('Datum_verwijderd', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fiets', 'Datum_verwijderd')
    ### end Alembic commands ###
