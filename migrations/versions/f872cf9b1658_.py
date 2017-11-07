"""empty message

Revision ID: f872cf9b1658
Revises: 85a4a2bfd35e
Create Date: 2017-10-17 09:55:36.830608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f872cf9b1658'
down_revision = '85a4a2bfd35e'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fiets', sa.Column('user_edt', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fiets', 'user', ['user_edt'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fiets', type_='foreignkey')
    op.drop_column('fiets', 'user_edt')
    ### end Alembic commands ###