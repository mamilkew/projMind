"""empty message

Revision ID: eb98722a5ff0
Revises: c65a2954576b
Create Date: 2018-05-16 16:59:48.280901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb98722a5ff0'
down_revision = 'c65a2954576b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'user', ['user_id'], ['id'])
    op.add_column('user', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_hash')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'user_id')
    # ### end Alembic commands ###