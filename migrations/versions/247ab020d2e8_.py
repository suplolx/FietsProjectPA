"""empty message

Revision ID: 247ab020d2e8
Revises: d3c955f2061f
Create Date: 2017-11-13 13:06:25.516038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '247ab020d2e8'
down_revision = 'd3c955f2061f'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('verwijderd', sa.Column('Foto', sa.String(length=200), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('verwijderd', 'Foto')
    ### end Alembic commands ###
