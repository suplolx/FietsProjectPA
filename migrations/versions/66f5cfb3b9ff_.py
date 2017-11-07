"""empty message

Revision ID: 66f5cfb3b9ff
Revises: 28bccba952a9
Create Date: 2017-10-09 07:39:00.742428

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66f5cfb3b9ff'
down_revision = '28bccba952a9'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('fiets', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'fiets', 'user', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'fiets', type_='foreignkey')
    op.drop_column('fiets', 'user_id')
    ### end Alembic commands ###