"""empty message

Revision ID: 62a8eaefedc6
Revises: 1e0328c50262
Create Date: 2020-07-17 17:03:32.621474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a8eaefedc6'
down_revision = '1e0328c50262'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('buyer_user_id', sa.Integer(), nullable=False))
    op.add_column('payment', sa.Column('seller_user_id', sa.Integer(), nullable=False))
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.create_foreign_key(None, 'payment', 'user', ['seller_user_id'], ['user_id'])
    op.create_foreign_key(None, 'payment', 'user', ['buyer_user_id'], ['user_id'])
    op.drop_column('payment', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('user_id', sa.INTEGER(), nullable=False))
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.drop_constraint(None, 'payment', type_='foreignkey')
    op.create_foreign_key(None, 'payment', 'user', ['user_id'], ['user_id'])
    op.drop_column('payment', 'seller_user_id')
    op.drop_column('payment', 'buyer_user_id')
    # ### end Alembic commands ###
