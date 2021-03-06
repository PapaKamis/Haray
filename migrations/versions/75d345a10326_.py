"""empty message

Revision ID: 75d345a10326
Revises: 9848d5da73b8
Create Date: 2020-07-18 13:07:12.602110

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75d345a10326'
down_revision = '9848d5da73b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('transaction_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment', 'transaction_date')
    # ### end Alembic commands ###
